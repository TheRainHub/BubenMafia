from app.db import Base
from sqlalchemy import Column, Integer, String


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    games_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    points = Column(Integer, default=0)
