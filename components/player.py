from components.card import WheatField, Ranch, Bakery, Cafe, ConvenienceStore, Forest, Stadium, TvStation, BusinessCenter, \
    CheeseFactory, FurnitureFactory, Mine, FamilyRestaurant, AppleOrchard, FruitAndVegetableMarket


class Player:
    def __init__(self):
        self.cards = {
            WheatField: 1,
            Ranch: 0,
            Bakery: 1,
            Cafe: 0,
            ConvenienceStore: 0,
            Forest: 0,
            Stadium: 0,
            TvStation: 0,
            BusinessCenter: 0,
            CheeseFactory: 0,
            FurnitureFactory: 0,
            Mine: 0,
            FamilyRestaurant: 0,
            AppleOrchard: 0,
            FruitAndVegetableMarket: 0,
        }
        self.wallet = 3

        self.landmarks = {
            "Train Station": (False, 6),
            "Shopping Mall": (False, 10),
            "Amusement Park": (False, 16),
            "Radio Tower": (False, 22)
        }


        # train station  | you may roll 1 or 2 dice
        # shopping mall  | each of your cup and bread establishments earn +1 coin
        # amusement park | if you roll doubles take another turn after this one
        # radio tower    | once every turn you can choose to re-roll your dice
