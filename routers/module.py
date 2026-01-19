from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas , database
router = APIRouter(tags =['modules'],prefix='/modules')
@router.get('/')
def get_all_modules(db:Session = Depends(database.get_db)):
    modules = db.query(models.Module).all()
    return modules

@router.get('/{id}')
def get_module(id :int,db:Session = Depends(database.get_db)):
    module = db.query(models.Module).filter(models.Module.id == id).first()
    return module