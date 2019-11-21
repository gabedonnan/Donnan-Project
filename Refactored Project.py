import random, pprint, pygame, time
from enum import Enum
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
pygame.init()
#________________________________#
### MACHINE LEARNING CODE HERE ###
#________________________________#

#Oh boy o man kill me nowski

#_______________________________#
### END MACHINE LEARNING CODE ###
#_______________________________#

class Menu:
    def __init__(self):
        self.playing = False
        #Mode True is playing in local multiplayer, mode False will be playing vs an AI
        self.mode = False
        self.tutorial = False

class TextBox:
    def __init__(self, text, maxCharWidth, bufferSize, location):
        self.location = location
        self.text = text
        self.maxCharWidth = maxCharWidth
        self.bufferSize = bufferSize
        self.font = pygame.font.SysFont('arial', 16)
        self.font.set_bold(True)
        wordLen=0
        count = 0
        textSplit = [[]]
        for word in self.text.split(" "):
            wordLen += len(word)
            textSplit[count].append(word)
            if wordLen > maxCharWidth:
                count += 1
                wordLen = 0
                textSplit.append([])
        count = 0
        self.textDisplay = []
        for line in textSplit:
            self.textDisplay.append(self.font.render(" ".join(line), True, (255,255,255)))

    def draw(self):
        addFactor = 0
        provisionalW = 0
        for i in self.textDisplay:
            if i.get_width() > provisionalW:
                provisionalW = i.get_width()
        pygame.draw.rect(player.screen,(0,0,0),(self.location,(provisionalW + 2*self.bufferSize,len(self.textDisplay)*16 + 2*self.bufferSize)),0)
        pygame.draw.rect(player.screen,(255,255,255),(self.location,(provisionalW + 2*self.bufferSize,len(self.textDisplay)*16 + 2*self.bufferSize)),2)
        for line in self.textDisplay:
            player.screen.blit(line,(self.location[0]+self.bufferSize,self.location[1]+self.bufferSize+addFactor))
            addFactor += 14

class Button:
    def __init__(self, coords, size, picture, hoverPicture = ""):
        if hoverPicture == "":
            hoverPicture = picture
        self.size = size
        self.active = False
        self.clickRect = pygame.Rect(coords,size)
        self.coords = coords
        #Initialises the images for the button, the hoverPicture is a slightly lighter image displayed when the user hovers over it, this is a purely aesthetic thing but helps in testing to know the program is functioning
        self.hoverPicture = pygame.image.load(hoverPicture)
        self.hoverPicture = pygame.transform.scale(self.hoverPicture, size)
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture, size)

    def press(self):
        #Empty press function to allow polymorphism to change the function for each subclass of this as well as for the "press" function to be called when there is no changed child function
        pass

    def draw(self):
        #Draws the button at the position it is set and checks if it is collided with the mouse to display either the normal or hover picture
        mousepos = pygame.mouse.get_pos()
        if self.clickRect.collidepoint(mousepos) and not self.active:
            player.screen.blit(self.hoverPicture,self.coords)
        elif not self.active:
            player.screen.blit(self.picture,self.coords)
        else:
            player.screen.blit(self.altImage,self.coords)

class PlayGame(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()/2-220,100),(440,280),"Images\\PlayButton.png","Images\\PlayButtonHover.png")

    def press(self):
        menu.playing = True

class ToggleTutorial(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()/2-110,450),(220,60),"Images\\Tutorial.png","Images\\TutorialHover.png")
        self.altImage = pygame.transform.scale(pygame.image.load("Images\\TutorialActive.png"),self.size)

    def press(self):
        self.active = not self.active
        menu.tutorial = not menu.tutorial

class VsAI(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()/2-70,570),(140,60),"Images\\VsAI.png","Images\\VsAIHover.png")
        self.altImage = pygame.transform.scale(pygame.image.load("Images\\VsAIActive.png"),self.size)
        self.active = True

    def press(self):
        self.active = True
        playerButton.active = False
        menu.mode = False

class VsPlayer(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()/2-140,690),(280,60),"Images\\VsPlayer.png","Images\\VsPlayerHover.png")
        self.altImage = pygame.transform.scale(pygame.image.load("Images\\VsPlayerActive.png"),self.size)

    def press(self):
        self.active = True
        AIButton.active = False
        menu.mode = True

