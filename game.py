from deck import Deck
from dealer import Dealer
from player import Player
from functions import *


class Game:
    def __init__(self, start_chips, min_bet, player_num):
        self.deck = Deck()
        self.player = []
        self.dealer = Dealer()
        self.rounds = 0
        self.index = 0
        self.start_chips = start_chips
        self.min_bet = min_bet
        self.player_num = player_num

    def __iter__(self):
        return iter(self.player)

    def __next__(self):
        if self.index > len(self.player):
            raise StopIteration
        new_player = next(self)
        self.index += 1
        return new_player

    def player_alive(self):
        alive = []
        for player in self.player:
            if not player.round_over:
                alive.append(player)
        if len(alive) > 0:
            return True
        return False

    def reset(self):
        if len(self.player) > 0:
            self.player.clear()
        self.rounds = 0
        self.dealer.round_reset()
        self.deck.create_deck()

    def create_player(self):
        for i in range(self.player_num):
            name = input_str(f"Player {i + 1} Name: ")
            self.player.append(Player(name, self.start_chips, self.min_bet))

    def split(self, player):
        split = Player(f"{player.name}\'s splithand", player.bet, self.min_bet, player)
        pair_card = [player.hand.pop()]
        split.get_card(pair_card)
        split.get_card(self.deck.draw_card(1))
        self.player.insert(self.player.index(player) + 1, split)
        player.chips -= player.bet
        print("Hand splitted!")

    def add_round(self):
        self.rounds += 1

    def new_round(self):
        self.dealer.round_reset()
        self.deck.create_deck()
        go = []
        for player in self.player:
            player.round_reset()
            if player.is_game_over() or player.splitFrom is not None:
                go.append(player)
        for x in go:
            self.player.remove(x)
