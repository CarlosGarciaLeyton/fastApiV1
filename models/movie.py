from bd.database import Base
from sqlalchemy import Column, Integer, String, Float


class Movie (Base):
    __tablename__ ='Movies'
    id= Column(Integer, primary_key=True)
    title =Column(String)
    overview = Column(String)
    year = Column(String)
    rating = Column(Float)
    category= Column(String)

    