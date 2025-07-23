from enum import Enum


class GameRole(str, Enum):
    citizen = "Citizen"
    sheriff = "Sheriff"
    mafia = "Mafia"
    don = "Don"


class UserRole(str, Enum):
    organizer = "organizer"
    gm = "gm"
    player = "player"


class GameState(str, Enum):
    draft = "draft"
    live = "live"
    finished = "finished"
    aborted = "aborted"


class Condition(str, Enum):
    CITY_WIN = "CITY_WIN"
    MAFIA_WIN = "MAFIA_WIN"
    FIRST_NIGHT_KILLED = "FIRST_NIGHT_KILLED"
    BEST_MOVE_GUESS_DUO = "BEST_MOVE_GUESS_DUO"
    BEST_MOVE_GUESS_TRIO = "BEST_MOVE_GUESS_TRIO"
    BEST_MOVE_GUESS_DUO_SHERIFF = "BEST_MOVE_GUESS_DUO_SHERIFF"
    BEST_MOVE_GUESS_TRIO_SHERIFF = "BEST_MOVE_GUESS_TRIO_SHERIFF"
