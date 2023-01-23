from dataclasses import dataclass


@dataclass
class Card:
    name: str
    color: str
    value: int

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.name == other.name