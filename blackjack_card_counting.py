#!/usr/bin/python3
import random
import blackjack_solver as bjs
import blackjack_solver_helper
playerHand = []
dealerHand = []
deck = ['A', '2', '3', '4', '5', '6', '7',
        '8', '9', 'T', 'J', 'Q', 'K'] * 24


def dealCards(deck):
    c1 = random.choice(deck)
    c2 = random.choice(deck)
    c3 = random.choice(deck)
    deck.remove(c1)
    deck.remove(c2)
    deck.remove(c3)
    playerHand = [c1, c2]
    dealerHand = [c3]


def findCount(deck):
    count = 0.0
    for card in deck:
        if bjs.handSum([card]) >= 10:
            count += 1
        elif bjs.handSum([card]) <= 6:
            count -= 1
    return count / len(deck)


userChoice = blackjack_solver_helper.eachHandActionDict
print(userChoice)


def playGame(deck, n=-1):
    if len(deck) < 103:
        deck = ['A', '2', '3', '4', '5', '6', '7',
                '8', '9', 'T', 'J', 'Q', 'K'] * 24
    global userChoice
    userChoice[bjs.handSum(dealerHand), playerHand]
    if n > 0:
        playGame(deck, n-1)
    else:
        playGame(deck, n)


print(findCount(deck))
