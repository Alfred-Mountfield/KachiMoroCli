from components.card import WheatField, Ranch, Bakery, Cafe, ConvenienceStore, Forest, Stadium, TvStation, BusinessCenter, \
    CheeseFactory, FurnitureFactory, Mine, FamilyRestaurant, AppleOrchard, FruitAndVegetableMarket


class Shop:
    def __init__(self):
        self.inventory = {
            WheatField: 6,
            Ranch: 6,
            Bakery: 6,
            Cafe: 6,
            ConvenienceStore: 6,
            Forest: 6,
            Stadium: 4,
            TvStation: 4,
            BusinessCenter: 4,
            CheeseFactory: 6,
            FurnitureFactory: 6,
            Mine: 6,
            FamilyRestaurant: 6,
            AppleOrchard: 6,
            FruitAndVegetableMarket: 6,
        }
