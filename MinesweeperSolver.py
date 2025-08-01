#!/usr/bin/python3
# ./MinesweeperSolver.py
board = {
    1: [1, 1],
    2: [2, 2],
    3: [2, 3],
    4: [1, 4],
    5: [0, 5],
    6: [1, 6],
    7: ["b", 7],
    8: [1, 8],
    9: [1, -9],
    10: ["b", 10],
    11: ["b", 11],
    12: [2, -12],
    13: [2, -13],
    14: [2, -14],
    15: [2, -15],
    16: [1, -16],
    17: [1, -17],
    18: [2, -18],
    19: [3, -19],
    20: ["b", 20],
    21: [2, -21],
    22: ["b", 22],
    23: [2, -23],
    24: [1, -24],
    25: [0, -25],
    26: [1, -26],
    27: [2, -27],
    28: [2, -28],
    29: [2, -29],
    30: [1, -30],
    31: [2, -31],
    32: ["b", 32],
    33: [0, -33],
    34: [1, -34],
    35: ["b", 35],
    36: [1, -36],
    37: [0, -37],
    38: [0, -38],
    39: [2, -39],
    40: [2, -40],
    41: [0, -41],
    42: [1, -42],
    43: [1, -43],
    44: [1, -44],
    45: [0, -45],
    46: [0, -46],
    47: [1, -47],
    48: ["b", 48],
    49: [0, -49],
    50: [0, -50],
    51: [0, -51],
    52: [0, -52],
    53: [0, -53],
    54: [0, -54],
    55: [1, -55],
    56: [1, -56],
    57: [0, -57],
    58: [0, -58],
    59: [0, -59],
    60: [0, -60],
    61: [0, -61],
    62: [0, -62],
    63: [0, -63],
    64: [0, -64],
}
# try:
#     with open("minesweeper board", "r") as file:
#         board = file.read()
# except:
#     None
# print(board)
length = int(len(board) ** 0.5)
inTheMiddle = []
revealed = []
# v1: calculates ~25,000 board per second
aroundRevealed = {}


def gbold(string):
    string = "\033[1m" + string + "\033[0m"
    string = "\033[1;32;40m" + string + "\033[0m"  # makes string green
    return string


def rbold(string):
    string = "\033[1m" + string + "\033[0m"
    string = "\033[1;31;40m" + string + "\033[0m"  # makes string red
    return string


print(rbold("hello"))


def printBoard(someBoard):
    length == int(len(someBoard) ** 0.5)
    printBoard = ""
    for allArrays in range(length):
        line = ""
        for oneArray in range(length):
            inx = length * allArrays + oneArray + 1
            if someBoard[inx] == -1:
                line += "[?]"
            elif someBoard[inx] == "b":
                line += "[" + rbold(str(someBoard[inx])) + "]"
            else:
                line += "[" + gbold(str(someBoard[inx])) + "]"
        printBoard += line + "\n"
    return printBoard


def tryApp(num):
    global revealed
    global aroundRevealed
    if (
        not num in aroundRevealed.keys()
        and not num in revealed
        and not num in inTheMiddle
    ):
        aroundRevealed[num] = len(aroundRevealed) + 1


def findArounds():
    global length
    global revealed
    for inx in revealed:
        if inx % length > 0:
            tryApp(inx + 1)
            # bottom right
            if inx < length * length - length:
                tryApp(inx + length + 1)
            # top right
            if inx > length:
                tryApp(inx - length + 1)
        if inx % length != 1:
            tryApp(inx - 1)
            # reveal bottom left?
            if inx <= length * length - length:
                tryApp(inx + length - 1)
            # reveal top left?
            if inx > length:
                tryApp(inx - length - 1)
        if inx > length:
            tryApp(inx - length)
        if inx <= length * length - length:
            tryApp(inx + length)


def calcRevealed():
    global board
    global revealed
    for inx in board:
        if (
            board[inx][1] < 0
            and board[inx][1] >= -length * length
            and not inx in revealed
            and not inx in revealed
        ):
            if board[inx][0] == 0:
                inTheMiddle.append(inx)
            else:
                revealed.append(inx)


def bombsAround(inx, board):
    global length
    bombsAround = 0
    if inx % length > 0:
        if board[inx + 1] == "b":
            bombsAround += 1
        # bottom right
        if inx < length * length - length:
            if board[inx + length + 1] == "b":
                bombsAround += 1
        # top right
        if inx > length:
            if board[inx - length + 1] == "b":
                bombsAround += 1
    if inx % length != 1:
        if board[inx - 1] == "b":
            bombsAround += 1
        # reveal bottom left?
        if inx <= length * length - length:
            if board[inx + length - 1] == "b":
                bombsAround += 1
        # reveal top left?
        if inx > length:
            if board[inx - length - 1] == "b":
                bombsAround += 1
    if inx > length:
        if board[inx - length] == "b":
            bombsAround += 1
    if inx <= length * length - length:
        if board[inx + length] == "b":
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
    allValidBoards = []
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
    for _ in range(2 ** len(aroundRevealed)):
        newBoard = randomBoard.copy()
        for inx in aroundRevealed.keys():
            newBoard[inx] = bombOrSafe(2 ** aroundRevealed[inx] / 2, _)
        boardsDrawn += 1
        print(
            "Boards drawn: " + str(boardsDrawn) + " / " + str(2 ** len(aroundRevealed))
        )
        if testBoard(newBoard):
            allValidBoards.append(newBoard)


def findKnownSquares():
    global allValidBoards
    global scoreOfEachSquare
    global board
    global length
    scoreOfEachSquare = {}
    for inx in aroundRevealed:
        scoreOfEachSquare[inx] = 0
        for board123 in allValidBoards:
            if board123[inx] != "b":
                scoreOfEachSquare[inx] += 1
    for inx in scoreOfEachSquare:
        if scoreOfEachSquare[inx] == len(allValidBoards):
            print(
                str(inx)
                + " ("
                + str((inx - 1) % length + 1)
                + ","
                + str((inx - 1) // length + 1)
                + ") is a safe square"
            )
        if scoreOfEachSquare[inx] == 0:
            print(
                str(inx)
                + " ("
                + str((inx - 1) % length + 1)
                + ","
                + str((inx - 1) // length + 1)
                + ") is a bomb"
            )


calcValidBoards()
for board in allValidBoards:
    print("Valid Board:\n" + printBoard(board))
findKnownSquares()
print("Og board:\n" + printBoard(randomBoard))
