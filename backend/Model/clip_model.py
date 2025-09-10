
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Clip(Base):
    __tablename__ = "clips"

    id_clip = Column(Integer, primary_key=True, autoincrement=True) 
    clip_url = Column(String) 
    broadcaster_id = Column(String) 
    broadcaster_name = Column(String) 
    creator_id  = Column(String) 
    creator_name = Column(String) 
    video_id = Column(String) 
    game_id = Column(String) 
    clip_language = Column(String) 
    date_creation = Column(String) 
    thumbnail_url = Column(String) 
    duration = Column(Float) 
   