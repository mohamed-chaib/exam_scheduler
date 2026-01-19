from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from .. import  database
router = APIRouter(tags =['etudiants'],prefix='/etudiants')
@router.get('/')
def get_all_etudiants(db:Session = Depends(database.get_db)):
    etudiants = db.query(models.Etudiant).all()
    return etudiants

@router.get('/{id}')
def get_etudiant(id :int,db:Session = Depends(database.get_db)):
    etudiant = db.query(models.Etudiant).filter(models.Etudiant.id == id).first()
    return etudiant