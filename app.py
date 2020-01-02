from random import randint

from components.player import Player


def parse_yes_no_input(query: str):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    while True:
        print(query)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes', 'no', 'y' or 'n'")


def parse_buy(active_player: Player):
    valid = ["WheatField", "Ranch", "Bakery", "Cafe", "ConvenienceStore", "Forest", "Stadium", "TvStation", "BusinessCentre",
             "CheeseFactory", "FurnitureFactory", "Mine", "FamilyRestaurant", "AppleOrchard", "FruitAndVegMarket", "Nothing"]

    while True:
        print("Do you wish to buy an establishment")
        choice = input().lower()
        if choice in "Nothing":
            pass
        elif choice in valid:
            # check the wallet of the player
            # buy the property
            pass
        else:
            print(f"Please respond with an establishment in the list: {''.join(valid)}")


def roll_dice(two_dice=False):
    if not two_dice:
        return randint(0, 6)
    else:
        return randint(0, 12)


def setup_game():
    pass


def run_game(num_of_players):
    setup_game()
    turn = 0
    active_player = 0
    players = []

    for ind in num_of_players:
        players.append(Player())

    # game loop
    while True:
        turn += 1
        active_player += 1
        print(f"It's player {active_player + 1}'s turn")
        # if possible
        two_dice = parse_yes_no_input("Do you want to roll with two dice?")

        roll = roll_dice(two_dice)
        print(f"Rolled: {roll}")

        for ind in range(num_of_players):
            player_ind = (ind + active_player) % 4

            for card in players[player_ind].cards:
                pass

        parse_buy(players[active_player])


def main():
    cards = {
        "WheatField": 6,
        "Ranch": 6,
        "Bakery": 6,
        "Cafe": 6,
        "ConvenienceStore": 6,
        "Forest": 6,
        "Stadium": 6,
        "TvStation": 6,
        "BusinessCentre": 6,
        "CheeseFactory": 6,
        "FurnitureFactory": 6,
        "Mine": 6,
        "FamilyRestaurant": 6,
        "AppleOrchard": 6,
        "FruitAndVegMarket": 6,
    }


if __name__ == "__main__":
    main()
