import random, pprint, pygame, time
from enum import Enum
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
pygame.init()
#________________________________#
### MACHINE LEARNING CODE HERE ###
#________________________________#


#_______________________________#
### END MACHINE LEARNING CODE ###
#_______________________________#

class Button:
    def __init__(self, coords, size, picture, hoverPicture = ""):
        if hoverPicture == "":
            hoverPicture = picture
        self.clickRect = pygame.Rect(coords,size)
        self.coords = coords
        self.hoverPicture = pygame.image.load(hoverPicture)
        self.hoverPicture = pygame.transform.scale(self.hoverPicture, size)
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture, size)

    def press(self):
        pass

    def draw(self):
        mousepos = pygame.mouse.get_pos()
        if self.clickRect.collidepoint(mousepos):
            player.screen.blit(self.hoverPicture,self.coords)
        else:
            player.screen.blit(self.picture,self.coords)

class CloseGame(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()-60,15), (45,45), "Images\\Close.png","Images\\CloseHover.png")
        #self.clickRect = pygame.Rect((player.screen.get_width()-60,15),(45,45))

    def press(self):
        pygame.quit()
        quit()

class EndTurn(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()-115,(player.screen.get_height()/2)-19),(100,38),"Images\\EndTurn.png","Images\\EndTurnHover.png")

    def press(self):
        player.endTurn()

class Combine(Button):
    def __init__(self):
        Button.__init__(self,(20,20),(10,15),"Images\\Combine.png")

    def press(self):
        pass #Add something to choose a card and call player.combineCard() with that card

class ShowShop(Button):
    def __init__(self):
        Button.__init__(self,(15,15),(100,38),"Images\\Shop.png","Images\\ShopHover.png")
        self.buttons = []
        #self.clickRect = pygame.Rect((15,15),(100,38))
        self.pressed = False

    def press(self):
        if self.pressed == True:
            self.pressed = False
        elif not len(player.forSale) == 0:
            self.pressed = True

    def displayCards(self):
        buttons = []
        xLoc=(player.screen.get_width())/6
        for i in player.forSale:
            player.drawCard((xLoc,(player.screen.get_height())/2),i)
            buttons.append(Buy(i,((xLoc-30,((player.screen.get_height())/2)+150))))
            xLoc += (player.screen.get_width())/6
        for button in buttons:
            button.draw()
        self.buttons = buttons
    
class Buy(Button):
    def __init__(self, card, coords):
        Button.__init__(self,coords,(60,27),"Images\\Buy.png","Images\\BuyHover.png")
        self.card = card
        #self.clickRect = pygame.Rect(coords,(60,27))

    def press(self):
        player.buyCard(self.card)

class Player:
    displayInfo = pygame.display.Info()
    #For some reason you need to resize the image to 0.83 of the detected monitor resolution as it is too big otherwise
    screen = pygame.display.set_mode((int(displayInfo.current_w*0.83), int(displayInfo.current_h*0.83)), pygame.FULLSCREEN)
    playerMaxMana = [None,None]
    playerHealth = [None,None]
    playerHand = [None,None]
    playerBoard = [None,None]
    playerMana = [None,None]
    playerCurrency = [None,None]
    coinIcon = [None]*5
    def __init__(self, cardList):
        self.coinIcon[0] = pygame.transform.scale(pygame.image.load("Images\\Coin.png"),(45,45))
        self.coinIcon[1] = pygame.transform.scale(pygame.image.load("Images\\Coin2.png"),(45,45))
        self.coinIcon[2] = pygame.transform.scale(pygame.image.load("Images\\Coin3.png"),(45,45))
        self.coinIcon[3] = pygame.transform.scale(pygame.image.load("Images\\Coin4.png"),(45,45))
        self.coinIcon[4] = pygame.transform.scale(pygame.image.load("Images\\Coin5.png"),(45,45))
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
        self.cardImageHover = pygame.transform.scale(pygame.image.load("Images\\CardHover.png"), (148, 192))
        self.cardImage = pygame.transform.scale(pygame.image.load("Images\\Card.png"), (148, 192))

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

    def buyCard(self, card):
        if self.playerCurrency[self.currentPlayer-1] >= card.shopCost and len(player.playerHand[player.currentPlayer-1])<9:
            self.playerCurrency[self.currentPlayer-1] -= card.shopCost
            self.forSale.remove(card)
            #Adds the purchased card to the purchasinc player's hand and removes it from the shop if they have enough currency to buy it
            self.playerHand[self.currentPlayer-1].append(card)
            if len(self.forSale) == 0:
                shopButton.pressed = False
        else:
            print("Oops, looks like you cant buy that right now!")

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
        mousepos = pygame.mouse.get_pos()
        #centres the image of the card instead of using the top left
        location = (location[0]-74,location[1]-96)
        if (mousepos[0]>location[0] and mousepos[0]<location[0]+148)and(mousepos[1]>location[1] and mousepos[1]<location[1]+192):
            if pygame.mouse.get_pressed()[0] and card in player.playerHand[player.currentPlayer-1]:
                #Plays card if you're hovering over it, click and have enough mana to play it (wierd to have it in this function but it works ok, dont judge me) 
                player.play(player.playerHand[player.currentPlayer-1].index(card))
                time.sleep(0.2)
            self.screen.blit(self.cardImageHover,location) 
        else:
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
        if card_played.mana <= player.playerMana[player.currentPlayer-1] and len(player.playerBoard[player.currentPlayer-1])<8:
            self.playerBoard[self.currentPlayer-1].append((self.playerHand[self.currentPlayer-1]).pop(cardPos))
            card_played.played()
            player.playerMana[player.currentPlayer-1] -= card_played.mana

    def drawScreen(self):
        self.screen.fill((255,255,0))
        pygame.display.update()

    def boardDisplay(self,mousepos):
        size = self.screen.get_size()
        #For drawing contents of hand
        location = 115
        if mousepos[1] > 550 and not shopButton.pressed:
            locFactor = 180
            heightMod = 115
        else:
            locFactor = 56
            heightMod = 25
        for card in self.playerHand[self.currentPlayer-1]:
            self.drawCard((location,size[1]-heightMod),card)
            location += locFactor
        #For drawing contents of board
        if not shopButton.pressed:
            location = 180
            for card in self.playerBoard[self.currentPlayer-1]:
                self.drawCard((location,size[1]-330),card)
                location += 180
            location = 180
            playerSwap = (player.currentPlayer % 2)+1
            for card in self.playerBoard[playerSwap-1]:
                self.drawCard((location,size[1]-575),card)
                location += 180

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
        CardBase.__init__(self, 5, "Ragnaros", 8, 2, 8,"TempImages\\Ragnaros.png","When played deals 8 damage to all enemy cards on the battlefield.")
        
    def played(self):
        #Very bugged, needs fixing, maybe make destroy function take lists
        playerSwap = (player.currentPlayer % 2)+1
        destroyed = []
        for i in player.playerBoard[playerSwap-1]:
            i.health -= 8
            if i.health <= 0:
                destroyed.append(i)
        for card in destroyed:
            player.destroy(card,playerSwap-1)

