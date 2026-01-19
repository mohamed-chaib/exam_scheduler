from fastapi import FastAPI
from .routers  import departement ,formation,etudiant ,module,lieu_examen , professeurs,inscription,examen
from .database import engine 
from . import models
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(formation.router)
app.include_router(departement.router)
app.include_router(etudiant.router)
app.include_router(module.router)
app.include_router(lieu_examen.router)
app.include_router(professeurs.router)
app.include_router(inscription.router)
app.include_router(examen.router)
