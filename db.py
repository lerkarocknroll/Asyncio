from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

PG_DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5431/netology_async'
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class PersonModel(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    person_id = Column(String, unique=True)
    birth_year = Column(String)
    eye_color = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    homeworld = Column(String)