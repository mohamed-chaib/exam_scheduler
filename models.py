from sqlalchemy import Column, Integer , String ,ForeignKey ,CheckConstraint ,DateTime
from .database import Base
from sqlalchemy.orm import Relationship 


class Departement(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False, unique=True)

    formations = Relationship("Formation", back_populates="departement")
    professeurs = Relationship("Professeur", back_populates="departement")

class Formation(Base):
    __tablename__ = "formations"

    id = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    dept_id = Column(Integer, ForeignKey("departements.id"), nullable=False)
    nb_modules = Column(Integer, nullable=False)

    departement = Relationship("Departement", back_populates="formations")
    modules = Relationship("Module", back_populates="formation")
    etudiants = Relationship("Etudiant", back_populates="formation")

class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    formation_id = Column(Integer, ForeignKey("formations.id"), nullable=False)
    promo = Column(String(10), nullable=False)

    formation = Relationship("Formation", back_populates="etudiants")
    inscriptions = Relationship("Inscription", back_populates="etudiant")



class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    credits = Column(Integer, nullable=False)
    formation_id = Column(Integer, ForeignKey("formations.id"), nullable=False)
    pre_req_id = Column(Integer, ForeignKey("modules.id"), nullable=True)

    formation = Relationship("Formation", back_populates="modules")

    # relation auto-référencée (prérequis)
    prerequis = Relationship("Module", remote_side=[id])

    inscriptions = Relationship("Inscription", back_populates="module")
    examens = Relationship("Examen", back_populates="module")

    __table_args__ = (
        CheckConstraint("credits > 0", name="check_credits_positive"),
    )

class Professeur(Base):
    __tablename__ = "professeurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    dept_id = Column(Integer, ForeignKey("departements.id"), nullable=False)
    specialite = Column(String(150), nullable=False)

    departement = Relationship("Departement", back_populates="professeurs")
    examens = Relationship("Examen", back_populates="professeur")


class LieuExamen(Base):
    __tablename__ = "lieu_examen"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    capacite = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)  # amphi / salle / labo
    batiment = Column(String(100), nullable=False)

    examens = Relationship("Examen", back_populates="salle")

    __table_args__ = (
        CheckConstraint("capacite > 0", name="check_capacite_positive"),
    )

class Inscription(Base):
    __tablename__ = "inscriptions"

    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)
    note = Column(Integer, nullable=True)

    etudiant = Relationship("Etudiant", back_populates="inscriptions")
    module = Relationship("Module", back_populates="inscriptions")


class Examen(Base):
    __tablename__ = "examens"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    prof_id = Column(Integer, ForeignKey("professeurs.id"), nullable=False)
    salle_id = Column(Integer, ForeignKey("lieu_examen.id"), nullable=False)

    date_heure = Column(DateTime, nullable=False)
    duree_minutes = Column(Integer, nullable=False)

    module = Relationship("Module", back_populates="examens")
    professeur = Relationship("Professeur", back_populates="examens")
    salle = Relationship("LieuExamen", back_populates="examens")

    __table_args__ = (
        CheckConstraint("duree_minutes > 0", name="check_duree_positive"),
    )
