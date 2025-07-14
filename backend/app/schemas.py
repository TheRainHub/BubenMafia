from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    games_played: int
    wins: int
    points: int

    class Config:
        orm_mode = True
