import random, pprint, pygame
from enum import Enum
import numpy as np
#________________________________#
### MACHINE LEARNING CODE HERE ###
#________________________________#

def getImmediateReward(healthLost = 0, damageDealt = 0, minionKilled = None, minionDied = None, gameWon = False, gameLost = False):
    reward = 0
    reward -= healthLost + (minionDied.attack * 2)
    reward += damageDealt + (minionKilled.attack * 2)
    if gameLost:
        reward -= 10
    if gameWon:
        reward += 10
    return reward


    

def makeAction():
    highestReward = 0
    actionToTake = None
    variableSave = [player.playerOneHealth,player.playerTwoHealth,player.currentPlayer,player.playerOneCurrency,player.playerTwoCurrency]
    boardSave = [player.playerOneHand,player.playerTwoHand,player.playerOneBoard,player.playerTwoBoard,player.globalCardList,player.forSale]
    actions = getAvailableActions()
    for action in actions:
        if type(action) is tuple:
            player.attack(action[0],action[1])
        #Put something to execute and get the reward for each action
        if reward > highestReward:
            highestReward = reward
            actionToTake = action
        #Might need to rework this function to make recursively doing this possible (to either depth 2-3 or possibly higher depending on performance)
  
def getAvailableActions():
    actions = []
    if player.currentPlayer == 1:
        for minion in player.playerOneBoard:
            if minion.canAttack:
                for enemy in player.playerTwoBoard:
                    actions.append(tuple(minion,enemy))
        for minion in player.playerOneHand:
            if minion.mana <= player.playerOneMana:
                actions.append(minion)
        for minion in player.forSale:
            if minion.shopCost <= player.playerOneCurrency:
                actions.append(minion)
    return actions
        
        
    

#_______________________________#
### END MACHINE LEARNING CODE ###
#_______________________________#

class Player:
    def __init__(self, cardList):
        self.playerOneHealth = 25
        self.playerTwoHealth = 25
        self.playerOneHand = []
        self.playerOneBoard = []
        self.playerTwoBoard = []
        self.playerTwoHand = []
        self.playerOneMana = 1
        self.playerTwoMana = 1
        self.globalCardList = cardList
        self.currentPlayer = 1
        self.forSale = []
        self.playerOneCurrency = 0
        self.playerTwoCurrency = 0

    def genCards(self, amount):
        displaylist = []
        #randomly generates (amount) cards from the globalCardList (list of all possible cards) and prints their name, will display them for purchase later and replace card drawing
        for i in range(amount):
            displaylist.append(random.choice(self.globalCardList))
        self.forSale = displaylist
        for i in self.forSale:
            print(i.name)

    def buyCard(self, cardPos):
        if self.currentPlayer == 1:
            if self.playerOneCurrency >= self.forSale[cardPos].shopCost:
                #Adds the purchased card to the purchasinc player's hand and removes it from the shop if they have enough currency to buy it
                self.playerOneHand.append(self.forSale.pop(cardPos))
            else:
                print("Oops, looks like you dont have enough gold to purchase that card right now!")
        else:
            if self.playerTwoCurrency >= self.forSale[cardPos].shopCost:
                #Adds the purchased card to the purchasinc player's hand and removes it from the shop if they have enough currency to buy it
                self.playerTwoHand.append(self.forSale.pop(cardPos))
            else:
                print("Oops, looks like you dont have enough gold to purchase that card right now!")
                
    def boardDisplay(self):
        #Update this with pygame stuff later, simple visualiser for logic for now
        print("\n[][] Player One Board [][]")
        for i in self.playerOneBoard:
            print("[] " + i.name + " []")
        print("\n[][] Player Two Board [] []")
        for i in self.playerTwoBoard:
            print("[] " + i.name + " []")
        
    #def draw(self, amount, player):
    #    if player == 1:
    #        if len(self.playerOneDeck) < amount:
    #            amount = len(self.playerOneDeck)
    #        for count in range(amount):
    #            card_drawn = self.playerOneDeck[0]
    #            self.playerOneDeck = self.playerOneDeck[1:]
    #            self.playerOneHand.append(card_drawn)
    #        print("Player 1 drew " + str(amount) + " cards")
    #    else:
    #        if len(self.playerTwoDeck) < amount:
    #            amount = len(self.playerTwoDeck)
    #        for count in range(amount):
    #            card_drawn = self.playerTwoDeck[0]
    #            self.playerTwoDeck = self.playerTwoDeck[1:]
    #            self.playerTwoHand.append(card_drawn)
    #        print("Player 2 drew " + str(amount) + " cards")

    def attack(self, card1, card2):
        self.boardDisplay()
        card.executeFunction(card1.attackFunc, self.currentPlayer)
        card2.health -= card1.attack
        card1.health -= card2.attack
        if self.currentPlayer == 1:
            if card1.health <= 0:
                self.destroy(card1, 1)
            if card1.health <= 0:
                self.destroy(card2, 2)
        else:
            if card1.health <= 0:
                self.destroy(card1, 2)
            if card1.health <= 0:
                self.destroy(card2, 1)
                
    #def shuffle(self,player):
    #    if player == 1:
    #        self.playerOneDeck = random.shuffle(self.playerOneDeck)
    #    else:
    #        self.playerTwoDeck = random.shuffle(self.playerTwoDeck)

    def destroy(self,card, player):
        card.executeFunction(card.destroyedFunc, player)
        if player == 1:
            (self.playerOneBoard).remove(card)
        else:
            (self.playerTwoBoard).remove(card)
            
    def endTurn(self):
        #Executes the end of turn functions of the cards in play
        for card in playerOneBoard:
            card.executeFunction(card.endFunc, 1)
        for card in playerTwoBoard:
            card.executeFunction(card.endFunc, 2)
        #Changes the current player
        self.playerOneCurrency += 3
        self.playerTwoCurrency += 3
        self.currentPlayer = (self.currentPlayer % 2)+1
        self.genCards(5)

    def play(self, mana, cardPos):
        if self.currentPlayer == 1:
            card_played = self.playerOneHand[cardPos]
            #Checks if the card you're trying to play costs too much
            if card_played.mana <= mana:
                self.playerOneBoard.append((self.playerOneHand).pop(cardPos))
                card_played.executeFunction(card_played.playedFunc,1)
                mana -= card_played.mana
                print("You played a card, costing you " + str(card_played.mana) + " mana")
            else:
                print("You failed to play a card, it costs " + str(card_played.mana) + " mana, whereas you have only " + str(mana) + " mana.")
            print("You have " + str(mana) + " mana remaining.")
            return mana
        else:
            card_played = self.playerTwoHand[cardPos]
            if card_played.mana <= mana:
                self.playerTwoBoard.append((self.playerTwoHand).pop(cardPos))
                card_played.executeFunction(card_played.playedFunc,2)
                mana -= card_played.mana
                print("You played a card, costing you " + str(card_played.mana) + " mana")
            else:
                print("You failed to play a card, it costs " + str(card_played.mana) + " mana, whereas you have only " + str(mana) + " mana.")
            print("You have " + str(mana) + " mana remaining.")
            return mana

