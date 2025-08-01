#!/usr/bin/python3
import blackjack_solver_helper
import random
import sys

numDecks = 6
deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"] * numDecks * 4
playerHand = []
dealerHand = []
# key:value == [(playerHand),dealerhand]:EV  ex: [("A","T"),3]: 1.5
# eachHandDict = blackjack_solver_helper.eachHandDict
dealerNumOddsDict = {16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0}


def calcEVOfDeck(deck):
    possibilities = len(deck) * (len(deck) - 1) * (len(deck) - 2)
    retEV = 0
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    for p1 in cards:
        for p2 in cards:
            for d1 in cards:
                p1count = deck.count(p1)
                p2count = deck.count(p2)
                d1count = deck.count(d1)
                if p1 == p2:
                    p2count -= 1
                if p2 == d1:
                    d1count -= 1
                if p1 == d1:
                    d1count -= 1
                if handSum([p1]) == 10:
                    p1 = "T"
                if handSum([p2]) == 10:
                    p2 = "T"
                if handSum([d1]) == 10:
                    d1 = "T"
                if handSum(p1) < handSum(p2):
                    retEV += eachHandDict[(p1, p2), d1] * p1count * p2count * d1count
                else:
                    retEV += eachHandDict[(p2, p1), d1] * p1count * p2count * d1count
    return retEV / possibilities


def calcBestBet(deck, totalCash):
    # assumes above function works correctly
    deckEV = calcEVOfDeck(deck)
    if deckEV <= 0.5:
        return 1


def trashCards(card):
    deck.remove(card)


def dealPlayer(card):
    global playerHand
    playerHand += card
    deck.remove(card)


def dealDealer(card):
    global dealerHand
    dealerHand += card
    deck.remove(card)


def dealCardsOut():
    dealDealer(random.choice(deck))
    dealPlayer(random.choice(deck))
    dealPlayer(random.choice(deck))


def printHands():
    None
    print("Player Hand:", playerHand, "Sum:", handSum(playerHand))
    print("Dealer Hand:", dealerHand, "Sum:", handSum(dealerHand))


def calcOddsWinning(deck, eachHandDict):
    numCombinations = 0
    winningOdds = 0
    for inx1 in len(deck):
        for inx2 in len(deck):
            for inx3 in len(deck):
                if inx1 != inx2 and inx2 != inx3 and inx1 != inx3:
                    winningOdds += eachHandDict[(deck[inx1], deck[inx2]), deck[inx3]]
                    numCombinations += 1
    return winningOdds / numCombinations


def handSum(handList):
    sum = 0
    for card in handList:
        if card == "A":
            sum += 1
        elif card == "T" or card == "K" or card == "Q" or card == "J":
            sum += 10
        else:
            sum += int(card)
    if "A" in handList and sum <= 11:
        sum += 10
    return sum


# if we were to hit, we would re-calculate after hitting


def normalizeDict(dictToNormalize, divideBy=0):
    retDict = {}
    if divideBy == 0:
        for key, value in dictToNormalize.items():
            divideBy += value
    for key, value in dictToNormalize.items():
        retDict[key] = float(value) / divideBy
    return retDict


def dealerOdds(deck, dealerHand, multiplier=1.0):
    global dealerNumOddsDict
    for c1 in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]:
        if (
            handSum(dealerHand + [c1]) < 17
            or (handSum(dealerHand + [c1]) == 17 and "A" in dealerHand)
        ) and len(dealerHand) <= 4:
            mockDeck = deck[:]
            mockDeck.remove(c1)
            dealerOdds(
                mockDeck, dealerHand + [c1], multiplier * deck.count(c1) / len(deck)
            )
        else:
            sum = handSum(dealerHand + [c1])
            dealerNumOddsDict[min(max(16, sum), 22)] += (
                deck.count(c1) / len(deck) * multiplier
            )
    dealerNumOddsDict[16] = 0
    return normalizeDict(dealerNumOddsDict)


def compareNumOdds(dealerDict, playerDict):
    playerOddsOfWinning = 0
    for dealerNum in range(16, 23):
        for playerNum in range(16, 23):
            if playerNum == 22:
                None
            elif dealerNum == 22:
                playerOddsOfWinning += dealerDict[dealerNum] * playerDict[playerNum]
            elif playerNum > dealerNum:
                playerOddsOfWinning += dealerDict[dealerNum] * playerDict[playerNum]
            elif playerNum == dealerNum:
                playerOddsOfWinning += (
                    dealerDict[dealerNum] * playerDict[playerNum] * 0.5
                )
    return playerOddsOfWinning


