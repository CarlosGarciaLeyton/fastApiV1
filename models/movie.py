from bd.database import Base

from sqlalchemy import Column, Integer, String, Float, orm



class Movie (Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = orm.Mapped[Column(String)]
    overview =orm.Mapped[ Column(String)]
    year = orm.Mapped[Column(String)]
    rating = orm.Mapped[Column(Float)]
    category= orm.Mapped[Column(String)]