class CloseGame(Button):
    def __init__(self):
        #Initialises the button as a child of the Button superclass
        Button.__init__(self, (player.screen.get_width()-60,15), (45,45), "Images\\Close.png","Images\\CloseHover.png")

    def press(self):
        #Closes the game when the button is pressed
        pygame.quit()
        quit()

class EndTurn(Button):
    def __init__(self):
        Button.__init__(self, (player.screen.get_width()-115,(player.screen.get_height()/2)-19),(100,38),"Images\\EndTurn.png","Images\\EndTurnHover.png")

    def press(self):
        player.endTurn()

class Reroll(Button):
    def __init__(self):
        Button.__init__(self,(120,10),(45,45),"Images\\RerollButton.png","Images\\RerollButtonHover.png")

    def press(self):
        if player.playerCurrency[player.currentPlayer-1]>0:
            player.genCards(5)
            player.playerCurrency[player.currentPlayer-1]-=1

class ShowCombine(Button):
    def __init__(self):
        Button.__init__(self,(16,60),(100,40),"Images\\CombineToggle.png","Images\\CombineToggleHover.png")
        self.pressed = False

    def press(self):
        shopButton.pressed = False
        if self.pressed:
            self.pressed = False
        elif not len(player.playerHand[player.currentPlayer-1])==0:
            self.pressed = True

    def displayCards(self):
        buttons = []
        #Scales the distance between the cards to the size of the screen
        xLoc=(player.screen.get_width())/(len(player.playerHand[player.currentPlayer-1])+1)
        for i in player.playerHand[player.currentPlayer-1]:
            player.drawCard((xLoc,(player.screen.get_height())/2),i)
            buttons.append(Combine(i,((xLoc-30,((player.screen.get_height())/2)+150))))
            xLoc += (player.screen.get_width())/(len(player.playerHand[player.currentPlayer-1])+1)
        for button in buttons:
            button.draw()
        #pushes all the buttons into a class variable so they are still accessable after the displayCards function has been called and finished
        self.buttons = buttons
        
class ShowShop(Button):
    def __init__(self):
        Button.__init__(self,(15,15),(100,38),"Images\\Shop.png","Images\\ShopHover.png")
        self.buttons = []
        self.soldIcon = pygame.transform.scale(pygame.image.load("Images\\ShopSold.png"),(100,38))
        self.pressed = False

    def press(self):
        combineButton.pressed = False
        #Toggles whether the button has been pressed to allow the shop to be displayed independantly of all other aspects of the game
        if self.pressed == True:
            self.pressed = False
        elif not len(player.forSale) == 0:
            #Forces the shop button not to be pressed if the shop has no cards left
            self.pressed = True

    def displayCards(self):
        #Draws the cards displayed in the shops and the buttons corresponding to them
        buttons = []
        #Scales the distance between the cards to the size of the screen
        xLoc=(player.screen.get_width())/6
        for i in player.forSale:
            player.drawCard((xLoc,(player.screen.get_height())/2),i)
            player.drawCoin(i.shopCost,(xLoc-65,((player.screen.get_height())/2)-87))
            #Initialises a "Buy" button to each card allowing the button to call the player.buyCard function
            buttons.append(Buy(i,((xLoc-30,((player.screen.get_height())/2)+150))))
            xLoc += (player.screen.get_width())/6
        for button in buttons:
            button.draw()
        #pushes all the buttons into a class variable so they are still accessable after the displayCards function has been called and finished
        self.buttons = buttons

    def draw(self):
        mousepos = pygame.mouse.get_pos()
        if not len(player.forSale)==0:
            if self.clickRect.collidepoint(mousepos):
                player.screen.blit(self.hoverPicture,self.coords)
            else:
                player.screen.blit(self.picture,self.coords)
        else:
            player.screen.blit(self.soldIcon,self.coords)
    
class Buy(Button):
    def __init__(self, card, coords):
        Button.__init__(self,coords,(60,27),"Images\\Buy.png","Images\\BuyHover.png")
        self.card = card
        #self.clickRect = pygame.Rect(coords,(60,27))

    def press(self):
        player.buyCard(self.card)

