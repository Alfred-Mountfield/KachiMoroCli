import curses
import curses.panel
from curses.textpad import rectangle, Textbox
from random import randint

from components.player import Player


class GameStateUi:
    def __init__(self, stdscr, num_of_players):
        self.stdscr = stdscr

        curses.start_color()
        curses.noecho()

        player_panel_h = int(curses.LINES/2)
        player_panel_w = int(curses.COLS/num_of_players)
        self.player_text_boxes = []
        for player_ind in range(num_of_players):
            rectangle(stdscr, 0, (player_ind * player_panel_w), player_panel_h, ((player_ind + 1) * player_panel_w))
            new_win = curses.newwin(player_panel_h-2, player_panel_w-2, 1, player_panel_w*player_ind + 1)
            new_panel = curses.panel.new_panel(new_win)
            new_win.addstr(0, 0, f'Player {player_ind + 1}')
            self.player_text_boxes.append((new_win, new_panel))

        # output box
        rectangle(stdscr, player_panel_h + 1, 0, curses.LINES - 5, curses.COLS - 1)
        out_win = curses.newwin(player_panel_h - 7, curses.COLS - 2, (player_panel_h + 2), 1)
        out_win.scrollok(True)
        out_win.idlok(True)
        out_panel = curses.panel.new_panel(out_win)
        self.out_panel = (out_win, out_panel)

        curses.panel.update_panels()

        # input box
        rectangle(stdscr, curses.LINES - 4, 0, curses.LINES - 2, curses.COLS - 1)
        curses.panel.update_panels()
        in_win = curses.newwin(2, curses.COLS-1, curses.LINES - 3, 1)
        in_text_box = Textbox(in_win)

        self.in_box = (in_win, in_text_box)

        stdscr.refresh()


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


def parse_buy(active_player: Player, state: GameStateUi):
    valid = ["Wheat Field", "Ranch", "Bakery", "Cafe", "Convenience Store", "Forest", "Stadium", "TV Station", "Business Centre",
             "Cheese Factory", "Furniture Factory", "Mine", "Family Restaurant", "Apple Orchard", "Fruit And Veg Market", "Nothing"]

    while True:
        write_message("What establishment do you want to buy?", state)
        write_message(f"Your options are: {', '.join(valid)}", state)
        choice = get_input(state)

        if choice.lower() in "nothing":
            write_message(f"Choosing not to buy an establishment: {choice}", state)
            break
        elif choice.lower() in [x.lower() for x in valid]:
            # check the wallet of the player
            # buy the property
            write_message(f"Buying establishment: {choice}", state)
            break
        else:
            write_message(f"Please respond with an establishment in the list: {', '.join(valid)}", state)


def roll_dice(two_dice=False):
    if not two_dice:
        return randint(0, 6)
    else:
        return randint(0, 12)


def run_game(num_of_players, stdscr):
    game_ui = GameStateUi(stdscr, num_of_players)
    turn = 1
    active_player = 0
    players = []

    for _ in range(num_of_players):
        players.append(Player())

    # game loop
    while True:

        write_message(f"It's player {active_player + 1}'s turn", game_ui)
        # if possible
        two_dice = parse_yes_no_input("Do you want to roll with two dice?", game_ui)

        roll = roll_dice(two_dice)
        write_message(f"Rolled: {roll}", game_ui)

        for ind in range(num_of_players):
            player_ind = (ind + active_player) % 4

            for card in players[player_ind].cards:
                if roll in card.rolls_active:
                    # card.on_activate()
                    pass

        parse_buy(players[active_player], game_ui)

        turn += 1
        active_player += 1


def main(stdscr):
    run_game(4, stdscr)
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
    curses.wrapper(main)
