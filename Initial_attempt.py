import random, pprint
from enum import Enum
class Player:
    def __init__(self, canPlay, Name):
        self.deck = []
        self.hand = []
        self.board = []
        self.canPlay = canPlay
        self.Name = Name
        
    def addCard(self, card):
        self.deck.append(card)
        
    def getDeck(self):
        return self.deck

    def getHand(self):
        return self.hand

    def getBoard(self):
        return self.board

    def draw(self, amount):
        if len(self.deck) < amount:
            amount = len(self.deck)
        for count in range(amount):
            card_drawn = self.deck[0]
            self.deck = self.deck[1:]
            card_drawn.setpos(CardState.Hand)
            self.hand.append(card_drawn)
            print(self.Name + "drew " + card_drawn.name)

    def destroy(self, card):
        (self.board).remove(card)
        
        
    def play(self, mana, card):
        #if card > len(self.hand):
        #    card = len(self.hand)
        #    print("There is no card at the index you specified, playing the card at index " + str(card) + " instead.")
        card_played = self.hand[card]
        #card is the index of the card in your hand
        if card_played.cost <= mana:
            if (card_played.text).find("Battlecry:") != -1:
                #stuff which happens in each battlecry to be defined here
                pass
            card_played.setpos(CardState.Board)
            self.board.append((self.hand).pop(card))
            print("You played " + card_played.name + ", costing you " + str(card_played.cost) + " mana")
            mana = mana - card_played.cost
        else:
            print("You failed to play " + card_played.name + ", it costs " + str(card_played.cost) + " mana, whereas you have only " + str(mana) + " mana.")
        print("You have " + str(mana) + " mana remaining.")
        return mana

class Game:
    def __init__(self, state, turns, mode):
        self.state = state
        self.turns = turns
        self.mode = mode
        self.activeCards = []
        self.activeMinions = []
        
    def start(self, starting):
        self.state = GameState.Start
        for i in p1.deck:
            i.setpos(CardState.Deck)
        for i in p2.deck:
            i.setpos(CardState.Deck)
        
        p1.draw(4)
        p2.draw(5)
        #Coin = Card(0,0,0,"The Coin", "Gain 1 mana crystal this turn only", "Hand")

    def setState(self,state):
        self.state = state

    def newTurn(self, canPlay):
        self.turns = self.turns + 1
        if canPlay:
            p2.canPlay = True
            p1.canPlay = False
            p2.draw(2)
        else:
            p1.canPlay = True
            p2.canPlay = False
            p1.draw(2)

    def concede(self):
        if self.state == GameState.Playing:
            self.state = GameState.End
            p1.canPlay = False
            p2.canPlay = False
        else:
            print("You cannot concede right now")

    def getState(self):
        return self.state

class GameState(Enum):
    Playing = 0
    Start = 1
    End = 2
    
class CardState(Enum):
    Graveyard = 0
    Deck = 1
    Hand = 2
    Board = 3

    
class Card:
    #Initially sets the values for every part of the card
    def __init__(self, cost, name, text, ID):
        self.cost = cost
        self.name = name
        self.text = text
        self.pos = CardState.Deck
        self.ID = ID
    
    def setpos(self, pos):
        self.pos = pos

    #Damages the instance of the card, you must check __delete__ afterwards to make sure the card is actually dead
    def damage(self, amount):
        self.health = self.health - amount

    #Finds the list of possible targets for your attack, taunt is a boolean, False means it ignores taunt
    #Cardlist is a list of all cards in your opponent's deck

class Hero():
    def __init__(self, health, name):
        self.name = name
        self.health = health
        
class Minion(Card):
    def __init__(self, health, attack, name, cost, text, ID):
        super().__init__(name, cost, text, ID)
        self.health = health
        self.damage = attack
        self.canAttack = False
    def attackTarget(self, canAttack, attackingPlayer):#targetting,
        if canAttack:
            if attackingPlayer == "2":
                targetlist = target(True, "1")#make something to change this 1st vs 2nd at some point
                for count in range(len(targetlist)):
                    print(str(count) + ": "+ targetlist[count])
                choice = int(input("please input which target you would like to attack (the index of the target, aka the number next to it)"))
                p1.board[choice].damageTarget(self.damage, "1")
                try:
                    self.damageTarget(p1.board[choice].damage, "2")
                except:
                    pass
            else:
                targetlist = target(True, "2")#make something to change this 1st vs 2nd at some point
                for count in range(len(targetlist)):
                    print(str(count) + ": "+ targetlist[count])
                choice = int(input("please input which target you would like to attack (the index of the target, aka the number next to it)"))
                p2.board[choice].damageTarget(self.damage, "2")
                try:
                    self.damageTarget(p2.board[choice].damage, "1")
                except:
                    pass
            if self.health <= 0:
                self.pos = CardState.Graveyard
                p1.destroy(self)
            #vvvv INCORRECT CODE vvvv
            #for count in range(len(targetlist[count])):
            #    if choice == str(count):
            #        self.health = self.health - targetlist[choice].attack
            #        self.canAttack = False
            #        targetlist[choice].health = targetlist[choice].health - self.attack  
            
        else:
            print("you cannot attack with this right now")
    def damageTarget(self, amount, player):
        self.health -= amount
        #if self.health <= 0:
            #self.pos = CardState.Graveyard
            #if player == "1":
            #    p1.destroy(self)
            #else:
            #    p2.destroy(self)
