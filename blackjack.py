#-------------------------------------------------------------------------------
# Name:        Blackjack
# Purpose:     The Game of Blackjack
#
# Author:      stevb6686
#
# Created:     12/12/2017
# Copyright:   (c) stevb6686 2017
# Licence:     @ Brad S.
#-------------------------------------------------------------------------------
from card import Card
from button import Button
from random import choice, randrange
from graphics import *
#-------------------------------------------------------------------------------

def undrawGraphics(var_dict): # Master undraw function for each window
    for x in var_dict:
        try:
            if x == "deck":
                for card in var_dict[x]:
                    var_dict[x][card].delete()
            else:
                var_dict[x].undraw()
        except:
            continue
    del var_dict

def getWindow(): # Open the containing game window
    win = GraphWin("Blackjack",800,600)
    win.setCoords(0,0,800,600)
    background = Image(Point(400,300), "textures/main_menu.gif")
    background.draw(win)
    return win

#-------------------------------------------------------------------------------

def fileLen(file): # Get the num of lines in a file
    x = 0
    for line in file:
        x += 1
    return x

def getScore(): # Get the player's name and balance
    try:
        data = open("playerdata.txt","r")
        if fileLen(data) == 2:
            data.close()
            data = open("playerdata.txt","r")
            name = data.readline().strip("\n")
            balance = float(data.readline().strip("\n"))
        else:
            name = "User"
            balance = 100.00
        data.close()
        return name, balance
    except:
        return "User", 100.00 # Default name/balance if file is incorrect

#-------------------------------------------------------------------------------

def getInput(win, ntext, btext, name, balance, saveb, cancelb, quitb):
    while True:
        pt = win.getMouse()
        if saveb.clicked(pt):
            try:
                new_name, new_balance = ntext.getText(), btext.getText()
                new_balance = float(new_balance)
                if new_name == "" or len(new_name) > 16:
                    continue
                return new_name, new_balance
            except:
                continue
        elif cancelb.clicked(pt):
            return name, balance
        elif quitb.clicked(pt):
            win.close()
            quit()

def optionWindow(win, name, balance):
    rect_box = Rectangle(Point(200,100), Point(600,500))
    rect_box.setFill(color_rgb(100,100,100))
    rect_box.draw(win)
    title = Text(Point(400,450), "Options")
    title.setSize(26)
    title.setTextColor("white")
    title.draw(win)
    header1 = Text(Point(400,380), "Set Your Name: (16 chr limit)")
    header1.setSize(16)
    header1.setTextColor("white")
    header1.draw(win)
    header2 = Text(Point(400,305), "Set Your Balance:")
    header2.setSize(16)
    header2.setTextColor("white")
    header2.draw(win)
    name_ent = Entry(Point(400,343), 20)
    name_ent.setText(name)
    name_ent.draw(win)
    balance_ent = Entry(Point(400,268), 20)
    balance_ent.setText(balance)
    balance_ent.draw(win)
    saveb = Button(win, Point(300,175), 100, 75, "Save")
    saveb.activate()
    cancelb = Button(win, Point(500,175), 100, 75, "Cancel")
    cancelb.activate()
    quitb = Button(win, Point(755,565), 50, 50, "Quit")
    quitb.activate()
    save_img = Image(Point(300,175), "textures/button_save.gif")
    save_img.draw(win)
    cancel_img = Image(Point(500,175), "textures/button_cancel.gif")
    cancel_img.draw(win)
    quit_img = Image(Point(755,565), "textures/button_quit.gif")
    quit_img.draw(win)
    name, balance = getInput(win, name_ent, balance_ent, name, balance, saveb, cancelb, quitb)
    #exitOption(locals())
    undrawGraphics(locals())
    return name, balance, False, False # Option/game do not run instantly

#-------------------------------------------------------------------------------