class Card:
    def __init__(self,shopCost,name, mana, attack, health, playedFunc = "pass", destroyedFunc = "pass", attackFunc = "pass", endFunc = "pass"):
        #for all the func variables the input is a block of text which is passed into generic functions containing only an exec block, this saves me from having to write hundreds of new functions and allows for creations of new cards extremely quickly
        #The function text defaults to a function that does nothing
        self.canAttack = False
        self.name = name
        self.playedFunc = playedFunc
        self.destroyedFunc = destroyedFunc
        self.attackFunc = attackFunc
        self.endFunc = endFunc
        self.mana = mana
        self.health = health
        self.attack = attack

    def executeFunction(self,text, playerNum):
        exec(text)

#Below are card definitions
cards = []
#Deals 8 damage to all minions on your opponent's board on play
cards.append(Card(4,"Ragnaros the Firelord" ,8,2,8,playedFunc = """if playerNum == 1:
    for i in player.playerTwoBoard:
        i.health -= 8
        if i.health <= 0:
            player.destroy(i,2)
else:
    for i in player.playerOneBoard:
        i.health -= 8
        if i.health <= 0:
            player.destroy(i,1)"""))

#Steals a random minion from your opponents board on death, uses an almost unreadable oneliner to do this for efficiency
cards.append(Card(3,"Sylvannas windrunner",6,5,5, destroyedFunc = """if playerNum == 1 and player.playerTwoBoard:
    (player.playerOneBoard).append((player.playerTwoBoard).pop(random.randint(0,len(player.playerTwoBoard)-1)))
elif player.playerOneBoard and playerNum == 2:
    player.playerTwoBoard.append(random.choice(player.playerOneBoard).pop)"""))

#Reduces the cost of all cards in your hand at the end of each turn
cards.append(Card(2,"Emperor Thaurissan",6,5,5, endFunc = """if playerNum == 1:
    for i in player.playerOneHand:
        i.mana -= 1
else:
    for i in player.playerTwoHand:
        i.mana -= 1"""))

cards.append(Card(1,"Bolderfist Oger",6,6,7))

#Deals 5 damage to the player playing it on play
cards.append(Card(2,"Crusader",4,6,6,playedFunc = """if playerNum == 1:
    player.playerOneHealth -= 5
else:
    player.playerTwoHealth -= 5"""))

#On death deals 2 damage to all minions on the board
cards.append(Card(1,"Angered Whelp", 2, 1,2, destroyedFunc = """for i in player.playerOneBoard:
    i.health -= 2
for i in player.playerTwoBoard:
    i.health -= 2"""))
player = Player(cards)
#Gives the second player a small headstart as they are naturally at a disadvantage due to how turn based games work
player.playerTwoCurrency += 2


#For any variable "player" or "playerNum" within a function this refers to the player *in control* of the thing making the effect, not necessarily the player being affected



        

    
