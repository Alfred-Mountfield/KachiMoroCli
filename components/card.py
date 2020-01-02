from abc import ABC, abstractmethod


class Card(ABC):
    def __init__(self, name: str, color: str, cost: int, rolls_active: list, effect: str, symbol: str):
        self.name = name
        self.color = color
        self.cost = cost
        self.rolls_active = rolls_active
        self.effect = effect
        self.symbol = symbol

    # @abstractmethod
    # def on_activate(self):
    #     pass


class WheatField(Card):
    def __init__(self):
        super().__init__(name="Wheat Field", color="blue", cost=1, rolls_active=[1], effect="Get 1 coin from the bank, on anyone's turn",
                         symbol="wheat")


class Ranch(Card):
    def __init__(self):
        super().__init__(name="Ranch", color="blue", cost=1, rolls_active=[2], effect="Get 1 coin from the bank, on anyone's turn",
                         symbol="cow")


class Bakery(Card):
    def __init__(self):
        super().__init__(name="Bakery", color="green", cost=1, rolls_active=[2, 3], effect="Get 1 coin from the bank, on your turn only",
                         symbol="bread")


class Cafe(Card):
    def __init__(self):
        super().__init__(name="Cafe", color="red", cost=2, rolls_active=[3], effect="Get 1 coin from the player who rolled the dice",
                         symbol="cup")


class ConvenienceStore(Card):
    def __init__(self):
        super().__init__(name="Convenience Store", color="green", cost=2, rolls_active=[4], effect="Get 3 coins from the bank, on your turn"
                                                                                                   " only",
                         symbol="bread")


class Forest(Card):
    def __init__(self):
        super().__init__(name="Forest", color="blue", cost=3, rolls_active=[5], effect="Get 1 coin from the bank, on anyone's turn",
                         symbol="cog")


class Stadium(Card):
    def __init__(self):
        super().__init__(name="Stadium", color="purple", cost=6, rolls_active=[6], effect="Get 2 coins from all players, on your turn only",
                         symbol="tower")


class TvStation(Card):
    def __init__(self):
        super().__init__(name="TV Station", color="purple", cost=7, rolls_active=[6], effect="Take 5 coins from any one player, on your "
                                                                                             "turn only",
                         symbol="tower")


class BusinessCenter(Card):
    def __init__(self):
        super().__init__(name="Business Center", color="purple", cost=8, rolls_active=[6], effect="Trade one non 'tower' establishment with"
                                                                                                  " another player, on your turn only",
                         symbol="tower")


class CheeseFactory(Card):
    def __init__(self):
        super().__init__(name="Cheese Factory", color="green", cost=5, rolls_active=[7], effect="Get 3 coins from the bank for each 'cow' "
                                                                                                "establishment that you own, on your turn "
                                                                                                "only",
                         symbol="factory")


class FurnitureFactory(Card):
    def __init__(self):
        super().__init__(name="Furniture Factory", color="green", cost=3, rolls_active=[8], effect="Get 3 coins from the bank for each "
                                                                                                   "'cog' establishment that you own, "
                                                                                                   "on your turn only",
                         symbol="factory")


class Mine(Card):
    def __init__(self):
        super().__init__(name="Mine", color="blue", cost=6, rolls_active=[9], effect="Get 5 coins from the bank, on anyone's turn",
                         symbol="cog")


class FamilyRestaurant(Card):
    def __init__(self):
        super().__init__(name="Family Restaurant", color="red", cost=3, rolls_active=[9, 10], effect="Get 2 coins from the player who "
                                                                                                     "rolled the dice",
                         symbol="cup")


class AppleOrchard(Card):
    def __init__(self):
        super().__init__(name="AppleOrchard", color="blue", cost=3, rolls_active=[10], effect="Get 3 coins from the bank, "
                                                                                              "on anyone's turn",
                         symbol="wheat")


class FruitAndVegetableMarket(Card):
    def __init__(self):
        super().__init__(name="Fruit and Vegetable Market", color="green", cost=2, rolls_active=[11, 12], effect="Get 3 coins from te "
                                                                                                                 "bank, on anyone's turn",
                         symbol="scale")
