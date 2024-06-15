from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


# Модель базы данных для приложения.

class Meme(BaseModel):
    id: int
    image_url: str
    text: str


class MemeImage(Base):
    __tablename__ = 'meme_images'
    id = Column(Integer, primary_key=True, index=True)
    meme_id = Column(Integer, ForeignKey('memes.id'))
    image_url = Column(String)
    meme = relationship("Meme", back_populates="images")