def homeScreen(win, name, balance):
    # Display the game homescreen
    title_img = Image(Point(400,450), "textures/title_blackjack.gif")
    title_img.draw(win)
    playb = Button(win, Point(400,300), 150, 90, "Play Game!")
    playb.activate()
    playb_img = Image(Point(400,300), "textures/button_play-game.gif")
    playb_img.draw(win)
    quitb = Button(win, Point(600,300), 150, 90, "Quit Game")
    quitb.activate()
    quitb_img = Image(Point(600,300), "textures/button_quit_main_menu.gif")
    quitb_img.draw(win)
    optionb = Button(win, Point(200,300), 150, 90, "Options")
    optionb.activate()
    optionb_img = Image(Point(200,300), "textures/button_options.gif")
    optionb_img.draw(win)
    statr = Rectangle(Point(200,100), Point(600,200))
    statr.setFill("gray")
    statr.draw(win)
    playert_name = Text(Point(400,165), "Name: {0}".format(name))
    playert_name.setSize(18)
    playert_name.draw(win)
    playert_bal = Text(Point(400,130), "Balance: ${0:0.2f}".format(balance))
    playert_bal.setSize(18)
    playert_bal.draw(win)
    while True: # Click event loop
        pt = win.getMouse()
        if playb.clicked(pt):
            undrawGraphics(locals())
            return True, True, False # 1. Menu, 2. Game, 3. Option
        elif quitb.clicked(pt):
            win.close()
            return False, False, False
        elif optionb.clicked(pt):
            undrawGraphics(locals())
            return True, True, True

#-------------------------------------------------------------------------------

def getVars(win):
    # Create buttons
    hit = Button(win,Point(100,75), 100, 75, "Hit")
    hit.activate()
    hit_img = Image(Point(100,75), "textures/button_hit.gif")
    hit_img.draw(win)
    stand = Button(win, Point(250,75), 100, 75, "Stand")
    stand.activate()
    stand_img = Image(Point(250,75), "textures/button_stand.gif")
    stand_img.draw(win)
    home = Button(win, Point(755,565), 50, 50, "Quit")
    home.activate()
    home_img = Image(Point(755,565), "textures/button_quit.gif")
    home_img.draw(win)
    # Split not activate until doubles
    split = Button(win, Point(400,75), 100, 75, "Split")
    split_img_off = Image(Point(400,75), "textures/button_split_off.gif")
    split_img_off.draw(win)
    # Double not active unless total of 9, 10, or 11 (ORIGINAL CARDS ONLY)
    double = Button(win, Point(550,75), 100, 75, "Double Down")
    double_img_off = Image(Point(550,75), "textures/button_double-down_off.gif")
    double_img_off.draw(win)
    # Insurance not active unless the dealer's face-up card is an ace
    insurance = Button(win, Point(700,75), 100, 75, "Insurance")
    insurance_img_off = Image(Point(700,75), "textures/button_insurance_off.gif")
    insurance_img_off.draw(win)
    playerbox = Rectangle(Point(25,120), Point(775,320))
    playerbox.setOutline("orange")
    playerbox.setWidth(3)
    playerbox.draw(win)
    deck_stack = Image(Point(500,420), "poker_cards/Card Back.gif")
    deck_stack.draw(win)
    return (hit, stand, home, split, double, insurance, playerbox, deck_stack,
            hit_img, stand_img, split_img_off, double_img_off, insurance_img_off, home_img)

def drawStats(win, balance, name):
    stat_box = Rectangle(Point(600,340), Point(780,530))
    stat_box.setFill("white")
    stat_box.draw(win)
    player_name = Text(Point(690,510), name)
    player_name.setSize(16)
    player_name.draw(win)
    balance_text = Text(Point(690,475), "Balance:\n${0:0.2f}".format(balance))
    balance_text.setSize(14)
    balance_text.draw(win)
    bet_text = Text(Point(690,425), "Bet:\n")
    bet_text.setSize(14)
    bet_text.draw(win)
    new_balance = Text(Point(690,375), "New Balance:\nTBD")
    new_balance.setSize(14)
    new_balance.draw(win)
    return stat_box, player_name, balance_text, bet_text, new_balance

