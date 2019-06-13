import random, pprint, pygame
from enum import Enum
class Player:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.board = []

    def addCard(self, card):
        self.deck.append(card)

    def draw(self, amount):
        if len(self.deck) < amount:
            amount = len(self.deck)
        for count in range(amount):
            card_drawn = self.deck[0]
            self.deck = self.deck[1:]
            self.hand.append(card_drawn)
            print(self.Name + " drew " + card_drawn.name)

    def shuffle(self):
        self.deck = random.shuffle(self.deck)

    def destroy(self, card):
        (self.board).remove(card)

    def play(self, mana, cardPos):
        card_played = self.hand[cardPos]
        if card_played.cost <= mana:
            self.board.append((self.hand).pop(card))
            #card_played.battlecry()
            mana -= card_played.cost
            print("You played " + card_played.name + ", costing you " + str(card_played.cost) + " mana")
        else:
            print("You failed to play " + card_played.name + ", it costs " + str(card_played.cost) + " mana, whereas you have only " + str(mana) + " mana.")
        print("You have " + str(mana) + " mana remaining.")
        return mana

class Card:
    def __init__(self,mana, health, attack, playedFunc = "pass", destroyedFunc = "pass", attackFunc = "pass", endFunc = "pass"):
        #for all the func ones input block of text which is passed into generic functions containing only an exec block, this saves me from having to write hundreds of new functions and allows for creations of new cards extremely quickly
        #The lambda functions default to a function that always returns false
        self.playedFunc = playedFunc
        self.destroyedFunc = destroyedFunc
        self.attackFunc = attackFunc
        self.endFunc = endFunc
        self.mana = mana
        self.health = health
        self.attack = attack

    def executeFunction(self,text):
        exec(text)
        
