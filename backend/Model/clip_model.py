
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from database import Base


class Clip(Base):
    __tablename__ = "clips"

    id_clip = Column(Integer, primary_key=True, autoincrement=True) 
    blob_name = Column(String) 
    broadcaster_id = Column(String) 
    broadcaster_name = Column(String) 
    creator_id  = Column(String) 
    creator_name = Column(String) 
    video_id = Column(String) 
    game_id = Column(String) 
    title = Column(String)
    clip_language = Column(String) 
    date_creation = Column(String) 
    thumbnail_url = Column(String) 
    duration = Column(Float)
    view_count = Column(Integer)
    user_id  = Column(Integer, ForeignKey("users.id_user"))
   