def showBet(win):
    bet_win = Rectangle(Point(250, 200), Point(550, 400))
    bet_win.setFill(color_rgb(75,75,75))
    bet_win.draw(win)
    bet_fill = Text(Point(400,355), "Enter your bet:\n(must be within your balance\nand non-negative)")
    bet_fill.setSize(16)
    bet_fill.setTextColor("white")
    bet_fill.draw(win)
    bet_confirm = Button(win, Point(400,250), 75, 50, "Confirm")
    bet_confirm.activate()
    bet_confirm_img = Image(Point(399,250), "textures/button_confirm.gif")
    bet_confirm_img.draw(win)
    bet_value = Entry(Point(400,300), 10)
    bet_value.draw(win)
    return bet_win, bet_fill, bet_confirm, bet_value, bet_confirm_img

def getBet(win, balance, bet_text, home): # Get player bet
    bet_win, bet_fill, bet_confirm, bet_value, bet_confirm_img = showBet(win)
    while True:
        pt = win.getMouse()
        if bet_confirm.clicked(pt):
            try:
                if bet_value.getText() != "":
                    bet = bet_value.getText()
                    bet = round(float(bet),2)
                    if bet > balance or bet <= 0:
                        continue
                    break
            except:
                continue
        elif home.clicked(pt):
            win.close()
            quit()
    undrawGraphics(locals())
    bet_text.setText("Bet:\n${0:0.2f}".format(bet))
    bet_text.draw(win)
    return bet

def checkOption(win, dealer, player, ddeck, pdeck, bet):
    string1 = string2 = string3 = string4 = ""
    # Player blackjack beats all
    if player == 21:
        ddeck["dcard1"].faceup(win)
        ddeck["dcard2"].update(win)
        return "playerblackjack"
    if ddeck["dcard2"].BJValue() == 10: # If the faceup card is a 10 card (any), check for blackjack
        if ddeck["dcard1"].getRank() == 1:
            string1 = "dealerblackjack"
    if ddeck["dcard2"].getRank() == 1: # If the faceup card is an ace, insurance is offered
        string2 = "insurance"
    if pdeck["pcard1"].getRank() == pdeck["pcard2"].getRank(): # If the player has two of the same card, offer a split
        string3 = "split"
    if player >= 9 and player <= 11: # If the player total is 9, 10, or 11, offer doubling down
        string4 = "double"
    return string1 + string2 + string3 + string4

def gameOver(d,p):
    if d >= 21 or p >= 21:
        return True
    else:
        return False

def checkAce(deck, entity):
    ace_count = 0
    for i in range(len(deck)):
        if list(deck.values())[i].getRank() == 1: # If you already have an ace, the next ace has to be worth 1
            ace_count += 1
    # First ace brings total over 21, is 1
    if ace_count == 0:
        if entity[1] + 11 > 21:
            return True
    # First ace brings total to or below 21, is 11
        else:
            return False
    # Not the first ace, is 1
    elif ace_count > 1:
        return True

def checkPastAce(chardeck, entity, value):
    ace_count = 0
    for i in range(len(chardeck)):
        if list(chardeck.values())[i].getRank() == 1:
            ace_count += 1
    if ace_count == 1: # If you have one ace worth 11, make it worth 1
        if (entity[1] + value) > 21:
            return True
    else:
        return False

def setHandValue(card, deck, entity, chardeck, run_once):
    if card.getRank() == 1:       # An ace
        if checkAce(deck, entity):
            value = 1
            run_once = 1
        else:
            value = 11
    else:                         # Any other card
        value = card.BJValue()
    if run_once == 0:
        if checkPastAce(chardeck, entity, value): # Check if a single ace should be changed to a value of 1
            entity[1] = entity[1] + value - 10
            run_once = 1
        else:
            entity[1] = entity[1] + value
    else:
        entity[1] = entity[1] + value
    return entity[1], run_once