def oddsBtwTwo(dealerOddsDict, lowerBound, upperBound):
    retOdds = 0
    retOdds += dealerOddsDict[lowerBound] * 0.5
    retOdds -= dealerOddsDict[upperBound] * 0.5
    for num in range(lowerBound + 1, upperBound):
        retOdds += dealerOddsDict[num]
    return retOdds


def oddsOfWinningWithHit(deck, playerHand, dealerHand):
    dealerNumOddsDict = dealerOdds(deck, dealerHand)
    playerHitOdds = {16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0}
    for card in deck:
        sum = handSum(playerHand + [card])
        playerHitOdds[min(max(16, sum), 22)] += 1
    playerHitOdds = normalizeDict(playerHitOdds)
    return compareNumOdds(dealerNumOddsDict, playerHitOdds)


def oddsOfWinningWithStand(deck, playerHand, dealerHand):
    dealerNumOddsDict = dealerOdds(deck, dealerHand)
    standNumOdds = {16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0}
    standNumOdds[min(max(16, handSum(playerHand)), 22)] += 1
    return compareNumOdds(dealerNumOddsDict, standNumOdds)


def oddsOfWinningWithSplit(deck, playerHand, dealerHand):
    standEV = 0
    hitEV = 0
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    cards.remove(playerHand[0])
    for card in cards:
        standEV += (
            oddsOfWinningWithStand(deck, [playerHand[0]] + [card], dealerHand)
            * deck.count(card)
            / len(deck)
        )
        hitEV += (
            oddsOfWinningWithHit(deck, [playerHand[0]] + [card], dealerHand)
            * deck.count(card)
            / len(deck)
        )
    return max(standEV, hitEV) * len(deck) / (len(deck) - deck.count(playerHand[0]))


def findHitEV(deck, playerHand, dealerHand):
    hitEV = 0
    for card in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]:
        if card in deck:
            oneHitEV = oddsOfWinningWithHit(deck, playerHand + [card], dealerHand)
            oneStandEV = oddsOfWinningWithStand(deck, playerHand + [card], dealerHand)
            # if diff btw stand and hit is insurmountable
            if oneHitEV * 4 < oneStandEV or oneStandEV == 0 or len(playerHand) >= 3:
                hitEV += max(oneStandEV, oneHitEV) * deck.count(card) / len(deck)
            else:  # see if extra hit may help in some cases
                newDeck = deck[:]
                newDeck.remove(card)
                hitEV += (
                    max(findHitEV(newDeck, playerHand + [card], dealerHand), oneStandEV)
                    * deck.count(card)
                    / len(deck)
                )
    return hitEV


# print(oddsOfWinningWithHit(deck, dealerOdds(deck, ["T"]), ["Q", "K"]))
# print(oddsOfWinningWithStand(dealerOdds(deck, ["T"]), ["Q", "K"]))


