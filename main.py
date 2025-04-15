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


def printBoard(board, shots):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (i + 1, j + 1) in shots:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print()


def takeInput(n, shots):
    while True:
        y = input("Cordenada y: ")
        x = input("Cordenada X: ")
        if x.isnumeric() and y.isnumeric():
            if int(x) <= n and int(y) <= n and int(x) >= 1 and int(y) >= 1:
                return int(y), int(x)
            else:
                print("Valor fuera de rango")
        else:
            print("Formato incorrecto")


def shoot(board, y, x):
    if board[y][x]:
        board[y][x] = False
        return True
    return False


def terminalState(board, triesLeft):
    if triesLeft <= 0:
        return True
    for row in board:
        for cell in row:
            if cell == True:
                return False
    return True


while True:
    n = input("Tamaño del tablero: ")
    if n.isnumeric():
        n = int(n)
        break
    else:
        print("Formato incorrecto")

triesLeft = 20
misses = 0
hits = 0
shots: list[tuple[int, int]] = []
board = generateBoard(n)
while True:
    printBoard(board, shots)
    y, x = takeInput(n, shots)
    triesLeft -= 1
    shots.append((y, x))
    if shoot(board, y - 1, x - 1):
        print("Tiro acertado")
        hits += 1
    else:
        print("Tiro fallido")
        misses += 1
    if terminalState(board, triesLeft):
        print("Fin del juego, ")
        break
print(f"Disparos: {len(shots)}")
print(f"Aciertos: {hits}")
print(f"Fallos: {misses}")
