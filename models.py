from sqlalchemy import Column, Integer, String, ARRAY, Float, TIMESTAMP
from database import Base

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    #created_at= Column(ARRAY, nullable=False)