def deal(entity, deck, chardeck, x, y, win, current, run_once):
    repick = True
    while repick == True: # Choose a new random card, if it already exists in the deck, repick
        rank = randrange(1,14)
        suit = choice(["d","c","h","s"])
        repick = False
        #deck.values() pertains to the objects that the keys in the dict refer to, check each one
        #for the pontential same name as the created
        for i in range(len(deck)):
            if list(deck.values())[i].getRank() == rank and list(deck.values())[i].getSuit() == suit:
                repick = True
    card = Card(rank, suit, Point(500,420))
    card.draw(win)
    card.facedown(win)
    card.animate(Point(x,y), 0.5, win)
    if not(entity[0] == "dealer" and current == 1):
        card.faceup(win)
    entity[1], run_once = setHandValue(card, deck, entity, chardeck, run_once) # Figues out what blackjack value to add to hand
    x = x + 25
    if entity[0] == "player":
        deck["pcard{0}".format(current)] = card # USE DICTIONARIES TO MAKE VARIABLE NAMES
        chardeck["pcard{0}".format(current)] = card # Also put card in char's deck
    else:
        deck["dcard{0}".format(current)] = card
        chardeck["dcard{0}".format(current)] = card
    current = current + 1
    return entity, x, y, current, run_once

def updateButton(win, split, double, insurance, split_img_off, double_img_off, insurance_img_off):
    split.deactivate()
    double.deactivate()
    insurance.deactivate()
    try:
        split_img_off.draw(win)
    except:
        split_img_off.undraw()
        split_img_off.draw(win)
    try:
        double_img_off.draw(win)
    except:
        double_img_off.undraw()
        double_img_off.draw(win)
    try:
        insurance_img_off.draw(win)
    except:
        insurance_img_off.undraw()
        insurance_img_off.draw(win)

def checkSplits(player, player2, dealer):
    if dealer > 21: # Both hands win by dealer bust
        return -3
    elif player > 21 and player2 > 21: # Both hands lose by bust
        return -2
    elif dealer > player and dealer > player2: # Both hands lose by value
        return -2
    elif (player > 21 and player2 > dealer) or (player2 > 21 and player > dealer): # One win, one loss by one hand bust
        return -1
    elif (player > 21 and player2 < dealer) or (player2 > 21 and player < dealer): # One loss, one loss by bust
        return -2
    elif player > dealer and player2 > dealer: # Both hands win by value
        return -3
    elif (player > dealer and player2 < dealer) or (player2 > dealer and player < dealer): # One win, one loss
        return -1
    elif player == dealer and player2 == dealer: # Double push
        return dealer
    elif (player == dealer and player2 > 21) or (player2 == dealer and player > 21): # One push, one loss
        return -5
    elif (player == dealer and player2 > dealer) or (player2 == dealer and player > dealer): # One push, one win
        return -4
    elif (player == dealer and player2 < dealer) or (player2 == dealer and player < dealer): # One push, one loss
        return -5
    elif player > 21 or player2 > 21: # One hand loses by bust
        return -1

def callSplit(win, bet, balance, deck, pdeck, pcurrent):
    pdeck2 = {} # Second player split hand
    run_once_player = 0
    run_once_player2 = 0
    player = ["player", pdeck["pcard1"].BJValue()]
    player2 = ["player",0]
    py = 220
    px = 125
    px2 = 425
    # Second card becomes first card of new deck
    pdeck["pcard2"].animate(Point(400,220), 1, win)
    pdeck2["pcard1"] = pdeck["pcard2"]
    del pdeck["pcard2"]
    deck["pcard3"] = pdeck2["pcard1"]
    player2 = ["player", pdeck2["pcard1"].BJValue()]
    # Add cards to both hands
    pcurrent = 2
    player, px, py, pcurrent, run_once_player = deal(player, deck, pdeck, px, py, win, pcurrent, run_once_player)
    pcurrent = 4
    player2, px2, py, pcurrent, run_once_player2 = deal(player2, deck, pdeck2, px2, py, win, pcurrent, run_once_player2)
    return pdeck, pdeck2, player, player2, bet, balance

def callDoubleDown(bet, bet_text):
    bet = bet * 2
    bet_text.setText("Bet:\n${0:0.2f}".format(bet))
    return bet

