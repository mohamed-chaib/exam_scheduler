from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas , database
router = APIRouter(tags =['formations'],prefix='/formations')
@router.get('/')
def get_all_formations(db:Session = Depends(database.get_db)):
    formations = db.query(models.Formation).all()
    return formations

@router.get('/{id}')
def get_formation(id :int,db:Session = Depends(database.get_db)):
    formation = db.query(models.Formation).filter(models.Formation.id == id).first()
    return formation