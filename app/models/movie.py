from sqlalchemy import Column, Integer, String, Float, orm

from app.bd.database import Base



class Movie (Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview =Column(String)
    year = Column(String)
    rating = Column(Float)
    category= Column(String)