def callInsurance(win, bet, ddeck, home, balance, new_balance):
    # Insurance must be half the bet
    ins_box = Rectangle(Point(250, 200), Point(550, 400))
    ins_box.setFill(color_rgb(75,75,75))
    ins_box.draw(win)
    ins_text = Text(Point(400,330), "")
    ins_text.setSize(14)
    ins_text.setTextColor("white")
    ins_text.draw(win)
    ins_confirm = Button(win, Point(400,250), 75, 50, "Confirm")
    ins_confirm.activate()
    ins_confirm_img = Image(Point(400,250), "textures/button_confirm.gif")
    ins_confirm_img.draw(win)
    if ddeck["dcard1"].BJValue() == 10: # If the facedown card is a 10, insurance is paid out
        ddeck["dcard1"].faceup(win) # If dealer blackjack, insurance paid out 2:1
        ins_text.setText("Dealer has blackjack!\nInsurance paid out 1:1.\n(+${0}) Balance unchanged.".format(bet))
        ins = bet
    else:
        ins = bet/2 # If not dealer blackjack, insurance is lost. Bet is not changed. Taken from new balance
        ins_text.setText("Dealer does not have blackjack.\nInsurance (-${0}) lost.\n(Taken from new balance)".format(ins))
        balance = balance - ins
        new_balance.setText("New Balance:\n${0:0.2f}".format(balance))
    while True:
        pt = win.getMouse()
        if ins_confirm.clicked(pt):
            undrawGraphics(locals())
            new_balance.draw(win)
            return ins, balance
        elif home.clicked(pt):
            win.close()
            quit()

def endScreen(win):
    rectbar = Rectangle(Point(300,325), Point(800,540))
    rectbar.setFill(color_rgb(75,75,75))
    rectbar.draw(win)
    cont = Button(win, Point(380,375), 100, 75, "Continue")
    cont.activate()
    cont_img = Image(Point(380,375), "textures/button_continue_big.gif")
    cont_img.draw(win)
    backhome = Button(win, Point(515, 375), 100, 75, "Home")
    backhome.activate()
    backhome_img = Image(Point(515, 375), "textures/button_main-menu.gif")
    backhome_img.draw(win)
    return cont, backhome, rectbar, cont_img, backhome_img

def getBalance(win, player, dealer, deck, balance, bet):
    endtext = Text(Point(455, 475), "")
    endtext.setSize(22)
    endtext.setTextColor("white")
    endtext.draw(win)
    if player == dealer and not(player == 21 or dealer == 21):
        endtext.setText("Push!\nBet Returned.\nBalance Unchanged.")
    elif player == -1:
        endtext.setText("Player Wins One\nHalf Of The Split.\nBalance Unchanged.")
    elif player == -2:
        balance = balance - bet*2
        endtext.setText("Player Loses\nBoth Splits.\n(-${0:0.2f})".format(bet*2))
    elif player == -3:
        balance = balance + bet*2
        endtext.setText("Player Wins\nBoth Splits!\n(+${0:0.2f})".format(bet*2))
    elif player == -4:
        balance = balance + bet
        endtext.setText("Player Push/\nWins A split.\n(+${0:0.2f})".format(bet))
    elif player == -5:
        balance = balance - bet
        endtext.setText("Player Push/\nLoses A split.\n(-${0:0.2f})".format(bet))
    elif player == 21 and len(deck) == 4:
        balance = balance + bet*2
        endtext.setText("Player Blackjack!\n2:1 Bet Return!\n(+${0:0.2f})".format(bet*2))
    elif dealer == 21 and len(deck) == 4 and bet == 0:
        endtext.setText("Insurance paid!\n2:1 Insurance Return.\nBalance Unchanged")
    elif dealer == 21 and len(deck) == 4:
        balance = balance - bet
        endtext.setText("Dealer Blackjack.\nBet Lost!\n(-${0:0.2f})".format(bet))
    elif player == 21:
        balance = balance + bet
        endtext.setText("Player Natural!\nBet Return!\n(+${0:0.2f})".format(bet))
    elif dealer == 21:
        balance = balance - bet
        endtext.setText("Dealer Natural.\nBet Lost!\n(-${0:0.2f})".format(bet))
    elif player > 21:
        balance = balance - bet
        endtext.setText("Player Bust.\nBet Lost!\n(-${0:0.2f})".format(bet))
    elif dealer > 21:
        balance = balance + bet
        endtext.setText("Dealer Bust!\nBet Return!\n(+${0:0.2f})".format(bet))
    elif player > dealer:
        balance = balance + bet
        endtext.setText("Player win!\nBet Return!\n(+${0:0.2f})".format(bet))
    elif dealer > player:
        balance = balance - bet
        endtext.setText("Dealer win.\nBet Lost!\n(-${0:0.2f})".format(bet))
    return balance, endtext