class Combine(Button):
    def __init__(self, card, coords):
        Button.__init__(self,coords,(60,27),"Images\\Combine.png","Images\\CombineHover.png")
        self.card = card
        #self.clickRect = pygame.Rect(coords,(60,27))

    def press(self):
        player.combineCards(self.card)
        
class Player:
    displayInfo = pygame.display.Info()
    #For some reason you need to resize the image to 0.83 of the detected monitor resolution as it is too big otherwise
    screen = pygame.display.set_mode((int(displayInfo.current_w*0.83), int(displayInfo.current_h*0.83)), pygame.FULLSCREEN)
    coinIcon = [None]*15
    manaIcon = [None]*11
    moneyIcon = [None]*11
    def __init__(self, cardList):
        for i in range(0,11):
            self.manaIcon[i] = pygame.transform.scale(pygame.image.load("Images\\Mana" + str(i) + ".png"),(90,120))
        for i in range(0,11):
            self.moneyIcon[i] = pygame.transform.scale(pygame.image.load("Images\\Money" + str(i) + ".png"),(90,120))
        #Loads and scales all of the coin images
        self.coinIcon[0] = pygame.transform.scale(pygame.image.load("Images\\Coin.png"),(45,45))
        self.coinIcon[1] = pygame.transform.scale(pygame.image.load("Images\\Coin2.png"),(45,45))
        self.coinIcon[2] = pygame.transform.scale(pygame.image.load("Images\\Coin3.png"),(45,45))
        self.coinIcon[3] = pygame.transform.scale(pygame.image.load("Images\\Coin4.png"),(45,45))
        self.coinIcon[4] = pygame.transform.scale(pygame.image.load("Images\\Coin5.png"),(45,45))
        self.coinIcon[5] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin0.png"),(45,45))
        self.coinIcon[6] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin.png"),(45,45))
        self.coinIcon[7] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin2.png"),(45,45))
        self.coinIcon[8] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin3.png"),(45,45))
        self.coinIcon[9] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin4.png"),(45,45))
        self.coinIcon[10] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin5.png"),(45,45))
        self.coinIcon[11] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin6.png"),(45,45))
        self.coinIcon[12] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin7.png"),(45,45))
        self.coinIcon[13] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin8.png"),(45,45))
        self.coinIcon[14] = pygame.transform.scale(pygame.image.load("Images\\ManaCoin9.png"),(45,45))
        self.cross = pygame.transform.scale(pygame.image.load("Images\\Cross.png"),(65,65))
        self.heroPortrait = pygame.transform.scale(pygame.image.load("Images\\HeroPortrait.png"),(300,250))
        self.heroPortraitHover = pygame.transform.scale(pygame.image.load("Images\\HeroPortraitHover.png"),(300,250))
        #Initialises all class variables, can be improved in line efficiency
        self.playerHealth = [25,25]
        self.playerHand = [[],[]]
        self.playerBoard = [[],[]]
        self.playerMaxMana = [1,1]
        self.playerMana = [1,1]
        self.globalCardList = cardList
        self.currentPlayer = 1
        self.forSale = []
        self.playerCurrency = [1,2]
        self.attackHover = False
        #Initialises and scales the card background images
        self.cardImageHover = pygame.transform.scale(pygame.image.load("Images\\CardHover.png"), (148, 192))
        self.cardAttackImage = pygame.transform.scale(pygame.image.load("Images\\CardAttacking.png"),(148,192))
        self.cardImage = pygame.transform.scale(pygame.image.load("Images\\Card.png"), (148, 192))

    def combineCards(self, card):
        #Takes a card and removes all instances of it from your hand then calls upgradeCard on it
        combinationCounter = 0
        removed = []
        for i in player.playerHand[player.currentPlayer-1]:
            #Checks if the cards are all identical (i.e. you cannot combine an un-upgraded card and an upgraded one)
            if i.name == card.name and combinationCounter < 3 and not i.upgraded and not card.upgraded:
                removed.append(i)
                combinationCounter += 1
        #Checks if you have enough cards to combine
        if len(removed) > 2:
            for i in removed:
                player.playerHand[player.currentPlayer-1].remove(i)
            #Adds the upgraded card to the player's hand
            player.playerHand[player.currentPlayer-1].append(player.upgradeCard(removed))

    def upgradeCard(self, cards):
        #Scales the amount your card has been upgraded by the amount of cards used to upgrade it
        cards[0].attack = cards[0].attack*2
        cards[0].health = cards[0].health*2
        cards[0].upgraded = True
        if cards[0].mana > 0:
            cards[0].mana -= 1
        return cards[0]

    def drawCoin(self, value, location):
        location = (location[0]-22,location[1]-22)
        self.screen.blit(self.coinIcon[value-1], location)
        
    def genCards(self, amount):
        displaylist = []
        for i in range(amount):
            displaylist.append(random.choice(self.globalCardList)())
        self.forSale = displaylist

    def buyCard(self, card):
        #Checks if you can buy the card you want to buy (i.e. you have enough currency, your hand is not full)
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
        #Allows one card to attack another if it can attack
        if card1.canAttack:
            #Calls the "attacking" function of the card, triggering specific effects the card may enact when attacking
            card1.attacking()
            #Damages each card's health for the attack value of the other
            card2.health -= card1.attack
            card1.health -= card2.attack
            card1.canAttack = False
            self.attackHover = False
        else:
            print("That minion cannot attack right now")
            self.attackHover = False

    def destroy(self,card, player):
        #Enacts the "destroyed" function of a card and removes it from the board when it dies, this has some bugs when removing larger amounts of cards
        #And as such I may have to allow it to take lists of cards to destroy
        if card.name != "Dreadsteed":
            card.destroyed()
            (self.playerBoard[player]).remove(card)
        else:
            card.health = 1

    def drawCard(self, location, card):
        mousepos = pygame.mouse.get_pos()
        #centres the image of the card instead of using the top left
        location = (location[0]-74,location[1]-96)
        #Checks if the mouse is colliding with the card
        if (mousepos[0]>location[0] and mousepos[0]<location[0]+148)and(mousepos[1]>location[1] and mousepos[1]<location[1]+192):
            try:
                if self.attackHover and pygame.mouse.get_pressed()[0] and card in self.playerBoard[(self.currentPlayer % 2)]:
                    player.attack(self.attacker,card)
                    self.attackHover = False
                    
            except:
                pass
            #Checks if the mouse is down and the card is in the player's hand so that the .play function can be called, will add the same but for .attack later 
            if pygame.mouse.get_pressed()[0] and card in self.playerHand[player.currentPlayer-1] and not shopButton.pressed and not combineButton.pressed:
                #Plays card if you're hovering over it, click and have enough mana to play it (wierd to have it in this function but it works ok, dont judge me) 
                self.play(player.playerHand[player.currentPlayer-1].index(card))
                #Rests for 0.2 seconds so that a brief click of the mouse will not rapidfire buy lots of cards
                time.sleep(0.2)
                self.attackHover = False
            if pygame.mouse.get_pressed()[0] and card in self.playerBoard[self.currentPlayer-1] and card.canAttack:
                self.attackHover = True
                self.attacker = card
                #add attack selector function
            self.screen.blit(self.cardImageHover,location) 
        elif card.canAttack:
            self.screen.blit(self.cardAttackImage,location)
        else:
            self.screen.blit(self.cardImage,location)
        #Draws the text of all relevant attributes of the card in the correct locations on the card so that they can be changed dynamically and will not need to be "hard drawn"
        self.screen.blit(card.picture,(location[0]+17,location[1]+13))
        self.screen.blit(card.nameText,(location[0]+17,location[1]+86))
        self.screen.blit(card.hpText,(location[0]+112,location[1]+79))
        self.screen.blit(card.atkText,(location[0]+112,location[1]+100))
        player.drawCoin(card.mana+6,(location[0]+138,location[1]+10))
        addFactor = 125
        #Places the scaled text in the correct location and renders it line by line so it does not stretch off the end of the card
        for line in card.textDisplay:
            self.screen.blit(line,(location[0]+17,location[1]+addFactor))
            addFactor += 11
            
    def endTurn(self):
        self.attackHover = False
        #Executes the end of turn functions of the cards in play
        for card in self.playerBoard[self.currentPlayer-1]:
            card.end()
        #Changes the current player and gives both players currency
        self.playerCurrency[player.currentPlayer-1] += 4
        if self.playerCurrency[player.currentPlayer-1] > 10:
           self.playerCurrency[player.currentPlayer-1] = 10 
        #Increments the maximum mana of each player if it is less than 10
        if self.playerMaxMana[player.currentPlayer-1] < 10:
            self.playerMaxMana[self.currentPlayer-1] += 1
        self.playerMana[0] = self.playerMaxMana[0]
        self.playerMana[1] = self.playerMaxMana[1]
        #Sets all minions on the board to be able to attack
        #Changes player
        for i in self.playerBoard[player.currentPlayer-1]:
            i.canAttack = False
        self.currentPlayer = (self.currentPlayer % 2)+1
        for i in self.playerBoard[player.currentPlayer-1]:
            i.canAttack = True
        self.genCards(5)

    def play(self, cardPos):
        card_played = self.playerHand[self.currentPlayer-1][cardPos]
        #Checks if the card you're trying to play costs too much
        if card_played.mana <= player.playerMana[player.currentPlayer-1] and len(player.playerBoard[player.currentPlayer-1])<8:
            self.playerBoard[self.currentPlayer-1].append((self.playerHand[self.currentPlayer-1]).pop(cardPos))
            card_played.played()
            player.playerMana[player.currentPlayer-1] -= card_played.mana

    def boardDisplay(self,mousepos):
        size = self.screen.get_size()
        font = pygame.font.SysFont('arial', 16)
        font.set_bold(True)
        playerSwap = (self.currentPlayer % 2)+1
        if self.playerCurrency[self.currentPlayer-1]>10:
            coins = 10
        else:
            coins = self.playerCurrency[self.currentPlayer-1]
        self.screen.blit(self.moneyIcon[coins],(size[0]-80,size[1]-130))
        self.screen.blit(self.manaIcon[self.playerMana[self.currentPlayer-1]],(size[0]-130,size[1]-130))
        #For drawing contents of hand
        location = 115
        if mousepos[1] > 550 and not shopButton.pressed and not combineButton.pressed:
            #Moves the cards so they're farther apart if your mouse is further down the screen so they are easier to interact with but make minimal clutter otherwise
            locFactor = 180
            heightMod = 115
        else:
            locFactor = 56
            heightMod = 25
        for card in self.playerHand[self.currentPlayer-1]:
            self.drawCard((location,size[1]-heightMod),card)
            location += locFactor
        #For drawing contents of board
        if not shopButton.pressed and not combineButton.pressed:
            location = 180
            #Draws the cards in the board of the current player
            for card in self.playerBoard[self.currentPlayer-1]:
                self.drawCard((location,size[1]-330),card)
                location += 180
            location = 180
            #Draws the cards in the board of the opposing player
            for card in self.playerBoard[playerSwap-1]:
                self.drawCard((location,size[1]-575),card)
                location += 180
        heroRect = self.screen.blit(self.heroPortrait,(self.screen.get_width()-375,0))
        
        if heroRect.collidepoint(mousepos):
            heroRect = self.screen.blit(self.heroPortraitHover,(self.screen.get_width()-375,0))
            if self.attackHover and pygame.mouse.get_pressed()[0]:
                self.attackHero(self.attacker)
        else:
            heroRect = self.screen.blit(self.heroPortrait,(player.screen.get_width()-375,0))
        healthText = font.render(str(self.playerHealth[playerSwap-1]),True,(255,255,255))
        self.screen.blit(healthText,(self.screen.get_width()-346,213))

    def attackHero(self, card):
        playerSwap = (self.currentPlayer % 2)+1
        card.attacking()
        self.playerHealth[playerSwap-1] -= card.attack
        card.canAttack = False
        self.attackHover = False

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
        #Initialises the font for most card text
        self.font = pygame.font.SysFont('arial', 16)
        self.font.set_bold(True)
        self.nameText = self.font.render(name, True, (255,255,255))
        self.hpText = self.font.render(str(self.health), True, (255,255,255))
        self.atkText = self.font.render(str(self.attack), True, (255,255,255))
        #Initialises the font scaled for the text of each card
        self.font2 = pygame.font.SysFont('arial', int((180/len(text.split(" ")))))
        self.text = text
        textSplit = [[]]
        wordLen = 0
        count = 0
        self.upgraded = False
        #Splits the text automatically into lines based on how long it is using the custom scaled font
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

