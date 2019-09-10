import random, pprint, pygame
from enum import Enum
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#Pygame Setup vvVVvv
pygame.init()
#Gets screen size to automatically set the screen size to match the native reolution
##from collections import namedtuple
##from itertools import count
##import torch
##import torch.nn as nn
##import torch.optim as optim
##import torch.nn.functional as F
##import torchvision.transforms as T

#Code to set up the pytorch environment
##device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
##Transition = namedtuple('Transition',('state', 'action', 'next_state', 'reward'))
###________________________________#
##### MACHINE LEARNING CODE HERE ###
###________________________________#
   

#_______________________________#
### END MACHINE LEARNING CODE ###
#_______________________________#

class Button:
    def __init__(self, coords, size, picture):
        self.coords = coords
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture, size)

    def press(self):
        pass

class EndTurn(Button):
    def __init__(self):
        Button.__init__(self, (10,10),(10,15),"C:\\Users\\Gabriel\\Desktop\\EndTurn.png")

    def press(self):
        player.endTurn()

class Combine(Button):
    def __init__(self):
        Button.__init__(self,(20,20),(10,15),"C:\\Users\\Gabriel\\Desktop\\Combine.png")

    def press(self):
        pass #Add something to choose a card and call player.combineCard() with that card

class Buy(Button):
    def __init__(self):
        Button.__init__(self,(30,30),(10,15),"C:\\Users\\Gabriel\\Desktop\\Buy.png")

    def press(self):
        xLoc=(player.displayInfo.current_w)/6
        for i in player.forSale:
            player.drawCard((xLoc,(player.displayInfo.current_h)/2),i)
            xLoc += (player.displayInfo.current_w)/6

