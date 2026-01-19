from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas , database
router = APIRouter(tags =['inscriptions'],prefix='/inscriptions')
@router.get('/')
def get_all_inscriptions(db:Session = Depends(database.get_db)):
    inscriptions = db.query(models.Inscription).all()
    return inscriptions

@router.get('/{id}')
def get_inscription(id :int,db:Session = Depends(database.get_db)):
    inscription = db.query(models.Inscription).filter(models.Inscription.etudiant_id == id).first()
    return inscription