class Glocktopus(CardBase):
    #All init statements for CardBase subclasses are extremely similar, merely passing in the values needed
    def __init__(self):
        CardBase.__init__(self, 2, "Glocktopus", 5, 2, 8,"Images\\Glocktopus.png","When played deals 8 damage to all enemy cards on the battlefield.")
        
    def played(self):
        #Deals 8 damage to all cards on the opposing side of the board
        playerSwap = (player.currentPlayer % 2)+1
        destroyed = []
        for i in player.playerBoard[playerSwap-1]:
            i.health -= 8


class Sylvannas(CardBase):
    def __init__(self):
        CardBase.__init__(self, 3, "Sylvannas", 4, 5, 5,"TempImages\\Sylvanas.png","When destroyed this steals a random card from your opponents side of the battlefield.")

    def destroyed(self):
        #Steals a card from the opposing player's board (if they have one) and makes it unable to attack this turn
        playerSwap = (player.currentPlayer % 2)+1
        #Switches attackHover to false so that if this card steals something without a player attacking when they were previously planning to (as can happen in specific situations) they will not continue to try and attack with a card they no longer have
        player.attackHover = False 
        if self in player.playerBoard[player.currentPlayer-1] and player.playerBoard[playerSwap-1]:
            player.playerBoard[player.currentPlayer-1].append((player.playerBoard[playerSwap-1]).pop(random.randint(0,len(player.playerBoard[playerSwap-1])-1)))
            player.playerBoard[player.currentPlayer-1][len(player.playerBoard[player.currentPlayer-1])-1].canAttack = False
        elif self in player.playerBoard[playerSwap-1] and player.playerBoard[player.currentPlayer-1]:
            player.playerBoard[playerSwap-1].append((player.playerBoard[player.currentPlayer-1]).pop(random.randint(0,len(player.playerBoard[player.currentPlayer-1])-1)))
            player.playerBoard[playerSwap-1][len(player.playerBoard[playerSwap-1])-1].canAttack = False

