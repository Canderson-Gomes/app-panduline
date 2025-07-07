import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# NO RENDE : DataBase-panduLine;
#HOST: dpg-d1he362dbo4c73da8iog-a.oregon-postgres.render.com
#PORT: 5432
#DATABASE: pessoa_desaparecidas
#USERNAME: cggomes
#PASSWORD: nE3cRJBtkPnKDOoDbl7imSjArThmzv42

#EXTERNAL_URL: postgresql://cggomes:nE3cRJBtkPnKDOoDbl7imSjArThmzv42@dpg-d1he362dbo4c73da8iog-a.oregon-postgres.render.com/pessoa_desaparecidas
