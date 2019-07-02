import random, pprint, pygame
from enum import Enum
class Player:
    def __init__(self, cardList):
        self.playerOneHand = []
        self.playerOneBoard = []
        self.playerTwoBoard = []
        self.playerTwoHand = []
        self.globalCardList = cardList
        self.currentPlayer = 1

    def genCards(self, amount):
        displaylist = []
        #randomly generates (amount) cards from the globalCardList (list of all possible cards) and prints their name, will display them for purchase later and replace card drawing
        for i in range(amount):
            displaylist.append(random.choice(self.globalCardList))
        for i in displaylist:
            print(i.name)

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

    def attack(self):
        self.boardDisplay()
        card.executeFunction(card.attackFunc, self.currentPlayer)
        if self.currentPlayer == 1:
            pass
        else:
            pass
        ##Add code here dweeb##
                
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
        for card in playerOneBoard:
            card.executeFunction(card.endFunc, 1)
        for card in playerTwoBoard:
            card.executeFunction(card.endFunc, 2)
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1
        #add a global player changer, possibly as a class variable

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
    def __init__(self,name, mana, attack, health, playedFunc = "pass", destroyedFunc = "pass", attackFunc = "pass", endFunc = "pass"):
        #for all the func variables the input is a block of text which is passed into generic functions containing only an exec block, this saves me from having to write hundreds of new functions and allows for creations of new cards extremely quickly
        #The function text defaults to a function that does nothing
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
cards.append(Card("Ragnaros the Firelord" ,8,2,8,playedFunc = """if playerNum == 1:
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
cards.append(Card("Sylvannas windrunner",6,5,5, destroyedFunc = """if playerNum == 1 and player.playerTwoBoard:
    (player.playerOneBoard).append((player.playerTwoBoard).pop(random.randint(0,len(player.playerTwoBoard)-1)))
elif player.playerOneBoard and playerNum == 2:
    player.playerTwoBoard.append(random.choice(player.playerOneBoard).pop)"""))

#Reduces the cost of all cards in your hand at the end of each turn
cards.append(Card("Emperor Thaurissan",6,5,5, endFunc = """if playerNum == 1:
    for i in player.playerOneHand:
        i.mana -= 1
else:
    for i in player.playerTwoHand:
        i.mana -= 1"""))
for i in range(2):
    cards.append(Card("Bolderfist Oger",6,6,7))
player = Player([cards[1],cards[2],cards[3]],[cards[0],cards[4]], cards)
#For any variable "player" or "playerNum" within a function this refers to the player *in control* of the thing making the effect, not necessarily the player being affected
player.draw(100,1)
player.draw(100,2)


        

    
