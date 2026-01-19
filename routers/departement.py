from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas , database
router = APIRouter(tags =['departments'],prefix='/departments')
@router.get('/')
def get_all_depatments(db:Session = Depends(database.get_db)):
    departments = db.query(models.Departement).all()
    return departments

@router.get('/{id}')
def get_depatment(id :int,db:Session = Depends(database.get_db)):
    department = db.query(models.Departement).filter(models.Departement.id == id).first()
    return department