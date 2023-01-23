from baseplayer import BasePlayer
from functions import *


class Player(BasePlayer):
    def __init__(self, name: str, chips: int, min_bet, player=None):
        super().__init__()
        self.name = name
        self.chips = chips
        self.bet = 0
        self.round_over = False
        self.splitFrom = player
        self.min_bet = min_bet

    def __str__(self):
        return f"Player {self.name}"


    def is_game_over(self) -> bool:
        if self.chips <= 0 or self.chips < self.min_bet:
            return True
        else:
            return False

    def set_round_over(self, over: bool):
        if over:
            self.round_over = True
        elif not over:
            self.round_over = False

    def round_reset(self):
        self.hand.clear()
        self.bet = 0
        if self.is_game_over():
            print(f"{self.name} is GAME OVER. Not enough Chips - Sorry")
        else:
            self.set_round_over(False)
            if self.splitFrom is not None:
                self.splitFrom.chips += int(self.chips)

    def place_bet(self):
        print(f"{self.name}\'s turn. You\'ve got {self.chips} Chips left.")
        bet = input_int(f"Place bet ({self.min_bet} Chips minimum): ", self.min_bet, self.chips)
        self.bet = bet
        print(f"{bet} Chips bet. {self.chips - bet} Chips left.")

    def double(self):
        self.bet *= 2
        print(f"Bet is doubled to {self.bet}. Good luck!")

    def is_pair(self) -> bool:
        return self.hand[0] == self.hand[1]

    def set_condition(self, condition: str):
        if not self.round_over:
            if condition == "blackjack":
                self.chips += int(self.bet * 1.5)
                print(f"{self.name}: Blackjack!!")
            elif condition == "win":
                self.chips += int(self.bet * 2)
                print(f"{self.name}: Win!!")
            elif condition == "lose":
                self.chips -= int(self.bet)
                print(f"{self.name}: Oh no, maybe next time.")
            elif condition == "tie":
                print(f"{self.name}: Tie.")
            self.set_round_over(True)
