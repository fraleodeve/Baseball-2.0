from dataclasses import dataclass
from datetime import date

@dataclass
class Giocatore:
    playerID: str
    birthCountry: str
    birthCity: str
    deathCountry: str
    deathCity: str
    nameFirst: str
    nameLast: str
    weight: int
    height: int
    bats: str
    throws: str
    birth_date: date
    debut_date: date
    finalgame_date: date
    death_date: date

    def __hash__(self):
        return hash(self.playerID)

    def __eq__(self, other):
        return self.playerID == other.playerID

    def __str__(self):
        return self.nameFirst + " " + self.nameLast