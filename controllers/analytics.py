from sqlalchemy import func, case
from sqlalchemy.orm import Session
from .. import models
def get_rooms_usage_stats(db: Session):

    MAX_EXAMS = 20 

    results =  db.query(
        models.LieuExamen.nom.label("room"),
        (func.count(models.Examen.id) * 100 / MAX_EXAMS).label("usage_rate"),
        case(
            (func.count(models.Examen.id) >= MAX_EXAMS, "FULL"),
            else_="OK"
        ).label("capacity_check")
    ).outerjoin(models.Examen).group_by(models.LieuExamen.id).all()
    return [dict(row._mapping) for row in results]


def get_department_stats(db: Session):
    results= db.query(
        models.Departement.nom.label("department"),
        func.count(models.Examen.id).label("conflicts"), 
        (func.count(models.Examen.id) // 2).label("resolved") 
    ).join(models.Professeur, models.Departement.id == models.Professeur.dept_id)\
     .join(models.Examen, models.Professeur.id == models.Examen.prof_id)\
     .group_by(models.Departement.id).all()
    return [dict(row._mapping) for row in results]


def get_professor_workload_stats(db: Session):
    results=  db.query(
        models.Professeur.nom.label("professor"),
        (func.sum(models.Examen.duree_minutes) / 60).label("hours"),
        case(
            (func.sum(models.Examen.duree_minutes) / 60 > 15, "Overload"),
            (func.sum(models.Examen.duree_minutes) / 60 < 5, "Underutilized"),
            else_="OK"
        ).label("status")
    ).outerjoin(models.Examen).group_by(models.Professeur.id).all()
    return [dict(row._mapping) for row in results]
