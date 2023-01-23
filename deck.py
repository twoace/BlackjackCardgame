import random
from card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        if len(self.cards) > 0:
            self.cards.clear()
        cards = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "Bube": 10,
            "Dame": 10,
            "König": 10,
            "Ass": 11
        }
        colors = ["Herz", "Kreuz", "Pik", "Karo"]
        for color in colors:
            for key in cards:
                self.cards.append(Card(key, color, cards[key]))
        random.shuffle(self.cards)

    def draw_card(self, num):
        lst = []
        for _ in range(num):
            lst.append(self.cards.pop())
        return lst
