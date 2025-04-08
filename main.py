# Oliver -->
# Pepo -->
# Mercho -->
#
import random


def generateBoard(n):
    board: list[list[bool]] = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() >= 0.85:
                board[i][j] = True
            else:
                board[i][j] = False
    return board


def printBoard(board):
    for row in board:
        for cell in row:
            if cell:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print()


def terminalState(board):
    for row in board:
        for cell in row:
            if cell:
                return False
    return True


maxTries = 20

printBoard(generateBoard(10))
