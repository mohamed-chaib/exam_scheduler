from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from .. import schemas , database
from ..controllers import exam 
router = APIRouter(tags =['examens'],prefix='/examens')
from datetime import datetime, timedelta


from datetime import datetime, timedelta

def generate_all_time_slots(start_date: str, days_count: int):
    """
    Generates exam time slots from Saturday to Thursday
    at fixed times: 08:30, 10:30, 12:30.
    """

    slots = []

    daily_times = [
        datetime.strptime("08:30", "%H:%M").time(),
        datetime.strptime("10:15", "%H:%M").time(),
        datetime.strptime("12:00", "%H:%M").time(),
        datetime.strptime("13:45", "%H:%M").time(),

    ]

    current_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    for _ in range(days_count):
        
        if current_date.weekday() != 4:  # 4 = Friday
            for t in daily_times:
                slots.append(datetime.combine(current_date, t))

        current_date += timedelta(days=1)

    return slots

@router.post('/')
def get_examen(db:Session = Depends(database.get_db)):
    all_time_slots = generate_all_time_slots("2026-01-03", 20)
    return exam.generate_smart_exam_schedule(db,"2026-01-03")

@router.get('/')
def get_all_examens(db:Session = Depends(database.get_db)):
    examens = db.query(models.Examen).all()
    return examens

@router.get('/{id}')
def get_examen(id :int,db:Session = Depends(database.get_db)):
    examen = db.query(models.Examen).filter(models.Examen.id == id).first()
    return examen