class Player:
    displayInfo = pygame.display.Info()
    screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
    playerMaxMana = [None,None]
    playerHealth = [None,None]
    playerHand = [None,None]
    playerBoard = [None,None]
    playerMana = [None,None]
    playerCurrency = [None,None]
    def __init__(self, cardList):
        self.playerHealth[0] = 25
        self.playerHealth[1] = 25
        self.playerHand[0] = []
        self.playerBoard[0] = []
        self.playerBoard[1] = []
        self.playerHand[1] = []
        self.playerMaxMana[0] = 1
        self.playerMaxMana[1] = 1
        self.playerMana[0] = 1
        self.playerMana[1] = 1
        self.globalCardList = cardList
        self.currentPlayer = 1
        self.forSale = []
        self.playerCurrency[0] = 0
        self.playerCurrency[1] = 0
        self.cardImage = pygame.image.load("C:\\Users\\Gabriel\\Desktop\\Card.png")
        self.cardImage = pygame.transform.scale(self.cardImage, (148, 192))

    def combineCards(self, card):
        combinationCounter = 0
        removed = []
        for i in player.playerHand[player.currentPlayer-1]:
            if i.name == card.name and i.mana == card.mana and i.attack == card.attack and i.health == card.health:
                removed.append(i)
                combinationCounter += 1
        if len(removed) < 3:
            print("Error, you do not have enough of these cards to combine")
        else:
            for i in removed:
                player.playerHand[player.currentPlayer-1].remove(i)
            player.playerHand[player.currentPlayer-1].append(player.upgradeCard(removed))

    def upgradeCard(self, cards):
        cards[0].attack += (1 + int(((len(cards)-3)/3)))
        cards[0].health += (1 + int(((len(cards)-3)/3)))
        if cards[0].mana < 10:
            cards[0].mana += (1 + int(((len(cards)-3)/3)))
        return cards[0]
        
    def genCards(self, amount):
        displaylist = []
        #randomly generates (amount) cards from the globalCardList (list of all possible cards) and prints their name, will display them for purchase later and replace card drawing
        for i in range(amount):
            displaylist.append(random.choice(self.globalCardList))
        self.forSale = displaylist
        for i in self.forSale:
            print(i.name)

    def buyCard(self, cardPos):
        if self.playerCurrency[self.currentPlayer-1] >= self.forSale[cardPos].shopCost:
            self.playerCurrency[self.currentPlayer-1] -= self.forSale[cardPos].shopCost
            #Adds the purchased card to the purchasinc player's hand and removes it from the shop if they have enough currency to buy it
            self.playerHand[self.currentPlayer-1].append(self.forSale.pop(cardPos))
            
        else:
            print("Oops, looks like you dont have enough gold to purchase that card right now!")
                
    def boardDisplay(self):
        #Update this with pygame stuff later, simple visualiser for logic for now
        print("\n[][] Player One Board [][]:\n")
        for i in self.playerBoard[0]:
            print("[] " + i.name + f" [{i.mana}/{i.attack}/{i.health}]")
        print("\n[][] Player One Hand [][]:\n")
        for i in self.playerHand[0]:
            print("[] " + i.name + f" [{i.mana}/{i.attack}/{i.health}]")
        print("\n[][] Player Two Board [][]:\n")
        for i in self.playerBoard[1]:
            print("[] " + i.name + f" [{i.mana}/{i.attack}/{i.health}]")
        print("\n[][] Player Two Hand [][]:\n")
        for i in self.playerHand[1]:
            print("[] " + i.name + f" [{i.mana}/{i.attack}/{i.health}]")
        print(f"Player one has {player.playerMana[0]} mana and {player.playerCurrency[0]} currency\nPlayer two has {player.playerMana[1]} mana and {player.playerCurrency[1]} currency")
        print(f"Player one has {player.playerHealth[0]} health and player two has {player.playerHealth[1]} health")
        
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
        if card1.canAttack:
            card1.attacking()
            card2.health -= card1.attack
            card1.health -= card2.attack
            card1.canAttack = False
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
        else:
            print("That minion cannot attack right now")

    def destroy(self,card, player):
        card.destroyed()
        (self.playerBoard[player]).remove(card)

    def drawCard(self, location, card):
        #centres the image of the card instead of using the top left
        location = (location[0]-74,location[1]-96)
        self.screen.blit(self.cardImage,location)
        self.screen.blit(card.picture,(location[0]+17,location[1]+13))
        self.screen.blit(card.nameText,(location[0]+17,location[1]+86))
        self.screen.blit(card.hpText,(location[0]+112,location[1]+79))
        self.screen.blit(card.atkText,(location[0]+112,location[1]+100))
            
    def endTurn(self):
        #Executes the end of turn functions of the cards in play
        for card in self.playerBoard[self.currentPlayer-1]:
            card.end()
        #Changes the current player
        self.playerCurrency[0] += 3
        self.playerCurrency[1] += 3
        if self.playerMaxMana[player.currentPlayer-1] < 10:
            self.playerMaxMana[0] += 1
            self.playerMaxMana[1] += 1
        self.playerMana[0] = self.playerMaxMana[0]
        self.playerMana[1] = self.playerMaxMana[1]
        for i in self.playerBoard[player.currentPlayer-1]:
            i.canAttack = True
        self.currentPlayer = (self.currentPlayer % 2)+1
        self.genCards(5)

    def play(self, cardPos):
        card_played = self.playerHand[self.currentPlayer-1][cardPos]
        #Checks if the card you're trying to play costs too much
        if card_played.mana <= player.playerMana[player.currentPlayer-1]:
            self.playerBoard[self.currentPlayer-1].append((self.playerHand[self.currentPlayer-1]).pop(cardPos))
            card_played.played()
            player.playerMana[player.currentPlayer-1] -= card_played.mana
            print("You played a card, costing you " + str(card_played.mana) + " mana")
        else:
            print("You failed to play a card, it costs " + str(card_played.mana) + " mana, whereas you have only " + str(player.playerMana[player.currentPlayer-1]) + " mana.")
        print("You have " + str(player.playerMana[player.currentPlayer-1]) + " mana remaining.")

    def drawScreen(self):
        screen.fill((255,255,0))
        pygame.display.update()

