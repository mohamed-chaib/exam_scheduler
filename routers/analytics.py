from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import   database
from ..controllers import analytics
router = APIRouter(tags =['analytics'],prefix='/analytics')
@router.get('/room_usage')
def get_room_usage(db:Session = Depends(database.get_db)):
    return analytics.get_rooms_usage_stats(db)

@router.get('/department_conflicts')
def get_department_conflicts(db:Session = Depends(database.get_db)):
    return analytics.get_department_stats(db)

@router.get('/professor_workload')
def get_professor_workload(db:Session = Depends(database.get_db)):
    return analytics.get_professor_workload_stats(db)