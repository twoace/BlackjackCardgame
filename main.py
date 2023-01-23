from functions import *
from settings import *
import start_game

if __name__ == '__main__':
    running = True
    start_chips = START_CHIPS
    min_bet = MIN_BET
    player_num = PLAYER_NUM
    while running:
        choice = main_menu()
        if choice == 1:
            start_game.run(start_chips, min_bet, player_num)
        elif choice == 2:
            start_chips, min_bet, player_num = settings_menu()
            continue
        elif choice == 3:
            running = False
