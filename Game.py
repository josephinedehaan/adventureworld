from Player import Player
from Room import Room
from Npc import Npc
from Utils import gameLog
import random

"""
    This class is the main class of the "Adventure World" application. 
    This main class creates and initialises all the others: it creates all
    rooms, creates the parser and starts the game. 
"""


class Game:

    def __init__(self):
        """
        Initialises the game
        """
        self.setupSupermarket()
        self.setupNPCs()
        self.player = Player(self.outside)
        self.tempShoppingList = []
        self.createShoppingList()
        self.player.setShoppingList(self.tempShoppingList)
        self.inAisle = False
        self.selectedBonusItem = {}
        self.setBonusItem()
        self.player.setBonusItem(self.selectedBonusItem)
        self.secretItems = {}
        self.getSecretItems()
        self.player.setSecretItems(self.secretItems)

    def setupSupermarket(self):
        """
            Sets up all supermarket assets
        :return: None
        """
        self.outside = Room("outside", "There's not much out here... Try going inside!", None, None)

        self.lobby = Room("lobby", "There is a stack of baskets next to you.\n There's a friendly store worker, Lisa"
                                   " - she wants to talk to you",
                          None, None)

        self.aisleOne = Room("aisle 1", "There are piles of colourful fresh fruits and vegetables",
                             ['APPLES', 'BANANAS', 'CELERY', 'CARROTS', 'MELON', 'GRAPES', 'BROCCOLI', 'AVOCADOS'],
                             {"KIWI": "The item you are looking for is the word for a bird, a food and a person."}, )

        self.aisleTwo = Room("aisle 2", "There are fridges full of fresh milk, cheese, meat, fish and eggs. \n"
                                        "There is a store worker Sam, he wants to talk to you.",
                             ['YOGHURT', 'MILK', 'CHEDDAR', 'FETA', 'CHICKEN', 'FISHCAKES', 'HAM'],
                             {"EDAM": "The item you are looking for is a cheese which is made backwards",
                              "EGG": "The item you are looking for is one of the two main characters of a "
                                     "famous causality dilemma"})

        self.aisleThree = Room("aisle 3", "There are dry goods: tins of soup, beans, pasta, rice and pulses",
                               ['RICE', 'PASTA', 'SPAGHETTI', 'LENTILS', 'BEANS', 'SOUP', 'CRACKERS'],
                               {"HONEY": "The item you are looking for is known to never spoil.",
                                "BARLEY": "The item you are looking for was one of the first forms of "
                                          "currency used in ancient Mesopotamia."})

        self.aisleFour = Room("aisle 4", "There bottles of juice, soda, mineral water and squash. "
                                         "\nThere is a key on the ground",
                              ['WINE', 'WATER', 'LEMONADE', 'JUICE', 'BEER', 'FANTA', 'PEPSI', 'SPRITE'],
                              {"WATER": "The item you are looking for has the chemical formula H2O"})

        self.aisleFive = Room("aisle 5", "There are freshly baked loaves of bread, cakes and pastries.\n "
                                         "There is also a locked door",
                              ['BREAD', 'BAGUETTE', 'CUPCAKES', 'CROISSANTS', 'BAGELS', 'TORTILLAS'], None)

        self.secretAisle = Room("secret aisle", "You are in a secret aisle full of delicious items! \n"
                                                "There is a friendly store worker, Eddy, who wants to talk to you.",
                                {"PINEAPPLE": 6, "CHOCOLATE": 4, "PRETZELS": 8, "PIZZA": 8, "CHEESECAKE": 5, }, None)

        self.checkout = Room("checkout", "There is a friendly store worker, Dot, at the checkout. "
                                         ""
                                         "Talk to her if you are ready to checkout", None, None)

        self.outside.setExit("NORTH", self.lobby)

        self.lobby.setExit("NORTH", self.aisleOne)
        self.lobby.setExit("SOUTH", self.outside)

        self.aisleOne.setExit("EAST", self.aisleTwo)
        self.aisleOne.setExit("SOUTH", self.lobby)

        self.aisleTwo.setExit("EAST", self.aisleThree)
        self.aisleTwo.setExit("WEST", self.aisleOne)

        self.aisleThree.setExit("EAST", self.aisleFour)
        self.aisleThree.setExit("WEST", self.aisleTwo)

        self.aisleFour.setExit("EAST", self.aisleFive)
        self.aisleFour.setExit("WEST", self.aisleThree)

        self.aisleFive.setExit("WEST", self.aisleFour)
        self.aisleFive.setExit("SOUTH", self.checkout)

        self.checkout.setExit("NORTH", self.aisleFive)
        self.checkout.setExit("SOUTH", self.outside)

        self.aisles = [self.aisleOne, self.aisleTwo, self.aisleThree, self.aisleFour, self.aisleFive]

    def setupNPCs(self):
        """
            Sets up all NPC names, dialogue lines and location.
        :return: None
        """
        lisa = Npc("LISA")
        lisa.addLine("Here is your shopping list. Once you've taken your basket, you will be able to see it using "
                     "the list button on the left. \n"
                     "Your goal is to fill your basket with as many of items on the list as possible."
                     "The items in your basket will appear on the right.")

        sam = Npc("SAM")
        sam.addLine("Hello! I hope you're enjoying your time at Adventure World Supermarket."
                    "I have a riddle that may help you find the bonus item."
                    "If you think you have guessed the item, use the command word 'guess'."
                    "The item will automatically be added to your basket. \n")

        eddy = Npc("EDDY")
        eddy.addLine(f'You\'ve made it to the secret room! You must be hungry.'
                     f'You are allowed to snack on one of these items. All items are worth points,'
                     f' but I cannot tell you which one is worth more. Here is what\'s on the menu.'
                     f' Take one! Choose wisely. Good luck! \n'
                     f'{", ".join(list(self.secretAisle.items.keys()))}')

        dot = Npc("DOT")

        self.lobby.setNpc(lisa)  # assigns NPCs to various rooms
        self.aisleTwo.setNpc(sam)
        self.secretAisle.setNpc(eddy)
        self.checkout.setNpc(dot)

    def createSecretRoom(self):
        """
            Creates a secret room only
            accessible with a key.
        :return: Various string messages for the GUI
        """
        # Checks that user has met all conditions to enter secret room
        if self.player.hasKey and self.player.currentRoom is self.aisleFive:
            self.secretAisle.setExit("WEST", self.aisleFive)
            self.aisleFive.setExit("EAST", self.secretAisle)
            gameLog('User unlocked secret room.')
            return "Door unlocked. Go east to enter the secret aisle."
        elif not self.player.hasKey:
            gameLog('User tried unlocking room without key.')
            return "You can't unlock unless you have found the key."
        elif self.player.currentRoom != self.aisleFive:
            gameLog('User tried unlocking room in the wrong aisle.')
            return "There are no doors to unlock here... Try going somewhere else!"

    def createShoppingList(self):
        """
            Iterates through a list of aisles then selects two random items
            from each aisle items list and creates a new list with the selected items.
        :return: list to be passed into the permanent shopping list.
        """
        for aisle in self.aisles:
            self.tempShoppingList.extend(random.sample(aisle.items, 2))
        return self.tempShoppingList

    def getSecretItems(self):
        """
            Gets secret items from secret aisle to make them accessible to Player class
        :return: list to be passed into the permanent shopping list.
        """
        self.secretItems.update(self.secretAisle.items)

    def setBonusItem(self):
        """
            Creates a new dictionary from the various Room() dictionary parameters
            and selects a random item from it, which is the put into a new
            dictionary.
        :return: None
        """
        bonusItems = {}

        for aisle in self.aisles:
            if aisle.bonusItem != None:
                for item in aisle.bonusItem:
                    bonusItems[item] = aisle.bonusItem[item]

        randItem = random.choice(list(bonusItems))
        self.selectedBonusItem[randItem] = bonusItems[randItem]

    def printWelcome(self):
        """
            Displays a welcome message.
        :return: welcome message
        """
        welcomeMsg = f'Welcome to Adventure World Supermarket! \n ' \
                     f'You are outside the supermarket. The entrance is up north.'

        if self.player.currentRoom == self.outside:
            return welcomeMsg

    def doPrintHelp(self):
        """
            Display some useful help text
        :return: help message
        """
        message = f'The goal of the game is to collect all the items on the shopping list. A store worker will give you ' \
                  f'your shopping list. There is a bonus item and a secret room... pay attention to the room ' \
                  f'description to find out how to get these. You can check out when you have got all the items on the' \
                  f'list. Bonus items are optional. If you take less than 3 minutes to complete the game, you will be ' \
                  f'rewarded, and if you take more than 8 minutes you will be penalised! ' \
                  f'Timer starts when you have taken a basket!'
        return message
