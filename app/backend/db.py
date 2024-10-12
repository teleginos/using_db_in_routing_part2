from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///taskmanager.db", echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
