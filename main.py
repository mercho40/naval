tablero: List[List[Bool]]


def generarTablero(n):
    for i in range(n):
        for j in range(n):
            tablero[i][j] = False