##class Card:
##    def __init__(self,shopCost,name, mana, attack, health, playedFunc = "pass", destroyedFunc = "pass", attackFunc = "pass", endFunc = "pass"):
##        #for all the func variables the input is a block of text which is passed into generic functions containing only an exec block, this saves me from having to write hundreds of new functions and allows for creations of new cards extremely quickly
##        #The function text defaults to a function that does nothing
##        self.canAttack = False
##        self.name = name
##        self.playedFunc = playedFunc
##        self.destroyedFunc = destroyedFunc
##        self.attackFunc = attackFunc
##        self.endFunc = endFunc
##        self.mana = mana
##        self.health = health
##        self.attack = attack
##        self.shopCost = shopCost
##
##    def executeFunction(self,text, playerNum):
##        exec(text)


class CardBase:
    def __init__(self,shopCost,name, mana, attack, health, picture, text):
        #for all the func variables the input is a block of text which is passed into generic functions containing only an exec block, this saves me from having to write hundreds of new functions and allows for creations of new cards extremely quickly
        #The function text defaults to a function that does nothing
        self.canAttack = False
        self.name = name
##        self.playedFunc = playedFunc
##        self.destroyedFunc = destroyedFunc
##        self.attackFunc = attackFunc
##        self.endFunc = endFunc
        self.mana = mana
        self.health = health
        self.attack = attack
        self.shopCost = shopCost
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture, (115, 56))
        self.font = pygame.font.SysFont('arial', 16)
        self.font.set_bold(True)
        self.nameText = self.font.render(name, True, (255,255,255))
        self.hpText = self.font.render(str(self.health), True, (255,255,255))
        self.atkText = self.font.render(str(self.attack), True, (255,255,255))
        self.font2 = pygame.font.SysFont('arial', int((128/len(text.split("")))))
        self.text = text
        self.textText = [[]]
        wordLen = 0
        count = 0
        for word in self.text.split(" "):
            wordLen += len(word)
            self.textText[count].append(word)
            if wordLen > 15 and ("." not in word) :
                count += 1
                wordLen = 0
                self.textText.append([])
        print(self.textText)
##        self.textRect = self.nameText.get_rect()
##        self.textRect.center = (self.textRect[0]//2,self.textRect[1]//2)

    def played(self):
        pass

    def destroyed(self):
        pass

    def attacking(self):
        pass

    def end(self):
        pass

class Ragnaros(CardBase):
    def __init__(self):
        CardBase.__init__(self, 5, "Ragnaros", 8, 2, 8,"C:\\Users\\Gabriel\\Desktop\\Ragnaros.png","When played deals 8 damage to all enemy cards on the battlefield.")
        
    def played(self):
        playerSwap = (player.currentPlayer % 2)+1
        for i in player.playerBoard[playerSwap-1]:
            i.health -= 8
            if i.health <= 0:
                player.destroy(i,playerSwap-1)

class Sylvannas(CardBase):
    def __init__(self):
        CardBase.__init__(self, 4, "Sylvannas", 6, 5, 5,"C:\\Users\\Gabriel\\Desktop\\Sylvanas.png","When destroyed this steals a random card from your opponents side of the battlefield.")

    def destroyed(self):
        playerSwap = (player.currentPlayer % 2)+1
        if player.playerBoard[playerSwap]:
            player.playerBoard[self.currentPlayer-1].append((player.playerBoard[playerSwap-1]).pop(random.randint(0,len(player.playerBoard[playerSwap-1])-1)))

class Thaurissan(CardBase):
    def __init__(self):
        CardBase.__init__(self, 3, "Thaurissan", 6, 5, 5,"C:\\Users\\Gabriel\\Desktop\\Thaurissan.jpg","At the end of your turn this reduces the cost of all cards in your hand by 1.")

    def end(self):
        for i in player.playerHand[player.currentPlayer-1]:
            i.mana -= 1

class Crusader(CardBase):
    def __init__(self):
        CardBase.__init__(self, 2, "Crusader", 4, 6, 6,"C:\\Users\\Gabriel\\Desktop\\Crusader.jpg","When played this deals 5 damage to your player.")

    def played(self):
        player.playerHealth[player.currentPlayer-1] -= 5

