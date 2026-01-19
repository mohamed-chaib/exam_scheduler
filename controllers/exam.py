from sqlalchemy.orm import Session, aliased
from sqlalchemy import func ,  and_, exists ,case
from fastapi import Depends
from .. import models, database
import logging
import time


def check_student_conflict(module_id, exam_date, db):
    conflict_exists = db.query(
        db.query(models.Inscription)
        .join(
            models.Examen,
            models.Inscription.module_id == models.Examen.module_id
        )
        .filter(
            models.Inscription.module_id == module_id,
            func.date(models.Examen.date_heure) == exam_date
        )
        .exists()
    ).scalar()

    return conflict_exists





def get_rooms(min_cap, slot, db):
    """
    Finds rooms that are free at the given slot and can hold min_cap students.
    """

    conflict_exists = (
        db.query(models.Examen)
        .filter(
            models.Examen.salle_id == models.LieuExamen.id,
            models.Examen.date_heure == slot
        )
        .exists()
    )

    rooms = (
        db.query(models.LieuExamen)
        .filter(
            models.LieuExamen.capacite >= min_cap,
            ~conflict_exists
        )
        .order_by(models.LieuExamen.capacite.asc())
        .all()
    )

    return rooms





def get_available_profs(slot, date, dept_id, db: Session):

    is_priority = case(
        (models.Professeur.dept_id == dept_id, 1),
        else_=0
    ).label("is_priority")

    total_load = (
        db.query(func.count(models.Examen.id))
        .filter(models.Examen.prof_id == models.Professeur.id)
        .correlate(models.Professeur)
        .scalar_subquery()
    ).label("total_load")

    query = (
        db.query(
            models.Professeur,
            is_priority,
            total_load
        )
        # ❌ Prof already has an exam at the same time
        .filter(
            ~db.query(models.Examen)
            .filter(
                models.Examen.prof_id == models.Professeur.id,
                models.Examen.date_heure == slot
            )
            .exists()
        )
        # ❌ Max exams per day constraint
        .filter(
            db.query(func.count(models.Examen.id))
            .filter(
                models.Examen.prof_id == models.Professeur.id,
                func.date(models.Examen.date_heure) == date
            )
            .correlate(models.Professeur)
            .scalar_subquery() < 3
        )
        # ✅ Correct ORDER BY
        .order_by(
            is_priority.desc(),
            total_load.asc()
        )
    )

    return query.all()



def save_exam(module_id: int, salle_id: int, prof_id: int, slot, db: Session):
    exam = models.Examen(
        module_id=module_id,
        prof_id=prof_id,
        salle_id=salle_id,
        date_heure=slot,
        duree_minutes=90
    )

    db.add(exam)
    db.commit()
    db.refresh(exam)

    return exam



logger = logging.getLogger("exam_scheduler")

def log_conflict(module,reason):
    logger.error(
        reason
    )



def generate_schedule(all_time_slots, db: Session):
    start_time = time.time()

    # 1️⃣ جلب كل البيانات مسبقًا
    inscriptions = db.query(models.Inscription).all()
    examens = db.query(models.Examen).all()
    rooms = db.query(models.LieuExamen).order_by(models.LieuExamen.capacite.asc()).all()
    profs = db.query(models.Professeur).all()

    # 2️⃣ تنظيم بيانات الطلاب حسب المادة
    student_modules = {}
    for insc in inscriptions:
        student_modules.setdefault(insc.module_id, set()).add(insc.etudiant_id)

    # 3️⃣ تنظيم الامتحانات حسب الطالب والتاريخ
    student_schedule = {}
    for ex in examens:
        for insc in student_modules.get(ex.module_id, []):
            student_schedule.setdefault((insc, ex.date_heure.date()), []).append(ex.module_id)

    prof_schedule = {}
    for ex in examens:
        prof_schedule.setdefault((ex.prof_id, ex.date_heure), 0)
        prof_schedule[(ex.prof_id, ex.date_heure)] += 1

    # 5️⃣ جدولة كل مادة
    modules_to_schedule = (
        db.query(
            models.Module,
            func.count(models.Inscription.etudiant_id).label("size")
        )
        .join(models.Inscription, models.Module.id == models.Inscription.module_id)
        .group_by(models.Module.id)
        .order_by(func.count(models.Inscription.etudiant_id).desc())
        .all()
    )

    for module, size in modules_to_schedule:
        scheduled = False

        # الطلاب المسجلين في المادة
        students = student_modules.get(module.id, set())

        for slot in all_time_slots:
            exam_date = slot.date()

            # CONSTRAINT 1: max 1 exam per day per student
            if any((s, exam_date) in student_schedule for s in students):
                continue

            # CONSTRAINT 2: find suitable room
            available_rooms = [r for r in rooms if r.capacite >= size and not any(e.salle_id == r.id and e.date_heure == slot for e in examens)]
            if not available_rooms:
                continue
            selected_room = available_rooms[0]

            # CONSTRAINT 3: find available prof
            available_profs = [p for p in profs if prof_schedule.get((p.id, slot), 0) == 0]
            if not available_profs:
                continue
            selected_prof = available_profs[0]

            # حفظ الامتحان
            save_exam(module.id, selected_room.id, selected_prof.id, slot, db)

            # تحديث الجداول المؤقتة في الذاكرة
            for s in students:
                student_schedule.setdefault((s, exam_date), []).append(module.id)
            prof_schedule[(selected_prof.id, slot)] = 1
            examens.append(models.Examen(module_id=module.id, salle_id=selected_room.id, prof_id=selected_prof.id, date_heure=slot, duree_minutes=90))

            scheduled = True
            break

        if not scheduled:
            log_conflict(module, reason="No valid slot satisfying constraints")

    end_time = time.time()
    duration = end_time - start_time
    print(f"Total Execution Time: {duration:.2f} seconds")