def calcBestMove(deck, playerHand, dealerHand, doubleValue=1):
    if handSum(playerHand) == 21 and len(playerHand) == 2:
        return ["stand", 1.5 * doubleValue]
    if handSum(playerHand) < 8:
        return ["hit", oddsOfWinningWithHit(deck, playerHand, dealerHand)]
    # stand is easy
    # double is easy
    dealerDict = dealerOdds(deck, dealerHand)
    standEV = oddsOfWinningWithStand(deck, playerHand, dealerHand)
    # print("standEV:", standEV)

    doubleEV = oddsOfWinningWithHit(deck, playerHand, dealerHand)
    # standDealerOdds = doubleDealerOdds
    # doubleOdds have NOT been adjusted to account for added Reward
    # print("doubleEV:", doubleEV)

    # go three times depth for the purposes of deciding between and double
    # rerun if hit is decided to be optimal
    hitEV = 0
    if doubleEV > standEV and doubleEV <= 0.5:
        hitEV = doubleEV + 0.0
    elif doubleEV * 2 > standEV:
        hitEV = findHitEV(deck, playerHand, dealerHand)
    splitEV = 0
    if len(playerHand) == 2 and playerHand[0] == playerHand[1]:
        if playerHand == ["A", "A"]:
            return ["split", 0.5]
        splitEV = oddsOfWinningWithSplit(deck, playerHand, dealerHand)
        # print("splitEV:", splitEV)
        # print("standEV:", standEV)
        # print("hitEV:", hitEV)
        # print("doubleEV:", doubleEV)
    if len(playerHand) != 2:
        doubleEV = 0
    print("splitEV:", splitEV)
    print("standEV:", standEV)
    print("hitEV:", hitEV)
    print("doubleEV:", doubleEV)
    standEV = standEV - 0.5
    hitEV = hitEV - 0.5
    doubleEV = 2 * (doubleEV - 0.5)
    splitEV = 2 * (splitEV - 0.5)
    bestEV = max(standEV, hitEV, doubleEV, splitEV)
    maxPayout = bestEV * doubleValue * 2
    if maxPayout == 2 * standEV or maxPayout == 2 * hitEV:
        maxOdds = bestEV + 0.5
    else:
        maxOdds = bestEV / 2 + 0.5
    # print("bestEV:", bestEV)
    # print("splitEV:", splitEV)
    # print("standEV:", standEV)
    # print("hitEV:", hitEV)
    # print("doubleEV:", doubleEV)
    print("Odds of Winning Best Move:", maxOdds, "Expected Payout:", maxPayout)
    if standEV == bestEV:
        return ["stand", maxPayout]
    elif hitEV == bestEV:
        return ["hit", maxPayout]
    elif doubleEV == bestEV:
        return ["double", maxPayout]
    elif splitEV == bestEV:
        return ["split", maxPayout]
    return "Error!"


# function,time to run with full deck
# dealerOdds, 0.00415
# findHitEV, 0.142
# calcBestMove, 0.22
numGames = 0
totalWinnings = 0
totalWins = 0
totalLosses = 0
actualPlayerDict = {}
actualDealerDict = {}
# print(findHitEV(deck, ['7', 'T'], ['A']))
# print(calcBestMove(deck, ['7', 'T'], ['A']))
# while True:
#     deck = ['A', '2', '3', '4', '5', '6', '7',
#             '8', '9', 'T', 'J', 'Q', 'K']*numDecks*4
#     while (len(deck) > 103):
#         playerHand = []
#         dealerHand = []
#         deckEV = calcEVOfDeck(deck)
#         if (deckEV < 0.51):
#             bet = 1
#         elif (deckEV < 0.52):
#             bet = 5
#         elif (deckEV < 0.53):
#             bet = 20
#         elif (deckEV < 0.54):
#             bet = 44
#         elif (deckEV < 0.55):
#             bet = 77
#         elif (deckEV < 0.56):
#             bet = 118
#         elif (deckEV < 0.57):
#             bet = 168
#         elif (deckEV < 0.58):
#             bet = 226
#         elif (deckEV < 0.59):
#             bet = 296
#         elif (deckEV < 0.60):
#             bet = 365
#         elif (deckEV < 0.61):
#             bet = 450
#         else:
#             bet = 1000
#         print("deckEV:", deckEV, "bet:", bet)
#         dealCardsOut()
#         playerDone = False
#         playerDouble = 1
#         printHands()
#         while (playerDone != True and handSum(playerHand) < 18 and (not "A" in playerHand or handSum(playerHand) != 21)):
#             playerBestMove = calcBestMove(
#                 deck, playerHand, dealerHand, playerDouble)[0]
#             print("Player Best Move:", playerBestMove)
#             sys.stdout.flush()
#             if playerBestMove == "stand":
#                 playerDone = True
#             elif playerBestMove == "double":
#                 dealPlayer(random.choice(deck))
#                 playerDone = True
#                 playerDouble *= 2
#             elif playerBestMove == "hit":
#                 dealPlayer(random.choice(deck))
#             elif playerBestMove == "split":
#                 playerHand = playerHand[:1]
#                 dealPlayer(random.choice(deck))
#                 playerDouble *= 2
#             print("Player Hand:", playerHand, "Sum:", handSum(playerHand))
#         while handSum(dealerHand) < 17 or (handSum(dealerHand) == 17 and "A" in dealerHand):
#             print("Dealer Hand:", dealerHand, "Sum:", handSum(dealerHand))
#             dealDealer(random.choice(deck))
#         print("Dealer Hand:", dealerHand, "Sum:", handSum(dealerHand))
#         if handSum(playerHand) > 21:
#             totalWinnings -= playerDouble * bet
#             totalLosses += playerDouble * bet
#         elif (len(playerHand) == 2 and handSum(playerHand) == 21 and (handSum(dealerHand) != 21 and len(dealerHand) == 2)):
#             totalWinnings += 1.5 * playerDouble * bet
#             totalWins += 1.5 * playerDouble * bet
#         elif handSum(dealerHand) > 21:
#             totalWinnings += playerDouble * bet
#             totalWins += playerDouble * bet
#         elif handSum(dealerHand) == handSum(playerHand):
#             totalWins += 0.5 * playerDouble*bet
#             totalLosses += 0.5 * playerDouble*bet
#         elif handSum(playerHand) > handSum(dealerHand):
#             totalWinnings += playerDouble * bet
#             totalWins += playerDouble * bet
#         else:
#             totalWinnings -= playerDouble * bet
#             totalLosses += playerDouble * bet
#         try:
#             actualPlayerDict[min(max(16, handSum(playerHand)), 22)] += 1
#             actualDealerDict[min(max(16, handSum(dealerHand)), 22)] += 1
#         except:
#             actualPlayerDict[min(max(16, handSum(playerHand)), 22)] = 1
#             actualDealerDict[min(max(16, handSum(dealerHand)), 22)] = 1
#         numGames += 1
#         print("bet:", bet*playerDouble)
#         print("Game:", numGames, "Winnings:", totalWinnings,
#               "Wins:", totalWins, "Losses:", totalLosses, "deck length:", len(deck))
#         if numGames % 100 == 0:
#             print("Player Hands", normalizeDict(actualPlayerDict))
#             print("Dealer Hands", normalizeDict(actualDealerDict))
#         print("")
#         sys.stdout.flush()

