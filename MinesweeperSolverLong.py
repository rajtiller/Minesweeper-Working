#!/usr/bin/python3
# /usr/bin/python3 "/Users/rajtiller/Source/Minesweeper/MinsweeperSolverLong.py"
# ./MinesweeperSolverLong.py
import random

# The board is a dictionary
# Each square has key of its index (numbered 1-length^2)
# Each square has a value of a two number list [a,b]
# a is either "b" or the number of bombs that squares is next to
# b is the same as index, but negative if that square has been revealed
# If b > length^2 then labeled as a flag


def gbold(string):
    string = "\033[1m" + string + "\033[0m"
    string = "\033[1;32;40m" + string + "\033[0m"  # makes string green
    return string


def rbold(string):
    string = "\033[1m" + string + "\033[0m"
    string = "\033[1;31;40m" + string + "\033[0m"  # makes string red
    return string


def randomNums(low, up, num):
    nums = []
    while len(nums) < num:
        pot = random.randint(low, up)
        if (not pot in nums):
            nums.append(pot)
    return nums


def createBoard(length):
    global board
    board = {}
    # Labels:
    # "b" = Bomb
    # 0 = Revealed to be 0
    # 1 = Revealed to be 1
    # 2 = Revealed to be 2
    # 3 = Revealed to be 3
    # 4 = Revealed to be 4
    # 5 = Revealed to be 5
    # second number - 1 means shown while 0 means hidden
    for _ in range(length*length):
        # Each square on board has a key of a number 1-5
        # The value of each key is [bombs it's next to, shown(1)/hidden(0)]
        board[_+1] = [0, _+1]
    bombs = randomNums(1, length*length, length*length//8)
    for _ in bombs:
        board[_][0] = "b"
    for num in range(length*length):
        board = setBoard(board, board[num+1])


def setBoard(board, square):
    # Board is a dictionary of the form num (1-50):[bombs touching,index]
    # Square is two-number array that is the value of some key of board
    length = len(board) ** 0.5
    inx = square[1]
    bombsTouching = 0
    if square[0] == "b":
        return board
    if inx == 1:
        if board[2][0] == "b":
            bombsTouching += 1
        if board[length + 1][0] == "b":
            bombsTouching += 1
        if board[length + 2][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx == length:
        if board[length - 1][0] == "b":
            bombsTouching += 1
        if board[2*length][0] == "b":
            bombsTouching += 1
        if board[2*length - 1][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx == length*length:
        if board[inx - 1][0] == "b":
            bombsTouching += 1
        if board[inx - length][0] == "b":
            bombsTouching += 1
        if board[inx - length - 1][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx == length*length-length+1:
        if board[inx + 1][0] == "b":
            bombsTouching += 1
        if board[inx - length][0] == "b":
            bombsTouching += 1
        if board[inx - length + 1][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx < length:
        if board[inx + 1][0] == "b":
            bombsTouching += 1
        if board[inx - 1][0] == "b":
            bombsTouching += 1
        if board[inx + length + 1][0] == "b":
            bombsTouching += 1
        if board[inx + length - 1][0] == "b":
            bombsTouching += 1
        if board[inx + length][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx > length*length-length:
        if board[inx + 1][0] == "b":
            bombsTouching += 1
        if board[inx - 1][0] == "b":
            bombsTouching += 1
        if board[inx - length + 1][0] == "b":
            bombsTouching += 1
        if board[inx - length - 1][0] == "b":
            bombsTouching += 1
        if board[inx - length][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx % length == 1:
        if board[inx + 1][0] == "b":
            bombsTouching += 1
        if board[inx + length][0] == "b":
            bombsTouching += 1
        if board[inx - length][0] == "b":
            bombsTouching += 1
        if board[inx - length + 1][0] == "b":
            bombsTouching += 1
        if board[inx + length + 1][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx % length == 0:
        if board[inx - 1][0] == "b":
            bombsTouching += 1
        if board[inx + length][0] == "b":
            bombsTouching += 1
        if board[inx - length][0] == "b":
            bombsTouching += 1
        if board[inx - length - 1][0] == "b":
            bombsTouching += 1
        if board[inx + length - 1][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board
    if inx % length > 1:
        if board[inx - 1][0] == "b":
            bombsTouching += 1
        if board[inx + 1][0] == "b":
            bombsTouching += 1
        if board[inx - length][0] == "b":
            bombsTouching += 1
        if board[inx - length - 1][0] == "b":
            bombsTouching += 1
        if board[inx - length + 1][0] == "b":
            bombsTouching += 1
        if board[inx + length + 1][0] == "b":
            bombsTouching += 1
        if board[inx + length][0] == "b":
            bombsTouching += 1
        if board[inx + length - 1][0] == "b":
            bombsTouching += 1
        board[inx][0] = bombsTouching
        return board


def revealBoard():
    global board
    global length
    global squaresRevealed
    if squaresRevealed > 0:
        print(gbold("You Win!"))
        printBoard = ""
        for allArrays in range(length):
            line = ""
            for oneArray in range(length):
                inx = length * allArrays + oneArray + 1
                if board[inx][0] == "b":
                    line += ("[" + rbold(str(board[inx][0])) + "]")
                else:
                    line += ("[" + gbold(str(board[inx][0])) + "]")
            printBoard += line + '\n'
        print(printBoard)
    else:
        print(rbold("You Lose!"))
        printBoard = ""
        for allArrays in range(length):
            line = ""
            for oneArray in range(length):
                inx = length * allArrays + oneArray + 1
                if board[inx][1] < 0 and board[inx][0] != "b":
                    line += ("[" + gbold(str(board[inx][0])) + "]")
                elif board[inx][0] == "b":
                    line += ("[" + rbold(str(board[inx][0])) + "]")
                else:
                    line += ("[?]")
            printBoard += line + '\n'
        print(printBoard)


def revealAll():
    global board
    global length
    printBoard = ""
    for _ in range(length):
        printBoard += str(_) + " "
    printBoard += '\n'
    for allArrays in range(length):
        line = str(allArrays)
        for oneArray in range(length):
            inx = length * allArrays + oneArray + 1
            line += ("[" + gbold(str(board[inx][0])) + "]")
        printBoard += line + '\n'
    return printBoard


def printBoard():
    global board
    printBoard = ""
    global length
    for allArrays in range(length):
        line = ""
        for oneArray in range(length):
            inx = length * allArrays + oneArray + 1
            if board[inx][1] > 0:
                line += ("[?]")
            elif board[inx][1] < -length*length:
                line += ("[" + rbold("X") + "]")
            elif board[inx][0] == "b":
                line += ("[" + rbold(str(board[inx][0])) + "]")
            else:
                line += ("[" + gbold(str(board[inx][0])) + "]")
        printBoard += line + '\n'
    return printBoard


def clearAround(inx):
    global board
    global length
    global revZeros
    if inx % length > 0:
        board[inx+1][1] = -1 * abs(board[inx+1][1])
        if board[inx+1][0] == 0 and not (inx+1) in revZeros:
            revZeros.append(inx+1)
        # reveal bottom right?
        if inx < length*length-length:
            board[inx + length + 1][1] = -1 * abs(board[inx+length+1][1])
            if board[inx+length+1][0] == 0 and not (inx+length+1) in revZeros:
                revZeros.append(inx+length+1)
        # reveal top right?
        if inx > length:
            board[inx - length + 1][1] = -1 * abs(board[inx-length+1][1])
            if board[inx-length+1][0] == 0 and not (inx-length+1) in revZeros:
                revZeros.append(inx-length+1)
    if inx % length != 1:
        board[inx-1][1] = -1 * abs(board[inx-1][1])
        if board[inx-1][0] == 0 and not (inx-1) in revZeros:
            revZeros.append(inx-1)
        # reveal bottom left?
        if inx <= length*length-length:
            board[inx + length - 1][1] = -1 * abs(board[inx+length-1][1])
            if board[inx+length-1][0] == 0 and not (inx+length-1) in revZeros:
                revZeros.append(inx+length-1)
        # reveal top left?
        if inx > length:
            board[inx - length - 1][1] = -1 * abs(board[inx-length-1][1])
            if board[inx-length-1][0] == 0 and not (inx-length-1) in revZeros:
                revZeros.append(inx-length-1)
    if inx > length:
        board[inx-length][1] = -1 * abs(board[inx-length][1])
        if board[inx-length][0] == 0 and not (inx-length) in revZeros:
            revZeros.append(inx-length)
    if inx <= length*length-length:
        board[inx+length][1] = -1 * abs(board[inx+length][1])
        if board[inx+length][0] == 0 and not (inx+length) in revZeros:
            revZeros.append(inx+length)


def clearSpace():
    global board
    global length
    global revZeros
    global doneZeros
    while len(revZeros) > len(doneZeros):
        for num in revZeros:
            if not num in doneZeros:
                clearAround(num)
                doneZeros.append(num)


def makeChoice(columna, rowa):
    global board
    global length
    global squaresRevealed
    column = columna
    row = rowa
    while column < 1 or column > length:
        try:
            column = int(
                input("Which Column? (1-" + str(length) + ')' + '\n' + printBoard()))
        except Exception as e:
            print(e)
            column = 0
    while row < 1 or row > length:
        try:
            row = int(
                input("Which Row? (1-" + str(length) + ')' + '\n' + printBoard()))
        except:
            row = 0
    flagMaybe = "d"
    while flagMaybe != "" and flagMaybe != "r" and flagMaybe != "f":
        flagMaybe = input("Reveal (r or leave blank) or flag(f)? (1-" +
                          str(length) + ')' + '\n' + printBoard())
    inx = row * length - length + column
    if flagMaybe == "f":
        if board[inx][1] >= -length*length and board[inx][1] > 0:
            board[inx][1] = -1 * abs(board[inx][1]) - length * length
        else:
            board[inx][1] += length * length
    else:
        board[inx][1] = -1 * abs(board[inx][1])
        if board[inx][1] < -length*length:
            board[inx][1] += length*length
        if board[inx][0] == 0:
            if not inx in revZeros:
                revZeros.append(inx)
        clearSpace()


def sqrev():
    global board
    global squaresRevealed
    squaresRevealed = 0
    for inx in board:
        if board[inx][1] < 0 and board[inx][1] >= -length*length:
            if board[inx][0] == "b":
                squaresRevealed = -1
                break
            squaresRevealed += 1


def playGame():
    global length
    global revZeros
    global doneZeros
    global squaresRevealed
    global safeSquares
    doneZeros = []
    length = 0
    squaresRevealed = 0
    while length < 1 or length > 50:
        length = int(input('How big do you want your board to be? (4-50)'))
    firstColumn = 0
    while not (firstColumn >= 1 and firstColumn <= length):
        firstColumn = int(
            input("What is the column of your first square? (1-" + str(length) + ")"))
    firstRow = 0
    while not (firstRow >= 1 and firstRow <= length):
        firstRow = int(
            input("What is the row of your first square? (1-" + str(length) + ")"))
    inx = firstRow * length - length + firstColumn
    createBoard(length)
    while board[inx][0] != 0:
        createBoard(length)
    board[inx][1] *= -1
    revZeros = []
    revZeros.append(inx)
    clearSpace()
    sqrev()
    print("Squares revealed: " + str(squaresRevealed) +
          "/" + str((length*length - length*length // 8)))
    while squaresRevealed > -1 and squaresRevealed < length*length - (length*length)//8:
        playOrCheat = "d"
        print("board:\n" + printBoard())
        sqrev()
        print("Squares revealed: " + str(squaresRevealed) +
              "/" + str((length*length - length*length//8)))
        playOrCheat = input(
            "Choose Column (1-" + str(length) + ") or solve (s)")
        while playOrCheat != "s" and squaresRevealed > -1 and squaresRevealed < length*length - (length*length)//8:
            makeChoice(int(playOrCheat), 0)
            print("board:\n" + printBoard())
            sqrev()
            print("Squares revealed: " + str(squaresRevealed) +
                  "/" + str((length*length - length*length//8)))
            playOrCheat = input(
                "Choose Column (1-" + str(length) + ") or solve (s)")
        calcValid()
        sqrev()
        print("Squares revealed: " + str(squaresRevealed) +
              "/" + str((length*length - length*length//8)))
    revealBoard()


# v1: calculates ~25,000 board per second


def printBoardSimple(someBoard):
    length == int(len(someBoard) ** 0.5)
    printBoard = ""
    for allArrays in range(length):
        line = ""
        for oneArray in range(length):
            inx = length * allArrays + oneArray + 1
            if someBoard[inx] == -1:
                line += ("[?]")
            elif someBoard[inx] == "b":
                line += ("[" + rbold(str(someBoard[inx])) + "]")
            else:
                line += ("[" + gbold(str(someBoard[inx])) + "]")
        printBoard += line + '\n'
    return printBoard


def tryApp(num):
    global revealed
    global aroundRevealed
    if not num in aroundRevealed.keys() and not num in revealed and not num in inTheMiddle:
        aroundRevealed[num] = len(aroundRevealed)+1


def findArounds():
    global length
    global revealed
    for inx in revealed:
        if inx % length > 0:
            tryApp(inx+1)
            # bottom right
            if inx < length*length-length:
                tryApp(inx+length+1)
            # top right
            if inx > length:
                tryApp(inx-length+1)
        if inx % length != 1:
            tryApp(inx-1)
            # reveal bottom left?
            if inx <= length*length-length:
                tryApp(inx+length-1)
            # reveal top left?
            if inx > length:
                tryApp(inx-length-1)
        if inx > length:
            tryApp(inx-length)
        if inx <= length*length-length:
            tryApp(inx+length)


def calcRevealed():
    global board
    global revealed
    revealed = []
    for inx in board:
        if board[inx][1] < 0 and board[inx][1] >= -length*length and not inx in revealed and not inx in revealed:
            if board[inx][0] == 0:
                inTheMiddle.append(inx)
            else:
                revealed.append(inx)


def bombsAround(inx, board):
    global length
    bombsAround = 0
    if inx % length > 0:
        if board[inx+1] == "b":
            bombsAround += 1
        # bottom right
        if inx < length*length-length:
            if board[inx+length+1] == "b":
                bombsAround += 1
        # top right
        if inx > length:
            if board[inx-length+1] == "b":
                bombsAround += 1
    if inx % length != 1:
        if board[inx-1] == "b":
            bombsAround += 1
        # reveal bottom left?
        if inx <= length*length-length:
            if board[inx+length-1] == "b":
                bombsAround += 1
        # reveal top left?
        if inx > length:
            if board[inx-length-1] == "b":
                bombsAround += 1
    if inx > length:
        if board[inx-length] == "b":
            bombsAround += 1
    if inx <= length*length-length:
        if board[inx+length] == "b":
            bombsAround += 1
    return bombsAround


def bombOrSafe(inx, largeNum):
    if (largeNum // inx) % 2 == 1:
        return "b"
    return 1


def testBoard(possBoard):
    global revealed
    for inx in revealed:
        if possBoard[inx] != bombsAround(inx, possBoard):
            return False
    return True


def calcValidBoards():
    global board
    global revealed
    global allValidBoards
    global randomBoard
    global aroundRevealed
    global inTheMiddle
    allValidBoards = []
    aroundRevealed = {}
    inTheMiddle = []
    calcRevealed()
    findArounds()
    randomBoard = {}
    # randomBoard is a board with an inx and a value
    # if value >= 0, then that is the number of bombs that square is next to
    # if value == -1 then that square is unknown
    # if value == "b" then the square is a bomb
    for inx in board:
        if board[inx][1] > 0:
            randomBoard[inx] = -1
        elif board[inx][0] == "b":
            randomBoard[inx] = "b"
        else:
            randomBoard[inx] = board[inx][0]
    boardsDrawn = 0
    for _ in range(2**len(aroundRevealed)):
        newBoard = randomBoard.copy()
        for inx in aroundRevealed.keys():
            newBoard[inx] = bombOrSafe(2**aroundRevealed[inx]/2, _)
        boardsDrawn += 1
        if boardsDrawn % 100000 == 0:
            print("Boards drawn: " + str((1000 * boardsDrawn) //
                                         2**len(aroundRevealed) / 10) + "%")
        if testBoard(newBoard):
            allValidBoards.append(newBoard)


def findKnownSquares():
    global allValidBoards
    global scoreOfEachSquare
    global board
    global length
    global safeSquares
    safeSquares = []
    scoreOfEachSquare = {}
    for inx in aroundRevealed:
        scoreOfEachSquare[inx] = 0
        for board123 in allValidBoards:
            if board123[inx] != "b":
                scoreOfEachSquare[inx] += 1
    for inx in scoreOfEachSquare:
        if scoreOfEachSquare[inx] == len(allValidBoards):
            safeSquares.append(inx)
            print(str(inx) + " (" + str((inx-1) % length + 1) + "," +
                  str((inx-1)//length + 1) + ") is a safe square")
        if scoreOfEachSquare[inx] == 0:
            print(str(inx) + " (" + str((inx-1) % length + 1) + "," +
                  str((inx-1)//length + 1) + ") is a bomb")


def calcValid():
    global allValidBoards
    calcValidBoards()
    for board in allValidBoards:
        print("Valid Board:\n" + printBoardSimple(board))
    findKnownSquares()


playGame()
