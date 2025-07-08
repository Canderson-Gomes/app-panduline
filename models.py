from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    embedding = Column(ARRAY(Float))
    #created_at= Column(ARRAY, nullable=False)