eachHandDict = {}


def createEachHandDict(deck):
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T"]
    for inxp1 in range(10):
        for inxp2 in range(inxp1, 10):
            for inxd1 in range(10):
                p1 = cards[inxp1]
                p2 = cards[inxp2]
                d1 = cards[inxd1]
                splitOdds = -1
                if handSum([p1, p2]) == 21:
                    dealerOddsDict = dealerOdds(deck, [d1])
                    eachHandDict[(p1, p2), d1] = 1.5 - dealerOddsDict[21]
                    break
                elif p1 == p2:
                    splitOdds = oddsOfWinningWithSplit(deck, [p1, p2], [d1])
                standOdds = oddsOfWinningWithStand(deck, [p1, p2], [d1])
                doubleOdds = oddsOfWinningWithHit(deck, [p1, p2], [d1])
                if standOdds > 2 * doubleOdds:
                    if splitOdds * 4 - 2 > standOdds * 2 - 1:
                        eachHandDict[(p1, p2), d1] = "split"
                    else:
                        eachHandDict[(p1, p2), d1] = "stand"

                elif splitOdds > 2 * doubleOdds:
                    if splitOdds * 4 - 2 > standOdds * 2 - 1:
                        eachHandDict[(p1, p2), d1] = "split"
                    else:
                        eachHandDict[(p1, p2), d1] = "stand"
                else:
                    hitOdds = findHitEV(deck, [p1, p2], [d1])
                    if hitOdds * 2 - 1 == max(
                        splitOdds * 4 - 2,
                        hitOdds * 2 - 1,
                        standOdds * 2 - 1,
                        doubleOdds * 4 - 2,
                    ):
                        eachHandDict[(p1, p2), d1] = "hit"
                    elif standOdds * 2 - 1 == max(
                        splitOdds * 4 - 2,
                        hitOdds * 2 - 1,
                        standOdds * 2 - 1,
                        doubleOdds * 4 - 2,
                    ):
                        eachHandDict[(p1, p2), d1] = "stand"
                    elif doubleOdds * 4 - 2 == max(
                        splitOdds * 4 - 2,
                        hitOdds * 2 - 1,
                        standOdds * 2 - 1,
                        doubleOdds * 4 - 2,
                    ):
                        eachHandDict[(p1, p2), d1] = "double"
                    else:
                        eachHandDict[(p1, p2), d1] = "split"
        print("1")
        sys.stdout.flush()
    print(eachHandDict)
    sys.stdout.flush()


print(findHitEV(deck, ["T", "6"], ["7"]))
# mockArray = sorted(eachHandDict.items(), key=lambda x: x[1], reverse=True)
# print(mockArray)