class Whelp(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Whelp", 2, 1, 2,"C:\\Users\\Gabriel\\Desktop\\deathwing.jpg","When destroyed this deals 2 damage to all other cards on the battlefield.")

    def destroyed(self):
        for i in player.playerBoard[0]:
            i.health -= 2
        for i in player.playerBoard[1]:
            i.health -= 2

class Ogre(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Ogre", 6, 6, 7,"C:\\Users\\Gabriel\\Desktop\\Oger.jpg"," ")

cards = [
        Ragnaros(),
        Sylvannas(),
        Thaurissan(),
        Crusader(),
        Whelp(),
        Ogre()
    ]

#Below are card definitions
##cards = []
#Deals 8 damage to all minions on your opponent's board on play
##cards.append(Card(4,"Ragnaros the Firelord" ,8,2,8,playedFunc = """
##playerSwap = (player.currentPlayer % 2)+1
##for i in player.playerBoard[playerSwap-1]:
##    i.health -= 8
##    if i.health <= 0:
##        player.destroy(i,playerSwap-1)"""))
##
###Steals a random minion from your opponents board on death, uses an almost unreadable oneliner to do this for efficiency
##cards.append(Card(3,"Sylvannas windrunner",6,5,5, destroyedFunc = """if playerNum == 1 and player.playerTwoBoard:
##    (player.playerOneBoard).append((player.playerTwoBoard).pop(random.randint(0,len(player.playerBoard[player.currentPlayer-1])-1)))
##elif player.playerOneBoard and playerNum == 2:
##    player.playerTwoBoard.append(random.choice(player.playerOneBoard).pop)"""))
##
###Reduces the cost of all cards in your hand at the end of each turn
##cards.append(Card(2,"Emperor Thaurissan",6,5,5, endFunc = """if playerNum == 1:
##    for i in player.playerOneHand:
##        i.mana -= 1
##else:
##    for i in player.playerTwoHand:
##        i.mana -= 1"""))
##
##cards.append(Card(1,"Bolderfist Oger",6,6,7))
##
###Deals 5 damage to the player playing it on play
##cards.append(Card(2,"Crusader",4,6,6,playedFunc = """if playerNum == 1:
##    player.playerOneHealth -= 5
##else:
##    player.playerTwoHealth -= 5"""))
##
###On death deals 2 damage to all minions on the board
##cards.append(Card(1,"Angered Whelp", 2, 1,2, destroyedFunc = """for i in player.playerOneBoard:
##    i.health -= 2
##for i in player.playerTwoBoard:
##    i.health -= 2"""))
player = Player(cards)
#Gives the second player a small headstart as they are naturally at a disadvantage due to how turn based games work
player.playerCurrency[1] += 2


#For any variable "player" or "playerNum" within a function this refers to the player *in control* of the thing making the effect, not necessarily the player being affected

##______________ MAIN GAME LOOP _________________##
player.playerHand[0].append(cards[0])
player.genCards(5)
player.playerMana[0] = 10
player.playerMana[1] = 10
player.playerMaxMana[0] = 10
player.playerMaxMana[1] = 10
player.playerCurrency[0] += 10
player.playerCurrency[1] += 10
done = False
buyButton = Buy()
while not done:
    #player.screen.blit(cards[0].picture,(10,110))
    mousepos = pygame.mouse.get_pos()
    player.screen.fill((0,0,0))
    player.drawCard(mousepos,cards[0])
    #player.drawCard((10,10),cards[1])
    buyButton.press()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #player.boardDisplay()
    
##    print("__________________________\nPlayer " + str(player.currentPlayer) + "'s Turn\n__________________________\nYou may:")
##    pprint.pprint(["1. Play a minion","2. View the shop", "3. Attack with a minion", "4. End your turn", "5. Combine Cards"])
##    choice = 0
##    while choice not in [1,2,3,4,5]:
##        try:
##            choice = int(input("Please input your choice [1,2,3,4 or 5]: "))
##        except:
##            print("Invalid input")
##    if choice == 1:
##        counter = 0
##        for i in player.playerHand[player.currentPlayer-1]:
##            print(str(counter) + ". " + i.name)
##            counter += 1
##        print(str(counter) + ". Back")
##        playChoice = 999
##        while playChoice not in range(0,len(player.playerHand[player.currentPlayer-1])+1):
##            try:
##                playChoice = int(input("please input the card you would like to play: "))
##            except:
##                print("invalid choice")
##        #print(len(player.playerHand[player.currentPlayer-1]))
##        if playChoice != len(player.playerHand[player.currentPlayer-1]):
##            player.play(playChoice)
##    elif choice == 2:
##        counter = 0
##        print("The shop has:")
##        for i in player.forSale:
##            print(str(counter)+".",i.name)
##            counter += 1
##        print(str(counter) + ". Back")
##        purchaseChoice = 255
##        while purchaseChoice not in range(0,len(player.forSale)+1):
##            try:
##                purchaseChoice = int(input("please input the card you would like to buy: "))
##            except:
##                print("invalid choice")
##        if purchaseChoice != len(player.forSale):
##            player.buyCard(purchaseChoice)
##    elif choice == 3:
##        counter = 0
##        print("You have " + str(len(player.playerBoard[player.currentPlayer-1])) + " minions, of which:")
##        for i in player.playerBoard[player.currentPlayer-1]:
##            if i.canAttack:
##                print(i.name)
##        print("Can attack")
##        for i in player.playerBoard[player.currentPlayer-1]:
##            print(str(counter) + ". " + i.name)
##            counter += 1
##        print(str(counter) + ". Back")
##        attackChoice = 255
##        while attackChoice not in range(0,len(player.playerBoard[player.currentPlayer-1])+1):
##            try:
##                attackChoice = int(input("please input the card you would like to attack with: "))
##            except:
##                print("invalid choice")
##        enemyChoice = 255
##        if player.currentPlayer == 2:
##            playerSwap = 1
##        else:
##            playerSwap = 2
##        counter = 0
##        for i in player.playerBoard[playerSwap-1]:
##            print(str(counter) + ". " + i.name)
##        while enemyChoice not in range(0,len(player.playerBoard[playerSwap-1])+1):
##            try:
##                enemyChoice = int(input("please input the card you would like to attack: "))
##            except:
##                print("invalid choice")
##        skip = False
##        try:
##            if len(player.playerBoard[playerSwap-1]) == 0 and player.playerBoard[player.currentPlayer-1][attackChoice].canAttack:
##                player.playerHealth[playerSwap-1] -= player.playerBoard[player.currentPlayer-1][attackChoice].attack
##                player.playerBoard[player.currentPlayer-1][attackChoice].canAttack = False
##                skip = True
##            elif not player.playerBoard[player.currentPlayer-1][attackChoice].canAttack:
##                print("That minion cannot attack right now")
##                skip = True
##        except:
##            skip = True
##        if attackChoice != len(player.playerBoard[player.currentPlayer-1]) and not skip:
##            player.attack(player.playerBoard[player.currentPlayer-1][attackChoice],player.playerBoard[playerSwap-1][enemyChoice])
##    elif choice == 4:
##        player.endTurn()
##    elif choice == 5:
##        counter = 0
##        print("You have the following cards, choose one which you have at least 3 of to combine:")
##        for i in player.playerHand[player.currentPlayer-1]:
##            print(str(counter)+".",i.name)
##            counter += 1
##        print(str(counter) + ". Back")
##        combinationChoice = 255
##        while combinationChoice not in range(0,len(player.playerHand[player.currentPlayer-1])+1):
##            try:
##                combinationChoice = int(input("please input the card you would like to combine: "))
##            except:
##                print("invalid choice")
##        if combinationChoice != len(player.playerHand[player.currentPlayer-1]):
##            player.combineCards(player.playerHand[player.currentPlayer-1][combinationChoice])
                    
    #if player.playerHealth[0] <= 0 or player.playerHealth[1] <= 0:
    #    done = True
        
    
    