class Sylvannas(CardBase):
    def __init__(self):
        CardBase.__init__(self, 4, "Sylvannas", 6, 5, 5,"TempImages\\Sylvanas.png","When destroyed this steals a random card from your opponents side of the battlefield.")

    def destroyed(self):
        playerSwap = (player.currentPlayer % 2)+1
        if player.playerBoard[playerSwap-1]:#hahoo haheyy theres a bug here nerd
            player.playerBoard[player.currentPlayer-1].append((player.playerBoard[playerSwap-1]).pop(random.randint(0,len(player.playerBoard[playerSwap-1])-1)))

class Thaurissan(CardBase):
    def __init__(self):
        CardBase.__init__(self, 3, "Thaurissan", 6, 5, 5,"TempImages\\Thaurissan.jpg","At the end of your turn this reduces the cost of all cards in your hand by 1.")

    def end(self):
        for i in player.playerHand[player.currentPlayer-1]:
            i.mana -= 1

class Crusader(CardBase):
    def __init__(self):
        CardBase.__init__(self, 2, "Crusader", 4, 6, 6,"TempImages\\Crusader.jpg","When this card is played this deals 5 damage to your player.")

    def played(self):
        player.playerHealth[player.currentPlayer-1] -= 5

class Whelp(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Whelp", 2, 1, 2,"TempImages\\deathwing.jpg","When destroyed this deals 2 damage to all other cards on the battlefield.")

    def destroyed(self):
        for i in player.playerBoard[0]:
            i.health -= 2
        for i in player.playerBoard[1]:
            i.health -= 2

class Ogre(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Ogre", 5, 2, 4,"TempImages\\Oger.jpg","When this card is played this summons a copy of itself.")

    def played(self):
        if not len(player.playerBoard[player.currentPlayer-1]) == 8:
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
player.playerMana[0] = 100
player.playerMana[1] = 100
player.playerMaxMana[0] = 100
player.playerMaxMana[1] = 100
player.playerCurrency[0] += 100000000
player.playerCurrency[1] += 10
done = False
shopButton = ShowShop()
closeButton = CloseGame()
endButton = EndTurn()
boardPicture = pygame.image.load("Images\\Board.png")
boardPicture = pygame.transform.scale(boardPicture, (player.screen.get_width(), player.screen.get_height()))
while not done:
    #player.screen.blit(cards[0].picture,(10,110))
    mousepos = pygame.mouse.get_pos()
    player.screen.blit(boardPicture,(0,0))
    shopButton.draw()
    endButton.draw()
    closeButton.draw()
    #player.drawCard(mousepos,declaredCards[0])
    if endButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        endButton.press()
        time.sleep(0.1)
    if shopButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        shopButton.press()
        time.sleep(0.1)
    if closeButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        closeButton.press()
        time.sleep(0.1)
    if shopButton.pressed:
        shopButton.displayCards()
        for i in shopButton.buttons:
            temprect = pygame.Rect(i.coords,(60,27))
            if temprect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
                i.press()
                time.sleep(0.1)
    #player.drawCard((10,10),cards[1])
    player.boardDisplay(mousepos)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #player.boardDisplay()

    
    