class Thaurissan(CardBase):
    def __init__(self):
        CardBase.__init__(self, 3, "Thaurissan", 4, 5, 5,"TempImages\\Thaurissan.jpg","At the end of your turn this reduces the cost of all cards in your hand by 1.")

    def end(self):
        for i in player.playerHand[player.currentPlayer-1]:
            #Reduces the cost of playing all cards in the controlling player's hand by 1
            if i.mana > 0:
                i.mana -= 1

class Crusader(CardBase):
    def __init__(self):
        CardBase.__init__(self, 2, "Crusader", 2, 6, 6,"TempImages\\Crusader.jpg","When this card is played this deals 5 damage to your player.")

    def played(self):
        #Deals 5 damage to the player that plays it
        player.playerHealth[player.currentPlayer-1] -= 5

class Armoursmith(CardBase):
    def __init__(self):
        CardBase.__init__(self, 2, "Armoursmith", 1, 1, 3,"TempImages\\Blacksmith.jpg","At the end of your turn this gives a friendly card in play 2 additional health")

    def end(self):
        choice = random.choice(player.playerBoard[player.currentPlayer-1])
        choice.health += 2

class Meteor(CardBase):
    def __init__(self):
        CardBase.__init__(self, 3, "Meteor", 4, 6, 3, "Images\\Meteor.png", "This card can attack immediately when played instead of waiting a turn.")

    def played(self):
        self.canAttack = True

