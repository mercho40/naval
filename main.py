import random


def generar_tablero(n):
    """
    Genera un tablero aleatorio de tamaño n x n.

    Esta función crea una matriz cuadrada donde cada celda tiene
    un valor booleano. Cada celda tiene aproximadamente un 15%
    de probabilidad de ser True y un 85% de ser False.

    Args:
        n: Entero que define el tamaño del tablero (n x n).

    Returns:
        list[list[bool]]: Matriz cuadrada con valores booleanos aleatorios.
    """
    barcos = 0
    tablero: list[list[bool]] = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() >= 0.85:
                tablero[i][j] = True
                barcos += 1
            else:
                tablero[i][j] = False
    return tablero, barcos


def disparar(tablero, Y, X):
    """Dispara a una coordenada especificada en el tablero.

    Esta función verifica si la coordenada (Y, X) es un disparo acertado:
    - si fue un disparo acertado o fallido
    - si la coordenada ya fue disparada anteriormente
    - si la coordenada está dentro del rango del tablero

    Args:
        tablero (list): Tablero de juego
        Y (int): Coordenada Y del disparo
        X (int): Coordenada X del disparo
    Returns:
        bool: True si el disparo fue acertado, False en caso contrario
    Raises:
        ValueError: Si las coordenadas están fuera del rango del tablero
    """
    if tablero[Y][X]:  # hay un barco? (Expected answer --> true / false)
        # se hunde el barco (Había un barco en esas coordenadas)
        # tablero[Y][X] = False
        return True  # Te devuelve que le pegaste al barco
    return False  # no hay barco


def preguntar(n, disparos):
    """
    Solicita y valida coordenadas de disparo al usuario.

    Esta función pide al usuario ingresar coordenadas X e Y, validando que:
    - Sean valores numéricos
    - Estén dentro del rango permitido (entre 1 y n)
    - No hayan sido utilizados previamente

    Args:
        n (int): Tamaño del tablero (n x n)
        disparos (list): Lista de coordenadas ya disparadas

    Returns:
        tuple: Coordenadas validadas en formato (y, x)
    """
    while True:
        y = input("Coordenada y: ")
        x = input("Coordenada X: ")
        if x.isnumeric() and y.isnumeric():
            if int(x) <= n and int(y) <= n and int(x) >= 1 and int(y) >= 1:
                if (int(y) - 1, int(x) - 1) in disparos:
                    print("Ya disparaste a esa coordenada")
                else:
                    return int(y) - 1, int(x) - 1
            else:
                print("Valor fuera de rango")
        else:
            print("Formato incorrecto")


def imprimir_tablero(tablero, disparos, intentosFaltantes, barcos):
    """Imprime el tablero de juego en la consola.

    Esta función muestra el estado actual del tablero, donde cada celda
    puede representar diferentes estados:
    - Un barco no atacado
    - Una celda vacía
    - Una celda atacada

    Args:
        tablero (list): Una matriz (lista de listas) que representa el tablero de juego.
    """

    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if (i, j) in disparos:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print()

    print("Barcos faltantes: ", barcos)
    print("Intentos faltantes: ", intentosFaltantes)


def terminado(intentosFaltantes, barcos):
    """Verifica si el juego ha terminado.

    Esta función determina si el juego ha terminado por alguna de estas razones:
    - Se agotaron los intentos disponibles
    - Se hundieron todos los barcos

    Args:
        intentosFaltantes (int): Número de intentos restantes
        barcos (int): Número de barcos restantes

    Returns:
        bool: True si el juego ha terminado, False en caso contrario
    """
    if intentosFaltantes <= 0:
        print("Te quedaste sin intentos")
        return True

    if barcos <= 0:
        print("¡Hundiste todos los barcos!")
        return True

    return False


while True:
    n = input("Tamaño del tablero: ")
    if n.isnumeric():
        n = int(n)
        break
    else:
        print("Formato incorrecto")
intentosFaltantes = int(0.8 * n * n)
fallidos = 0
aciertos = 0
disparos: list[tuple[int, int]] = []
tablero, barcos = generar_tablero(n)
while True:
    imprimir_tablero(tablero, disparos, intentosFaltantes, barcos)
    y, x = preguntar(n, disparos)
    intentosFaltantes -= 1
    disparos.append((y, x))
    if disparar(tablero, y, x):
        tablero[y][x] = False
        barcos -= 1
        print("Tiro acertado")
        aciertos += 1
    else:
        print("Tiro fallido")
        fallidos += 1
    if terminado(intentosFaltantes, barcos):
        print("Fin del juego")
        break
print(f"Disparos: {len(disparos)}")
print(f"Aciertos: {aciertos}")
print(f"Fallos: {fallidos}")
