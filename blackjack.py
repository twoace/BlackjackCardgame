import random
from dataclasses import dataclass

START_CHIPS = 1000
PLAYER_NUM = 1
MIN_BET = 200


# Funktionen:
# Input Nummer validieren
def input_int(text: str, from_range: int, to_range: int) -> int:
    while True:
        i = input(text)
        try:
            i = int(i)
        except ValueError:
            print("This is not a number.")
            continue
        if from_range <= i <= to_range:
            break
        else:
            print("Invalid number.")
    return i


# Input String validieren
def input_str(text: str) -> str:
    i = ""
    while True:
        try:
            i = input(text)
        except ValueError:
            print("This is not a string.")
            continue
        if i is not None:
            break
    return i


# Linien erstellen
def draw_lines():
    print("-" * 20)


# Settings Menü
def settings_menu():
    chips = input_int("Start chips (default: 1000): ", 2, 9999999)
    min = input_int("Minimum bet (default: 200): ", 1, chips * 1000)
    players = input_int("How many players (default: 1): ", 1, 99)
    return chips, min, players


# Menü nach jeder Runde
def end_menu() -> int:
    print("1 - Next round")
    print("2 - Quit")
    c = input_int("Choose a number: ", 1, 2)
    return c


# Hauptmenü
def main_menu() -> int:
    print("\nNew Game. Good luck!")
    draw_lines()
    print("1 - New Game")
    print("2 - Settings")
    print("3 - Quit")
    c = input_int("Choose a number: ", 1, 3)
    return c


# Menü für Spielzug pro Spieler
def turn_menu(player) -> int:
    x = 0
    y = 0
    print("1 - Draw card")
    print("2 - Stay")
    if len(player.hand) <= 2:
        if player.chips > 2 * player.bet:
            print("3 - Double")
            x += 1
            if player.is_pair():
                print("4 - Split")
                x += 1
    c = input_int("Choose a number: ", 1, 2 + x)
    return c


# Kartenwerte der übergebenen Hand berechnen
def hand_value(hand) -> int:
    points = 0
    ace = False
    for card in hand:
        points += card.value
        if card.name == "Ass":
            ace = True
    if points > 21 and ace:
        points -= 10
    return points


# Klassen:
# Abstrakte Klasse der Spielteilnehmer
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


# Dealer Klasse
class Dealer(BasePlayer):

    def __str__(self):
        return "Dealer"


# Spieler Klasse
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


# Kartendeck Klasse
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


# Karten Klasse
@dataclass
class Card:
    name: str
    color: str
    value: int

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.name == other.name


# Spiel Klasse
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


# Spielablauf:
# Funktion für den Spielablauf
def run(start_chips, min_bet, player_num):
    game = Game(start_chips, min_bet, player_num)
    # New player
    if game.rounds == 0:
        game.create_player()

    game_loop = True
    while game_loop:
        # Add round
        game.add_round()
        print(f"ROUND {game.rounds}")

        # Place bets
        for player in game:
            player.place_bet()

        # Draw Cards
        game.dealer.get_card(game.deck.draw_card(1))
        for player in game:
            player.get_card(game.deck.draw_card(2))

        # Show things
        draw_lines()
        print(f"Dealer Hand: {game.dealer.show_hand()}")

        # Player turn
        for player in game:
            print(f"{player.name}\'s turn.")
            print(f"Your Hand: {player.show_hand()}")
            if hand_value(player.hand) == 21:
                player.set_condition("blackjack")
            else:
                c = turn_menu(player)
                if c == 2:
                    continue
                if c == 3:
                    player.double()
                    player.get_card(game.deck.draw_card(1))
                    print(f"Your Hand: {player.show_hand()}")
                    if hand_value(player.hand) > 21:
                        player.set_condition("lose")
                    continue
                if c == 4:
                    game.split(player)
                    c = 1
                if c == 1:
                    while c == 1:
                        player.get_card(game.deck.draw_card(1))
                        print(f"Your Hand: {player.show_hand()}")
                        if hand_value(player.hand) > 21:
                            player.set_condition("lose")
                            break
                        c = turn_menu(player)

        # Dealer draw
        draw_lines()
        if game.player_alive():
            while hand_value(game.dealer.hand) < 17:
                game.dealer.get_card(game.deck.draw_card(1))
            print(f"Dealer Hand: {game.dealer.show_hand()}")
            if hand_value(game.dealer.hand) > 21:
                print("The dealer got over 21.")
                for player in game:
                    player.set_condition("win")
            else:
                for player in game:
                    if hand_value(player.hand) > hand_value(game.dealer.hand):
                        player.set_condition("win")
                    elif hand_value(player.hand) < hand_value(game.dealer.hand):
                        player.set_condition("lose")
                    else:
                        player.set_condition("tie")
        input("Press Enter to continue...")

        # Reset round
        game.new_round()

        # Game over?
        if len(game.player) <= 0:
            print("GAME OVER")
            draw_lines()
            game.reset()
            game_loop = False
        else:
            c = end_menu()
            if c == 1:
                print("NEW ROUND")
                draw_lines()
            if c == 2:
                print("GAME OVER")
                draw_lines()
                game.reset()
                game_loop = False


# Ausführung
if __name__ == '__main__':
    running = True
    start_chips = START_CHIPS
    min_bet = MIN_BET
    player_num = PLAYER_NUM
    while running:
        choice = main_menu()
        if choice == 1:
            run(start_chips, min_bet, player_num)
        elif choice == 2:
            start_chips, min_bet, player_num = settings_menu()
            continue
        elif choice == 3:
            running = False