def redrawStats(win, a, b, c, d, e, balance):
    for var in locals().values():
        if var == win:
            continue
        elif var == balance:
            continue
        elif var == e:
            e.setText("New Balance:\n${0:0.2f}".format(balance))
            e.undraw()
            e.draw(win)
        else:
            var.undraw()
            var.draw(win)

def gameScreen(win, name, balance):  # Master game function
    (hit, stand, home, split, double, insurance, playerbox, deck_stack,
     hit_img, stand_img, split_img_off, double_img_off, insurance_img_off, home_img) = getVars(win)
    game = True # Whether to return to home or not
    deck = {} # List of cards currently in play
    pdeck = {} # List of cards in player's hand
    ddeck = {} # List of cards in dealer's hand
    run_once_player = 0 # hasAce variable to make an ace worth 11 only once
    run_once_player2 = 0
    run_once_dealer = 0
    dealer = ["dealer",0]
    player = ["player",0] # Scores for player hand (split hand is created after)
    pcurrent = 1
    dcurrent = 1
    px = 100 # Starting point values
    py = 220
    dx = 100
    dy = 420
    sp_num = 0 # Split value
    stat_box, player_name, balance_text, bet_text, new_balance = drawStats(win, balance, name)
    bet = getBet(win, balance, bet_text, home) # Betting box
    #------------GAME LOOP------------------------------------------------------
    while (not gameOver(dealer[1], player[1])) or (sp_num >= 1):
        if dcurrent == 1: # Initial 4 card deal
            time.sleep(0.25)
            for i in range(2):
                player, px, py, pcurrent, run_once_player = deal(player, deck, pdeck, px, py, win, pcurrent, run_once_player)
                dealer, dx, dy, dcurrent, run_once_dealer = deal(dealer, deck, ddeck, dx, dy, win, dcurrent, run_once_dealer)
                if pcurrent == 2:
                    deck["dcard1"].facedown(win)
            option = checkOption(win, dealer[1], player[1], ddeck, pdeck, bet)
            if option == "playerblackjack" or option == "dealerblackjack":
                break
            if option.count("insurance") == 1:
                insurance.activate()
                insurance_img = Image(Point(700,75), "textures/button_insurance.gif")
                insurance_img.draw(win)
            if option.count("split") == 1:
                split.activate()
                split_img = Image(Point(400,75), "textures/button_split.gif")
                split_img.draw(win)
            if option.count("double") == 1:
                double.activate()
                double_img = Image(Point(550,75), "textures/button_double-down.gif")
                double_img.draw(win)
        #--------------------------PLAYER TURN----------------------------------
        pt = win.getMouse()
        if hit.clicked(pt): #SP_NUM is a *split* varaible
            updateButton(win, split, double, insurance, split_img_off, double_img_off, insurance_img_off)
            if sp_num == 0:
                player, px, py, pcurrent, run_once_player = deal(player, deck, pdeck, px, py, win, pcurrent, run_once_player)
                split.deactivate()
                insurance.deactivate()
            else:
                player2, px, py, pcurrent, run_once_player2 = deal(player2, deck, pdeck2, px, py, win, pcurrent, run_once_player2)
        elif stand.clicked(pt):
            updateButton(win, split, double, insurance, split_img_off, double_img_off, insurance_img_off)
            if not "pdeck2" in locals():
                deck["dcard1"].faceup(win)
                deck["dcard2"].update(win)
                while dealer[1] < 17:
                    dealer, dx, dy, dcurrent, run_once_dealer = deal(dealer, deck, ddeck, dx, dy, win, dcurrent, run_once_dealer)
                break
            elif sp_num == 1: # Player stands on the last hand, dealer goes
                deck["dcard1"].faceup(win)
                deck["dcard2"].update(win)
                while dealer[1] < 17:
                    dealer, dx, dy, dcurrent, run_once_dealer = deal(dealer, deck, ddeck, dx, dy, win, dcurrent, run_once_dealer)
                player[1] = checkSplits(player[1], player2[1], dealer[1])
                break
            else: # Player stands and does not bust, moves on to next hand
                sp_num = 1
                px = 450
                run_once_player = 0
                run_once_player2 = 0
        elif split.clicked(pt):
            updateButton(win, split, double, insurance, split_img_off, double_img_off, insurance_img_off)
            pdeck, pdeck2, player, player2, bet, balance = callSplit(win, bet, balance, deck, pdeck, pcurrent)
            if pdeck["pcard1"].getRank() == 1:
                player[1] = player[1] + 10
                player2[1] = player2[1] + 10
            pcurrent = 5
        elif double.clicked(pt):
            updateButton(win, split, double, insurance, split_img_off, double_img_off, insurance_img_off)
            bet = callDoubleDown(bet, bet_text)
        elif insurance.clicked(pt):
            updateButton(win, split, double, insurance, split_img_off, double_img_off, insurance_img_off)
            ins, balance = callInsurance(win, bet, ddeck, home, balance, new_balance)
            if ins == bet: # If the insurance is successful, break with same money
                bet = 0
                break
            # If insurance not successful, lose insurance and continue
        elif home.clicked(pt):
            win.close()
            quit()
        if "pdeck2" in locals(): # If a split has happened, player bust continues to next hand
            if gameOver(dealer[1], player[1]) and sp_num == 0: # Bust with first hand
                sp_num = 1
                px = 450
                run_once_player = 0
                run_once_player2 = 0
            if gameOver(dealer[1], player2[1]) and sp_num >= 1: # Bust with second hand
                player[1] = checkSplits(player[1], player2[1], dealer[1])
                break
    #-----------------------------GAME END--------------------------------------
    if not ddeck["dcard1"].getFace():
        ddeck["dcard1"].faceup(win)
        for x in ddeck.values():
            x.update(win)
    cont, backhome, rectbar, cont_img, backhome_img = endScreen(win)
    balance, endtext = getBalance(win, player[1], dealer[1], deck, balance, bet)
    redrawStats(win, stat_box, player_name, balance_text, bet_text, new_balance, balance)
    while True:
        pt = win.getMouse()
        if backhome.clicked(pt):
            game = False
            break
        elif cont.clicked(pt):
            break
        elif home.clicked(pt):
            win.close()
            quit()
    undrawGraphics(locals())
    return balance, game

#-------------------------------------------------------------------------------

def recordScore(name, balance):
    data = open("playerdata.txt", "w")
    name = str(name).replace("\n","")
    balance = str(balance).replace("\n","")
    data.write("{0}\n{1}".format(name, balance))
    data.close()

#-------------------------------------------------------------------------------

def main():
    """ This program simulates the Casino game of Blackjack, otherwise known
    as 21. Created by Brad Stevanus for the ICS4UI class of 2018 """
    try:
        print("Launched Blackjack.")
        home = True # Home always runs
        option = False # Option runs if you click options
        win = getWindow()
        name, balance = getScore() # Get paramter to login with new player before opening file later
        while home == True:
            home, game, option = homeScreen(win, name, balance)
            if option == True:
                name, balance, option, game = optionWindow(win, name, balance)
            while game == True:
                if balance < 10: # Minimum balance of $10 to start the game
                    balance = 10
                balance, game = gameScreen(win, name, balance)
        recordScore(name, balance) # Record new scores / quit under "name"
        win.close()
        print("Blackjack terminated. Progress Saved!")
    except:
        print("Blackjack terminated. Data may be lost.")

if __name__ == "__main__":
    main()
