# Oliver --> 
# Pepo --> 
# Mercho --> 
import random

def crear_tablero(N):
    # Crea un tablero vacío de NxN, donde cada celda es 0 (sin barco)
    return [[0 for _ in range(N)] for _ in range(N)]

  #def ubicar_barcos_por_codigo(tablero, posiciones_barcos):
    # Ubica los barcos según las posiciones dadas
   # for fila, columna in posiciones_barcos:
     #   tablero[fila][columna] = 1  # 1 representa un barco
    #return tablero

def ubicar_barcos_aleatoriamente(tablero, cantidad_barcos):
    N = len(tablero)
    ubicados = 0
    while ubicados < cantidad_barcos:
        fila = random.randint(0, N-1)
        columna = random.randint(0, N-1)
        if tablero[fila][columna] == 0:
            tablero[fila][columna] = 1
            ubicados += 1
    return tablero

def imprimir_tablero(tablero):
    for fila in tablero:
        print(" afa".join(str(celda) for celda in fila))

# Ejemplo de uso:
N = 5
tablero = ubicar_barcos_aleatoriamente(tablero, 5)

# Opción 1: Asignar barcos por código
barcos_por_codigo = [(0, 0), (2, 3), (4, 1)]  # posiciones manuales
tablero = ubicar_barcos_por_codigo(tablero, barcos_por_codigo)

# Opción 2: Asignar barcos aleatoriamente
# tablero = ubicar_barcos_aleatoriamente(tablero, 5)

# Mostrar el tablero
imprimir_tablero(tablero)
