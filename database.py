from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import  sessionmaker

SQLALCHEMY_DATABASE_URL =  "mysql+pymysql://root:omffmvoFSchAVPwAAPebdAJssbZRqXmK@crossover.proxy.rlwy.net:13114/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,          
    pool_pre_ping=True
    )

SessionLocal = sessionmaker(bind= engine , autoflush=False , autocommit= False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

