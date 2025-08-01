import random
digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
operations = ['+', '-', '*', '/']
bestDigitsArray = []
bestOperationsArray = []
bestDiff = 362881


def findApp(idealNum, numLoops=100000000000):
    global bestDiff, bestDigitsArray, bestOperationsArray
    # for d1 in digits:
    #     for d2 in digits:
    #         for d3 in digits:
    #             for d4 in digits:
    #                 for d5 in digits:
    #                     for d6 in digits:
    #                         for o1 in operations:
    #                             for o2 in operations:
    #                                 for o3 in operations:
    #                                     for o4 in operations:
    #                                         for o5 in operations:
    #                                             possDigitsArray = [
    #                                                 d1, d2, d3, d4, d5, d6]
    #                                             possOperationsArray = [
    #                                                 o1, o2, o3, o4, o5]
    for _ in range(numLoops):
        # if _ % 1000:
        #     print(_)
        possDigitsArray = [random.choice(digits), random.choice(digits), random.choice(
            digits), random.choice(digits), random.choice(digits), random.choice(digits)]
        possOperationsArray = [random.choice(operations), random.choice(operations), random.choice(
            operations), random.choice(operations), random.choice(operations)]
        if abs((performOperations(possDigitsArray, possOperationsArray)) - idealNum) < bestDiff:
            bestDiff = abs(
                (performOperations(possDigitsArray, possOperationsArray)) - idealNum)
            bestDigitsArray = possDigitsArray[:]
            bestOperationsArray = possOperationsArray[:]
            print(
                "bestDiff:", bestDiff)
            a, b, c, d, e, f = bestDigitsArray
            m, n, o, p, q = bestOperationsArray
            print(a, m, b, n, c, o, d, p, e, q, f, '=',
                  performOperations(possDigitsArray, possOperationsArray))
        if bestDiff <= 0.000001:
            print(a, m, b, n, c, o, d, p, e, q, f, '=',
                  performOperations(possDigitsArray, possOperationsArray))
            return


def performOperations(digitsList, operationsList):  # digits list, operations list
    currNum = digitsList[0] * 1.0
    for _ in range(len(digitsList)-1):
        if operationsList[_] == '+':
            currNum += digitsList[_+1]
        elif operationsList[_] == '-':
            currNum -= digitsList[_+1]
        elif operationsList[_] == '*':
            currNum *= digitsList[_+1]
        elif operationsList[_] == '/':
            if digitsList[_+1] == 0:
                return 362881*2
            else:
                currNum /= digitsList[_+1]
    return currNum


findApp(11111)
