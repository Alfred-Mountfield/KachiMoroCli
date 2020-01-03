from abc import ABC, abstractmethod


class Card(ABC):
    def __init__(self, name: str, color: str, cost: int, rolls_active: list, effect: str, symbol: str, active_on_others_turns: bool):
        self.name = name
        self.color = color
        self.cost = cost
        self.rolls_active = rolls_active
        self.effect = effect
        self.symbol = symbol
        self.active_on_others_turns = active_on_others_turns

    @abstractmethod
    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        pass


class WheatField(Card):
    def __init__(self):
        super().__init__(name="Wheat Field", color="blue", cost=1, rolls_active=[1], effect="Get 1 coin from the bank, on anyone's turn",
                         symbol="wheat", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        players[card_owner_ind].wallet += 1
        write_message(f"Player {card_owner_ind + 1} received 1 coin from the bank", state)


class Ranch(Card):
    def __init__(self):
        super().__init__(name="Ranch", color="blue", cost=1, rolls_active=[2], effect="Get 1 coin from the bank, on anyone's turn",
                         symbol="cow", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        players[card_owner_ind].wallet += 1
        write_message(f"Player {card_owner_ind + 1} received 1 coin from the bank", state)


class Bakery(Card):
    def __init__(self):
        super().__init__(name="Bakery", color="green", cost=1, rolls_active=[2, 3], effect="Get 1 coin from the bank, on your turn only",
                         symbol="bread", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        total = 2 if players[card_owner_ind].landmarks['Shopping Mall'][0] else 1
        players[card_owner_ind].wallet += total
        write_message(f"Player {card_owner_ind + 1} received {total} coin{'s' if total == 2 else ''} from the bank", state)


class Cafe(Card):
    def __init__(self):
        super().__init__(name="Cafe", color="red", cost=2, rolls_active=[3], effect="Get 1 coin from the player who rolled the dice",
                         symbol="cup", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        if players[active_player_ind].wallet > 0:
            total = min(players[active_player_ind].wallet, 2) if players[card_owner_ind].landmarks['Shopping Mall'][0] else 1
            players[active_player_ind].wallet -= total
            players[card_owner_ind].wallet += total
            write_message(f"Player {card_owner_ind + 1} received {total} coin{'s' if total == 2 else ''} from Player "
                          f"{active_player_ind + 1}", state)


class ConvenienceStore(Card):
    def __init__(self):
        super().__init__(name="Convenience Store", color="green", cost=2, rolls_active=[4], effect="Get 3 coins from the bank, on your turn"
                                                                                                   " only",
                         symbol="bread", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        total = 4 if players[card_owner_ind].landmarks['Shopping Mall'][0] else 3
        players[card_owner_ind].wallet += total
        write_message(f"Player {card_owner_ind + 1} received {total} coins from the bank", state)


class Forest(Card):
    def __init__(self):
        super().__init__(name="Forest", color="blue", cost=3, rolls_active=[5], effect="Get 1 coin from the bank, on anyone's turn",
                         symbol="cog", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        players[card_owner_ind].wallet += 1
        write_message(f"Player {card_owner_ind + 1} received 1 coin from the bank", state)


class Stadium(Card):
    def __init__(self):
        super().__init__(name="Stadium", color="purple", cost=6, rolls_active=[6], effect="Get 2 coins from all players, on your turn only",
                         symbol="tower", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        # loop through the other players
        for ind in range(len(players) - 1):
            player_ind = (ind + active_player_ind + 1) % 4

            total = min(players[player_ind].wallet, 2)
            players[card_owner_ind].wallet += total
            players[player_ind].wallet -= total

            if total:
                write_message(f"Player {card_owner_ind + 1} received {total} coins from Player {player_ind + 1}", state)


class TvStation(Card):
    def __init__(self):
        super().__init__(name="TV Station", color="purple", cost=7, rolls_active=[6], effect="Take 5 coins from any one player, on your "
                                                                                             "turn only",
                         symbol="tower", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message, get_input
        valid_player_nums = {"1": 0, "one": 0,
                             "2": 1, "two": 1,
                             "3": 2, "three": 2,
                             "4": 3, "four": 3}

        while True:
            write_message(f"What player do you want to take 5 coins from?", state)
            choice = get_input(state)

            # check it's a valid response
            if choice.lower() in valid_player_nums and valid_player_nums[choice.lower()] < len(players):
                ind = valid_player_nums[choice.lower()]

                total = min(players[ind].wallet, 5)
                players[card_owner_ind].wallet += total
                players[ind].wallet -= total

                if total:
                    write_message(f"Player {card_owner_ind + 1} received {total} coins from Player {ind + 1}", state)
                break

            else:
                write_message(f"Choice of '{choice}' is not valid, please write a number from 1 to {len(players)}", state)


class BusinessCenter(Card):
    def __init__(self):
        super().__init__(name="Business Center", color="purple", cost=8, rolls_active=[6], effect="Trade one non 'tower' establishment with"
                                                                                                  " another player, on your turn only",
                         symbol="tower", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message, get_input,establishment_str_to_obj
        valid_player_nums = {"1": 0, "one": 0,
                             "2": 1, "two": 1,
                             "3": 2, "three": 2,
                             "4": 3, "four": 3}

        while True:
            write_message(f"What player do you want to take an establishment from?", state)
            choice = get_input(state)

            # check it's a valid response
            if choice.lower() in valid_player_nums and valid_player_nums[choice.lower()] < len(players):
                ind = valid_player_nums[choice.lower()]
                valid_establishments = []

                for card in players[ind].cards:
                    if players[ind].cards[card] > 0:
                        card_obj = card()
                        if card_obj.symbol != "tower":
                            valid_establishments.append(card_obj.name)

                while True:
                    write_message(f"What non-tower establishment do you want to take?", state)
                    choice = get_input(state)

                    # check it's a valid response
                    if choice.lower() in valid_establishments:
                        card_obj = establishment_str_to_obj(choice)

                        players[card_owner_ind].cards[type(card_obj)] += 1
                        players[ind].cards[type(card_obj)] -= 1

                        write_message(f"Player {card_owner_ind + 1} received a {choice} from Player {ind + 1}", state)
                        break

                    else:
                        write_message(f"Player {ind + 1} does not have a '{choice}' or you cannot take it, please choose again", state)

                break

            else:
                write_message(f"Choice of '{choice}' is not valid, please write a number from 1 to {len(players)}", state)


class CheeseFactory(Card):
    def __init__(self):
        super().__init__(name="Cheese Factory", color="green", cost=5, rolls_active=[7], effect="Get 3 coins from the bank for each 'cow' "
                                                                                                "establishment that you own, on your turn "
                                                                                                "only",
                         symbol="factory", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        for card in players[card_owner_ind].cards:
            total = 0
            if card().symbol == 'cow':
                total += (3 * players[card_owner_ind].cards[card])

            players[card_owner_ind].wallet += total

            if total:
                write_message(f"Player {card_owner_ind + 1} received {total} coins from the bank", state)


class FurnitureFactory(Card):
    def __init__(self):
        super().__init__(name="Furniture Factory", color="green", cost=3, rolls_active=[8], effect="Get 3 coins from the bank for each "
                                                                                                   "'cog' establishment that you own, "
                                                                                                   "on your turn only",
                         symbol="factory", active_on_others_turns=False)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        for card in players[card_owner_ind].cards:
            total = 0
            if card().symbol == 'cog':
                total += (3 * players[card_owner_ind].cards[card])

            players[card_owner_ind].wallet += total
            if total:
                write_message(f"Player {card_owner_ind + 1} received {total} coins from the bank", state)


class Mine(Card):
    def __init__(self):
        super().__init__(name="Mine", color="blue", cost=6, rolls_active=[9], effect="Get 5 coins from the bank, on anyone's turn",
                         symbol="cog", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        players[card_owner_ind].wallet += 5
        write_message(f"Player {card_owner_ind + 1} received 5 coins from the bank", state)


class FamilyRestaurant(Card):
    def __init__(self):
        super().__init__(name="Family Restaurant", color="red", cost=3, rolls_active=[9, 10], effect="Get 2 coins from the player who "
                                                                                                     "rolled the dice",
                         symbol="cup", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        total = min(players[active_player_ind].wallet, 3) if players[card_owner_ind].landmarks['Shopping Mall'][0] \
            else min(players[active_player_ind].wallet, 2)
        players[card_owner_ind].wallet += total
        players[active_player_ind].wallet -= total

        if total:
            write_message(f"Player {card_owner_ind + 1} received {total} coins from Player {active_player_ind + 1}", state)


class AppleOrchard(Card):
    def __init__(self):
        super().__init__(name="AppleOrchard", color="blue", cost=3, rolls_active=[10], effect="Get 3 coins from the bank, "
                                                                                              "on anyone's turn",
                         symbol="wheat", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        players[card_owner_ind].wallet += 3
        write_message(f"Player {card_owner_ind + 1} received 3 coins from the bank", state)


class FruitAndVegetableMarket(Card):
    def __init__(self):
        super().__init__(name="Fruit and Vegetable Market", color="green", cost=2, rolls_active=[11, 12], effect="Get 3 coins from te "
                                                                                                                 "bank, on anyone's turn",
                         symbol="scale", active_on_others_turns=True)

    def on_activate(self, players: list, card_owner_ind: int, active_player_ind: int, state):
        from app import write_message
        players[card_owner_ind].wallet += 3
        write_message(f"Player {card_owner_ind + 1} received 3 coins from the bank", state)
