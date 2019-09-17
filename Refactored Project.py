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
#________________________________#
### MACHINE LEARNING CODE HERE ###
#________________________________#


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

    def draw(self):
        player.screen.blit(self.picture,self.coords)


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

class ShowShop(Button):
    def __init__(self):
        Button.__init__(self,(30,30),(10,15),"C:\\Users\\Gabriel\\Desktop\\Buy.png")
        self.buttons = []
    def press(self):
        buttons = []
        xLoc=(player.screen.get_width())/6
        for i in player.forSale:
            player.drawCard((xLoc,(player.screen.get_height())/2),i)
            buttons.append(Buy(i,((xLoc-30,((player.screen.get_height())/2)+200))))
            xLoc += (player.screen.get_width())/6
        for button in buttons:
            button.draw()
        self.buttons = buttons
    
class Buy(Button):
    def __init__(self, card, coords):
        Button.__init__(self,coords,(60,27),"C:\\Users\\Gabriel\\Desktop\\Buy.png")
        self.card = card

    def press(self):
        player.buyCard(self.card)

class Player:
    displayInfo = pygame.display.Info()
    screen = pygame.display.set_mode((displayInfo.current_w-300, displayInfo.current_h-300))
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
        cards = []
        #randomly generates (amount) cards from the globalCardList (list of all possible cards) and prints their name, will display them for purchase later and replace card drawing
        for card in self.globalCardList:
            cards.append(card())
        for i in range(amount):
            displaylist.append(random.choice(cards))
        self.forSale = displaylist
        for i in self.forSale:
            print(i.name)

    def buyCard(self, card):
        if self.playerCurrency[self.currentPlayer-1] >= card.shopCost:
            self.playerCurrency[self.currentPlayer-1] -= card.shopCost
            #Adds the purchased card to the purchasinc player's hand and removes it from the shop if they have enough currency to buy it
            self.playerHand[self.currentPlayer-1].append(card)    
        else:
            print("Oops, looks like you dont have enough gold to purchase that card right now!")

    def attack(self, card1, card2):
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
        addFactor = 125
        for line in card.textDisplay:
            self.screen.blit(line,(location[0]+17,location[1]+addFactor))
            addFactor += 11
            
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
        self.screen.fill((255,255,0))
        pygame.display.update()

    def boardDisplay(self):
        size = self.screen.get_size()
        location = 115
        for card in self.playerHand[self.currentPlayer-1]:
            self.drawCard((location,size[1]-115),card)
            location += 56

class CardBase:
    def __init__(self,shopCost,name, mana, attack, health, picture, text):
        self.canAttack = False
        self.name = name
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
        #Font scaled for the text of each card vv vv
        self.font2 = pygame.font.SysFont('arial', int((180/len(text.split(" ")))))
        self.text = text
        textSplit = [[]]
        wordLen = 0
        count = 0
        for word in self.text.split(" "):
            wordLen += len(word)
            textSplit[count].append(word)
            if wordLen > 12 and ("." not in word):
                count += 1
                wordLen = 0
                textSplit.append([])
        count = 0
        self.textDisplay = []
        for line in textSplit:
            #Transforms the split text into font form for rendering on the card in a more legible way
            self.textDisplay.append(self.font2.render(" ".join(line), True, (255,255,255)))

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
        CardBase.__init__(self, 2, "Crusader", 4, 6, 6,"C:\\Users\\Gabriel\\Desktop\\Crusader.jpg","When this card is played this deals 5 damage to your player.")

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
        CardBase.__init__(self, 1, "Ogre", 5, 2, 4,"C:\\Users\\Gabriel\\Desktop\\Oger.jpg","When this card is played this summons a copy of itself.")

    def played(self):
        player.playerBoard[player.currentPlayer-1].append(Ogre())

#This list stores the references to the classes in order that new objects can be created instead of duplicating old ones, meaning that specific instances of objects can be changed
cards = [
        Ragnaros,
        Sylvannas,
        Thaurissan,
        Crusader,
        Whelp,
        Ogre
    ]

#This list is to help speed up graphical things as it will not have to repeatedly declare the objects to render
declaredCards = [
        Ragnaros(),
        Sylvannas(),
        Thaurissan(),
        Crusader(),
        Whelp(),
        Ogre()
    ]

player = Player(cards)
#Gives the second player a small headstart as they are naturally at a disadvantage due to how turn based games work
player.playerCurrency[1] += 2


#For any variable "player" or "playerNum" within a function this refers to the player *in control* of the thing making the effect, not necessarily the player being affected

##______________ MAIN GAME LOOP _________________##
player.playerHand[0].append(cards[0]())
player.playerHand[0].append(cards[1]())
player.genCards(5)
player.playerMana[0] = 10
player.playerMana[1] = 10
player.playerMaxMana[0] = 10
player.playerMaxMana[1] = 10
player.playerCurrency[0] += 10
player.playerCurrency[1] += 10
done = False
shopButton = ShowShop()
while not done:
    #player.screen.blit(cards[0].picture,(10,110))
    mousepos = pygame.mouse.get_pos()
    player.screen.fill((0,0,0))
    player.drawCard(mousepos,declaredCards[0])
    for i in shopButton.buttons:
        temprect = i.picture.get_rect()
        print(temprect)
        if temprect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
            i.press()
    #player.drawCard((10,10),cards[1])
    shopButton.press()
    player.boardDisplay()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #player.boardDisplay()

    
    
