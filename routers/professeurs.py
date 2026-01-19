from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas , database
router = APIRouter(tags =['professeurs'],prefix='/professeurs')
@router.get('/')
def get_all_professeurs(db:Session = Depends(database.get_db)):
    professeurs = db.query(models.Professeur).all()
    return professeurs

@router.get('/{id}')
def get_professeur(id :int,db:Session = Depends(database.get_db)):
    professeur = db.query(models.Professeur).filter(models.Professeur.id == id).first()
    return professeur