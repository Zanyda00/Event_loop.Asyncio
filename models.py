import os

from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_DB = os.getenv("PG_DB", "asyncio")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5431")

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}: {PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN)
Session = sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=engine)

Base = declarative_base()


class SwapiPeople(Base):

    __tablename__ = "swapi_people"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    birth_year = Column(String, index=True)
    eye_color = Column(String, index=True)
    films = Column(String, index=True)
    gender = Column(String, index=True)
    hair_color = Column(String, index=True)
    height = Column(String, index=True)
    homeworld = Column(String, index=True)
    mass = Column(String, index=True)
    skin_color = Column(String, index=True)
    species = Column(String, index=True)
    starships = Column(String, index=True)
    vehicles = Column(String, index=True)