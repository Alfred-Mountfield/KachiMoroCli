import curses
import curses.panel
from curses.textpad import rectangle, Textbox
from random import randint

from components.player import Player
from components.card import WheatField, Ranch, Bakery, Cafe, ConvenienceStore, Forest, Stadium, TvStation, BusinessCenter, CheeseFactory,\
    FurnitureFactory, Mine, FamilyRestaurant, AppleOrchard, FruitAndVegetableMarket
from components.shop import Shop


class GameStateUi:
    def __init__(self, stdscr, players):
        self.stdscr = stdscr

        curses.start_color()
        curses.noecho()

        # player boxes
        player_panel_h = int(curses.LINES/2)
        player_panel_w = int(curses.COLS/len(players))
        self.player_text_boxes = []
        for player_ind in range(len(players)):
            rectangle(stdscr, 0, (player_ind * player_panel_w), player_panel_h, ((player_ind + 1) * player_panel_w))
            new_win = curses.newwin(player_panel_h-2, player_panel_w-2, 1, player_panel_w*player_ind + 1)
            new_panel = curses.panel.new_panel(new_win)

            self.player_text_boxes.append((new_win, new_panel))

        # output box
        rectangle(stdscr, player_panel_h + 1, 0, curses.LINES - 5, curses.COLS - player_panel_w - 1)
        out_win = curses.newwin(player_panel_h - 7, (curses.COLS - player_panel_w - 2), (player_panel_h + 2), 1)
        out_win.scrollok(True)
        out_win.idlok(True)
        out_panel = curses.panel.new_panel(out_win)
        self.out_panel = (out_win, out_panel)

        # shop box
        rectangle(stdscr, player_panel_h + 1, curses.COLS - player_panel_w - 1, curses.LINES - 5, curses.COLS - 1)
        shop_win = curses.newwin(player_panel_h - 7, player_panel_w - 1, player_panel_h + 2, curses.COLS - player_panel_w)
        shop_panel = curses.panel.new_panel(shop_win)
        shop_win.addstr(0, 0, f'Shop:')

        self.shop_panel = (shop_win, shop_panel)

        curses.panel.update_panels()

        # input box
        rectangle(stdscr, curses.LINES - 4, 0, curses.LINES - 2, curses.COLS - 1)
        curses.panel.update_panels()
        in_win = curses.newwin(2, curses.COLS-1, curses.LINES - 3, 1)
        in_text_box = Textbox(in_win)

        self.in_box = (in_win, in_text_box)

        stdscr.refresh()


def update_board(players: list, active_player_ind: int, state: GameStateUi, shop: Shop):
    for ind, player in enumerate(players):
        text_box = state.player_text_boxes[ind][0]
        text_box.clear()
        text_box.addstr(f"Player {ind + 1} - {player.wallet} coins:\n\n")
        for card in player.cards:
            if player.cards[card] > 0:
                card_obj = card()
                rolls_active = ' - '.join(map(str, card_obj.rolls_active))
                text_box.addstr(f"  {rolls_active.center(9)}  {card_obj.name} x{player.cards[card]} \n")

        text_box.addstr("\n\n")

        for landmark in player.landmarks:
            text_box.addstr(f"  {landmark}: {'Bought' if player.landmarks[landmark][0] else 'Not Bought'} \n")

    text_box = state.shop_panel[0]
    text_box.clear()
    text_box.addstr(f"Shop:\n\n")
    for card in shop.inventory:
        card_obj = card()
        rolls_active = ' - '.join(map(str, card_obj.rolls_active))
        text_box.addstr(f"  [{card_obj.cost} Coins]  {rolls_active.center(9)}  {card_obj.name} x{shop.inventory[card]} \n")

    for landmark in players[active_player_ind].landmarks:
        if not players[active_player_ind].landmarks[landmark][0]:
            cost = players[active_player_ind].landmarks[landmark][1]
            text_box.addstr(f"  [{cost} Coins]".ljust(24) + f"{landmark}\n")


def write_message(msg: str, state: GameStateUi):
    state.out_panel[0].addstr(msg + "\n")
    curses.panel.update_panels()
    state.stdscr.refresh()


def get_input(state: GameStateUi) -> str:
    def enter_is_terminate(x):
        if x == 10:
            return 7
        else:
            return x

    state.in_box[1].edit(enter_is_terminate)
    choice = state.in_box[1].gather().strip()
    state.in_box[0].clear()
    return choice


def parse_yes_no_input(query: str, state: GameStateUi):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    while True:
        write_message(query, state)
        choice = get_input(state)

        if choice.lower() in valid:
            return valid[choice.lower()]
        else:
            write_message(f"Please respond with 'yes', 'no', 'y' or 'n', you entered: \n{choice}", state)