class Spell(Card):
    def __init__(self, cost, name, text, ID):
        super().__init__(cost, name, text, ID)
        
    def cast(self, game):
        pass

#the "player" variable is which player you're attacking, not which player you are. May change this later depending on confusion.
def target(taunt, player):
    ##### Change this to something that gives a list of objects
    targetlist = []
    if taunt:
        #Looks through every card you've input from your opponent's starting deck
        if player == "1":
            for count in range(len(p1.board)):
                if not ((p1.board[count]).text).find("Taunt"):
                    targetlist.append((p1.board[count]).name)
        if player == "2":
            for count in range(len(p2.board)):
                if not ((p2.board[count]).text).find("Taunt"):
                    targetlist.append((p2.board[count]).name)
                
    if not targetlist:
        if player == "1":
            for count in range(len(p1.board)):
                targetlist.append((p1.board[count]).name)
        if player == "2":
            for count in range(len(p2.board)):
                targetlist.append((p2.board[count]).name)
    return targetlist

#class FooCard(Card):
#    def play(game):
#        print("Foo")


#Main program
Health = 1
#Textlist = []
p1 = Player(True, "Player 1 ")
p2 = Player(False, "Player 2 ")
newGame = Game(GameState.Playing, 0, "Standard")
#newGame.start(True)
cards = []

#Minions: Health -> attack -> cost -> name -> text


hero_player = Hero(30, "Player")
minion_infantry = Minion(1,1,1,"Infantry","Taunt", 1)
minion_lieutenant = Minion(2,1,2,"Lieutenant", "Battlecry: Deal 1 damage to a minion", 2)
minion_general = Minion(5,7,10,"General","Battlecry: Summon a 5/7 minion", 3)
minion_faceless = Minion(0,0,0, "Faceless", "Battlecry: Spend all your mana and gain attack and health equal to the mana spent", 4)
minion_theFrozenOne_legendary = Minion(8,0,4,"The Frozen One", "Deathrattle: Summon a random 10 cost minion", 5)
#Spells: cost -> name -> text
spell_fireball = Spell(5, "Fireball", "Deal 5 damage", 6)
spell_timeWarp = Spell(8, "Time Warp", "Both players cannot play cards for their next turn", 7)


for count in range(5):
    p1.addCard(minion_infantry)
    p2.addCard(minion_infantry)
    p1.addCard(minion_lieutenant)
    p2.addCard(minion_lieutenant)
    p1.addCard(minion_general)
    p1.addCard(spell_fireball)
    p1.addCard(minion_faceless)
    p1.addCard(minion_theFrozenOne_legendary)
    p1.addCard(spell_timeWarp)
newGame.start(False)
choice = "0"
mana = 10
newGame.setState(GameState.Playing)

#Main game loop
while newGame.state == GameState.Playing:
    pprint.pprint(["What do you want to do? (input the corresponding number)", "1. Play a Card", "2. Attack with your minions", "3. End your Turn", "9. Concede"])
    while not (choice == "1" or choice == "2" or choice == "3" or choice == "9"):
        choice = input()
        if not (choice == "1" or choice == "2" or choice == "3" or choice == "9"):
            print("please input a valid choice")
    if choice == "1":
        if p1.canPlay:
            print("which cards do you want to play? LLLLL")
            numberThing = 0
            for i in p1.getHand():
                print(f"Choice {numberThing}: ")

                #print("Choice " + str(numberThing) + ": ")
                print(i.name + " costing " + str(i.cost))
                print(" ")
                numberThing += 1
            choice = input()
            for count in range(len(p1.hand)):
                if choice == str(count):
                    mana = p1.play(mana,count)
        if p2.canPlay:
            print("which cards do you want to play?")
            numberThing = 0
            for i in p2.getHand():
                print("Choice " + str(numberThing) + ": ")
                print(i.name + " costing " + str(i.cost))
                print(" ")
                numberThing += 1
            choice = input()
            for count in range(len(p2.hand)):
                if choice == str(count):
                    mana = p2.play(mana,count)
                
        if (not p2.canPlay) and (not p1.canPlay):
            print("neither of you cannot play right now ((YOU SHOULD NOT BE SEEING THIS MESSAGE))")
        choice = "0"
    elif choice == "2":
        choice = "0"
        for i in p1.board:
            print(i.name)
        print("not implemented")
        #add attacking stuff here, add CanAttack property to minions
    elif choice == "3":
        newGame.newTurn(p1.canPlay)
        print("You have ended your turn")
        choice = "0"
        mana = 10
    elif choice == "9":
        newGame.concede()
        print("You have conceded the game, you lose")
        choice = "0"
    else:
        print("invalid choice")
