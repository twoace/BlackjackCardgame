class BasePlayer:

    def __init__(self):
        self.hand = []

    def get_card(self, cards):
        for card in cards:
            self.hand.append(card)

    def show_hand(self) -> str:
        out = ""
        for i, card in enumerate(self.hand):
            out += str(card.name + " " + card.color)
            if i < len(self.hand) - 1:
                out += ", "
        return out

    def round_reset(self):
        self.hand.clear()

