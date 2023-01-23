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


def draw_lines():
    print("---------------------------")


def settings_menu():
    chips = input_int("Start chips (default: 1000): ", 2, 9999999)
    min = input_int("Minimum bet (default: 200): ", 1, chips * 1000)
    players = input_int("How many players (default: 1): ", 1, 99)
    return chips, min, players


def end_menu() -> int:
    print("1 - Next round")
    print("2 - Quit")
    c = input_int("Choose a number: ", 1, 2)
    return c


def main_menu() -> int:
    print("\nNew Game. Good luck!")
    draw_lines()
    print("1 - New Game")
    print("2 - Settings")
    print("3 - Quit")
    c = input_int("Choose a number: ", 1, 3)
    return c


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
