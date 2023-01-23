from functions import *
from game import Game
from settings import *


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
