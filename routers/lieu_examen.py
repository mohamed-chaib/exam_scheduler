from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas , database
router = APIRouter(tags =['lieu_examen'],prefix='/lieu_examen')
@router.get('/')
def get_all_lieu_examen(db:Session = Depends(database.get_db)):
    lieu_examen = db.query(models.LieuExamen).all()
    return lieu_examen

@router.get('/{id}')
def get_lieu_examen(id :int,db:Session = Depends(database.get_db)):
    lieu_examen = db.query(models.LieuExamen).filter(models.LieuExamen.id == id).first()
    return lieu_examen