from dataclasses import dataclass
from datetime import date

@dataclass
class Actor:
    ActorID: int
    Name: str
    birth_date: date

    def __hash__(self):
        return hash(self.ActorID)

    def __str__(self):
        return f"{self.Name}"