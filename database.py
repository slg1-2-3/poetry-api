from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from db_creds import cred

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{name}:{password}@{server}/{database}".format(name=cred.name,password = cred.password ,server = cred.server,database = cred.database)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

