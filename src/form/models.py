from pydantic import BaseModel
from enum import Enum

class Level(Enum):
  ONE = 1
  TWO = 2
  THREE = 3
  FOUR = 4
  FIVE = 5
  SIX = 6

class Question(BaseModel):
  question: str
  answer: Level