#-------------------------------------------------------------------------------
# Name:        card
# Purpose:     Card class for Blackjack
#
# Author:      Brad Stevanus
#
# Created:     20/12/2017
# Copyright:   (c) stevb6686 2017
# Licence:     @ Brad S.
#-------------------------------------------------------------------------------

from graphics import *

class Card:

    """A card class that represents a card from the standard poker deck"""

    def __init__(self, rank, suit, center):

        """Creates a card with rank being an int representing Ace - King (1-13)
        and suit being a one letter string representing
        diamonds, clubs, hearts, or spades (d,c,h,s)"""

        self.rank = rank
        self.suit = suit
        self.center = center
        self.x, self.y = self.center.getX(), self.center.getY()
        self.xmin = self.x - 63 # Rounded width/2 of the image
        self.xmax = self.x + 63
        self.ymin = self.y - 91 # Round height/2 of the image
        self.ymax = self.y + 91
        self.p1 = Point(self.xmin,self.ymin)
        self.p2 = Point(self.xmax,self.ymax)
        self.name = self.__str__()
        self.image = "poker_cards/{0}.gif".format(self.name)
        self.showface = True

    def getRank(self):
        "Returns the rank of a card"
        return self.rank

    def getSuit(self):
        "Returns the suit of a card"
        return self.suit

    def getCenter(self):
        "Returns the center point of a card"
        return self.center

    def getFace(self):
        "Returns the faceup value of a card"
        return self.showface

    def setRank(self, rank):
        "Sets the rank of a card"
        self.rank = rank

    def setSuit(self, suit):
        "Sets the suit of a card"
        self.suit = suit

    def BJValue(self):
        "Returns the Blackjack value of a card"
        if self.rank <= 10:
            return self.rank
        else:
            return 10

    def __str__(self):
        "Returns a string that displays the name of the card"
        drank = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"][self.rank-1]
        dsuit = {"d": "Diamonds", "c": "Clubs", "h": "Hearts", "s": "Spades"}[self.suit.lower()]
        return "{0} of {1}".format(drank,dsuit)

    def draw(self, win):
        "Draws the respective cardface to a graphical window"
        self.cardface = Image(self.center,self.image)
        self.cardface.draw(win)

    def delete(self):
        "Undraws the cardface and delets the object"
        self.cardface.undraw()
        del self

    def update(self, win):
        self.cardface.undraw()
        self.cardface.draw(win)

    def move(self, dx, dy):
        "Moves the card object in a graphical window"
        self.cardface.move(dx,dy)
        self.center = Point(self.x + dx, self.y + dy)
        self.x, self.y = self.center.getX(), self.center.getY()
        self.xmin = self.x - 63 # Rounded width/2 of the image
        self.xmax = self.x + 63
        self.ymin = self.y - 91 # Round height/2 of the image
        self.ymax = self.y + 91
        self.p1 = Point(self.xmin,self.ymin)
        self.p2 = Point(self.xmax,self.ymax)

    def faceup(self, win):
        "Sets the card to face up"
        if self.showface == False:
            self.cardface.undraw()
            self.cardface = Image(self.center, self.image)
            self.cardface.draw(win)
        self.showface = True

    def facedown(self, win):
        "Sets the card to face down"
        if self.showface == True:
            self.cardface.undraw()
            self.cardface = Image(self.center, "poker_cards/Card Back.gif")
            self.cardface.draw(win)
        self.showface = False

    def animate(self, point, t, win):
        dx = point.getX() - self.center.getX()
        dy = point.getY() - self.center.getY()
        movx = dx/(t*20)
        movy = dy/(t*20)
        while not(self.x == point.getX() and self.y == point.getY()):
            self.move(movx, movy)
            time.sleep(0.016)