def parse_buy(active_player: Player, state: GameStateUi, shop: Shop):
    valid_establishments = ["Wheat Field", "Ranch", "Bakery", "Cafe", "Convenience Store", "Forest", "Stadium", "TV Station",
                            "Business Center", "Cheese Factory", "Furniture Factory", "Mine", "Family Restaurant", "Apple Orchard",
                            "Fruit And Vegetable Market", "Nothing"]
    valid_landmarks = [x for x in active_player.landmarks if not active_player.landmarks[x][0]]

    while True:
        write_message("What establishment or landmark do you want to buy?", state)
        write_message(f"Your options are: {', '.join(valid_establishments + valid_landmarks)}", state)
        choice = get_input(state)

        if choice.lower() in "nothing":
            write_message(f"Choosing not to buy an establishment", state)
            break
        elif choice.lower() in [x.lower() for x in valid_establishments]:
            chosen_establishment = establishment_str_to_obj(choice.lower())
            if active_player.wallet >= chosen_establishment.cost:
                if shop.inventory[type(chosen_establishment)] > 0:
                    if not active_player.cards[type(chosen_establishment)] or chosen_establishment.symbol != "tower":
                        write_message(f"Buying establishment: {chosen_establishment.name} for {chosen_establishment.cost} coins ", state)
                        active_player.wallet -= chosen_establishment.cost
                        active_player.cards[type(chosen_establishment)] += 1
                        shop.inventory[type(chosen_establishment)] -= 1
                        break
                    else:
                        write_message(f"You already have a {chosen_establishment.name()}, choose a different establishment or landmark", state)
                else:
                    write_message(f"There aren't any {chosen_establishment.name}'s left in the shop", state)
            else:
                write_message(f"Not enough money to buy a {choice}, please choose a different establishment or landmark", state)

        elif choice.lower() in [x.lower() for x in valid_landmarks]:
            # find the capitalised name
            for landmark in valid_landmarks:
                if choice.lower() == landmark.lower():
                    chosen_landmark = landmark

            if active_player.wallet >= active_player.landmarks[chosen_landmark][1]:
                write_message(f"Buying landmark: {chosen_landmark} for {active_player.landmarks[chosen_landmark][1]} coins ", state)
                active_player.wallet -= active_player.landmarks[chosen_landmark][1]
                active_player.landmarks[chosen_landmark] = (True, active_player.landmarks[chosen_landmark][1])
                break

            else:
                write_message(f"Not enough money to buy {chosen_landmark}, please choose a different establishment or landmark", state)
        else:
            write_message(f"Please respond with an establishment or landmark in the list: {', '.join(valid_establishments + valid_landmarks)}", state)


def establishment_str_to_obj(establishment_str: str):
    establishments = {
        "wheat field": WheatField(),
        "ranch": Ranch(),
        "bakery": Bakery(),
        "cafe": Cafe(),
        "convenience store": ConvenienceStore(),
        "forest": Forest(),
        "stadium": Stadium(),
        "tv station": TvStation(),
        "business center": BusinessCenter(),
        "cheese factory": CheeseFactory(),
        "furniture factory": FurnitureFactory(),
        "mine": Mine(),
        "family restaurant": FamilyRestaurant(),
        "apple orchard": AppleOrchard(),
        "fruit and vegetable market": FruitAndVegetableMarket(),
    }
    try:
        return establishments[establishment_str.lower()]
    except KeyError as e:
        raise ValueError("Unexpected type of establishment")


def roll_dice(two_dice=False):
    if not two_dice:
        return randint(1, 6), 0
    else:
        return randint(1, 6), randint(1, 6)


def run_game(num_of_players, stdscr):
    turn = 1
    active_player = 0
    players = []

    for _ in range(num_of_players):
        players.append(Player())

    state = GameStateUi(stdscr, players)
    shop = Shop()
    update_board(players, active_player, state, shop)

    # game loop
    while True:
        curses.panel.update_panels()
        write_message(f"\nIt's player {active_player + 1}'s turn", state)
        two_dice = parse_yes_no_input("Do you want to roll with two dice?", state) if players[active_player].landmarks["Train Station"][0] \
            else False

        rolls = roll_dice(two_dice)
        roll = rolls[0] + rolls[1]
        write_message(f"Rolled: {rolls[0]}, {rolls[1]}", state) if rolls[1] else write_message(f"Rolled: {rolls[0]}", state)

        if players[active_player].landmarks['Radio Tower'][0]:
            if parse_yes_no_input("Do you want to roll again?", state):
                rolls = roll_dice(two_dice)
                roll = rolls[0] + rolls[1]
                write_message(f"Rolled: {rolls[0]}, {rolls[1]}", state) if rolls[1] else write_message(f"Rolled: {rolls[0]}", state)


        for ind in range(num_of_players):
            player_ind = (ind + active_player + 1) % 4

            for card in players[player_ind].cards:
                card_obj = card()
                if roll in card_obj.rolls_active and (card_obj.active_on_others_turns or player_ind == active_player):
                    for num_of_cards in range(players[player_ind].cards[card]):
                        card_obj.on_activate(players=players, card_owner_ind=player_ind, active_player_ind=active_player, state=state)

        update_board(players, active_player, state, shop)
        parse_buy(players[active_player], state, shop)
        update_board(players, active_player, state, shop)

        if len([x for x in players[active_player].landmarks if players[active_player].landmarks[x][0]]) == 4:
            write_message(f"Player {active_player + 1} wins the game!", state)
            write_message(f"Type yes to end the game", state)

            while get_input(state).lower() not in ["yes", 'y']:
                pass

            break

        turn += 1
        if not (rolls[0] == rolls[1] and players[active_player].landmarks['Amusement Park'][0]):
            active_player = (active_player + 1) % 4
        else:
            write_message(f"You rolled doubles this turn and own the Amusement Park! Have another", state)


def main(stdscr):
    run_game(4, stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