class Implings(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Implings", 0, 2, 1, "Images\\Imps.png", "When this card is destroyed reroll the shop for the current player.")

    def destroyed(self):
        player.genCards(5)

class Dreadsteed(CardBase):
    def __init__(self):
        CardBase.__init__(self,4,"Dreadsteed",4,1,1,"TempImages\\Dreadsteed.jpg","This card cannot have its health reduced below 1.")

class Whelp(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Whelp", 1, 1, 2,"TempImages\\deathwing.jpg","When destroyed this deals 2 damage to all other cards on the battlefield.")

    def destroyed(self):
        #Deals 2 damage to all cards on both players boards when destroyed
        for i in player.playerBoard[0]:
            i.health -= 2
        for i in player.playerBoard[1]:
            i.health -= 2

class Ogre(CardBase):
    def __init__(self):
        CardBase.__init__(self, 1, "Ogre", 3, 2, 3,"TempImages\\Oger.jpg","When this card is played this summons a copy of itself.")

    def played(self):
        #Summons a copy of itself when played
        if not len(player.playerBoard[player.currentPlayer-1]) == 8:
            player.playerBoard[player.currentPlayer-1].append(Ogre())
        if self.upgraded:
            player.playerBoard[player.currentPlayer-1][len(player.playerBoard[player.currentPlayer-1])-1].health = 8
            player.playerBoard[player.currentPlayer-1][len(player.playerBoard[player.currentPlayer-1])-1].attack = 4

def updateCards():
    for i in player.playerBoard[0]:
        i.hpText = i.font.render(str(i.health), True, (255,255,255))
        i.atkText = i.font.render(str(i.attack), True, (255,255,255))
        if i.health <= 0:
            try:
                player.destroy(i,0)
            except:
                player.destroy(i,1)
    for i in player.playerHand[0]:
        i.hpText = i.font.render(str(i.health), True, (255,255,255))
        i.atkText = i.font.render(str(i.attack), True, (255,255,255))
        if i.health <= 0:
            try:
                player.destroy(i,0)
            except:
                player.destroy(i,1)
    for i in player.playerHand[1]:
        i.hpText = i.font.render(str(i.health), True, (255,255,255))
        i.atkText = i.font.render(str(i.attack), True, (255,255,255))
        if i.health <= 0:
            try:
                player.destroy(i,1)
            except:
                player.destroy(i,0)
    for i in player.playerBoard[1]:
        i.hpText = i.font.render(str(i.health), True, (255,255,255))
        i.atkText = i.font.render(str(i.attack), True, (255,255,255))
        if i.health <= 0:
            try:
                player.destroy(i,1)
            except:
                player.destroy(i,0)

def rotateCentre(image, angle):
    centre = image.get_rect().center
    rotatedImage = pygame.transform.rotate(image, angle)
    newRect = rotatedImage.get_rect(center = center)
    return rotatedImage, newRect
#This list stores the references to the classes in order that new objects can be created instead of duplicating old ones, meaning that specific instances of objects can be changed
#def MainGame():
cards = [
        Glocktopus,
        Sylvannas,
        Thaurissan,
        Crusader,
        Whelp,
        Ogre,
        Dreadsteed,
        Implings,
        Armoursmith,
        Meteor
    ]

#This list is to help speed up graphical things as it will not have to repeatedly declare the objects to render
declaredCards = [
        Glocktopus(),
        Sylvannas(),
        Thaurissan(),
        Crusader(),
        Whelp(),
        Ogre(),
        Dreadsteed(),
        Implings(),
        Armoursmith(),
        Meteor()
    ]

player = Player(cards)
#For any variable "player" or "playerNum" within a function this refers to the player *in control* of the thing making the effect, not necessarily the player being affected

##_______________MAIN MENU___________________##
menu = Menu()
playerButton = VsPlayer()
AIButton = VsAI()
tutorialButton = ToggleTutorial()
playGameButton = PlayGame()
while not menu.playing:
    mousepos = pygame.mouse.get_pos()
    tutorialButton.draw()
    AIButton.draw()
    playerButton.draw()
    playGameButton.draw()
    isPressed = pygame.mouse.get_pressed()[0]
    if tutorialButton.clickRect.collidepoint(mousepos) and isPressed:
        tutorialButton.press()
        time.sleep(0.2)
    if AIButton.clickRect.collidepoint(mousepos) and isPressed:
        AIButton.press()
        time.sleep(0.2)
    if playerButton.clickRect.collidepoint(mousepos) and isPressed:
        playerButton.press()
        time.sleep(0.2)
    if playGameButton.clickRect.collidepoint(mousepos) and isPressed:
        playGameButton.press()
        time.sleep(0.2)
    pygame.display.update()
    pygame.event.pump()



##______________ MAIN GAME LOOP _________________##
#Initialises all variables needed
player.genCards(5)
done = False
#Initialises objects needed
shopButton = ShowShop()
rerollButton = Reroll()
combineButton = ShowCombine()
closeButton = CloseGame()
endButton = EndTurn()
boardPicture = pygame.image.load("Images\\Board.png")
boardPicture = pygame.transform.scale(boardPicture, (player.screen.get_width(), player.screen.get_height()))
tutorialBoxes = [
    TextBox("Welcome to the game, here's a brief overview of the game's mechanics. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("Each turn you gain a set amount of gold which you can spend at the shop to buy cards. In order to open the shop press the shop button in the top left corner of the screen. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("If the cards in the shop are not to your liking or you have already bought everything in it you can spend 1 gold in order to refresh its contents using the reroll button which appears next to the shop button when the shop is open. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("When you have 3 of the same card you can choose to combine them to make a more powerful card using the combine button. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("You start the game with 1 maximum mana, this increases by 1 for each of your turn up to a maximum of 10. At the start of each turn your mana refreshes up to your maximum mana value. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("Each card has a mana cost associated with it, playing the cards (by clicking the cards when they're in your hand) will expend that much mana if it can, if it cannot you will not be able to play the card. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("Your cards will not normally be able to attack immediately when played, you will have to wait until your next turn. In order to attack with a card you click on a card with a green outline on the board and its desired target, whether that be your opponent or their cards on the board --PRESS SPACE TO CONTINUE--", 25, 8, (120,3)),
    TextBox("In order to win the game you must reduce the health of your opponent's hero down to 0 and having your health reduced to 0 or below will result in you losing the game. --PRESS SPACE TO CONTINUE--", 20, 8, (120,3)),
    TextBox("That concludes the tutorial, have fun playing the game! --PRESS SPACE TO CLOSE--", 20, 8, (120,3))
    ]
textBox=tutorialBoxes[0]
#ai=AI()
tutorialCounter = 0
while not done:
    mousepos = pygame.mouse.get_pos()
    #Draws the board
    player.screen.blit(boardPicture,(0,0))
    #Draws buttons so that they can be interacted with (they could still technically be clicked without being drawn but they would be invisible)
    shopButton.draw()
    endButton.draw()
    closeButton.draw()
    combineButton.draw()
    if menu.tutorial:
        textBox.draw()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            try:
                tutorialCounter +=1 
                textBox = tutorialBoxes[tutorialCounter]
                time.sleep(0.5)
            except:
                menu.tutorial = False
    if shopButton.pressed:
        rerollButton.draw()
        if rerollButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
            rerollButton.press()
            time.sleep(0.2)
    #Checks if the health and attack values of each card have been changed, destroys them if their HP is below 1
    if pygame.mouse.get_pressed()[2]:
        player.attackHover = False
    updateCards()
    #Checks if mouse is collided with the button and is clicked, if so it activates the pressed functions of the buttons
    if endButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        endButton.press()
        boardPicture = pygame.transform.flip(boardPicture, 1,1)
        time.sleep(0.2)
    if shopButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        shopButton.press()
        time.sleep(0.2)
    if combineButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        combineButton.press()
        time.sleep(0.2)
    if closeButton.clickRect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
        closeButton.press()
        time.sleep(0.2)
    if shopButton.pressed:
        shopButton.displayCards()
        for i in shopButton.buttons:
            #Defines the collision rects for each button generated by the shopButton
            temprect = pygame.Rect(i.coords,(60,27))
            if temprect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
                i.press()
                time.sleep(0.1)
    elif combineButton.pressed:
        combineButton.displayCards()
        for i in combineButton.buttons:
            #Defines the collision rects for each button generated by the combineButton
            temprect = pygame.Rect(i.coords,(60,27))
            if temprect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
                i.press()
                time.sleep(0.1)
    #Displays everything on the board and in the hand of players
    player.boardDisplay(mousepos)
    if player.attackHover:
        player.screen.blit(player.cross,(mousepos[0]-32,mousepos[1]-32))
    #Updates the diplay
    pygame.display.update()
    #Checks if the window has been closed (this is essentially functionless for now but it manages events)
    if player.playerHealth[0] < 1 or player.playerHealth[1] < 1:
        done = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #player.boardDisplay()
pygame.quit()
    
    
