import random
from typing import List, Tuple, Optional


def generar_tamaños_barcos(n: int) -> List[int]:
    """
    Genera una lista de tamaños de barcos proporcional al tamaño del tablero.

    Args:
        n (int): Tamaño del tablero (n x n).

    Returns:
        List[int]: Lista de tamaños de barcos generados.
    """
    total_casillas = n * n
    barcos = total_casillas // 3  # Número de barcos
    tamaños_barcos = []
    while barcos > 0:
        tamaño = random.choice([1, 2, 3])  # Tamaños posibles de los barcos
        if barcos - tamaño >= 0:
            tamaños_barcos.append(tamaño)
            barcos -= tamaño
        else:
            break
    return tamaños_barcos


def generar_tablero(n: int) -> Tuple[List[List[bool]], List[List[Tuple[int, int]]]]:
    """
    Genera un tablero aleatorio de tamaño n x n con barcos de tamaños
    proporcionales.

    Args:
        n (int): Entero que define el tamaño del tablero (n x n).

    Returns:
        Tuple[List[List[bool]], List[List[Tuple[int, int]]]]: Tupla con la matriz cuadrada
        de valores booleanos y la lista de barcos generados.
    """
    tablero: List[List[bool]] = [[False for _ in range(n)] for _ in range(n)]
    barcos: List[List[Tuple[int, int]]] = []
    tamaños_barcos = generar_tamaños_barcos(n)

    for tamaño in tamaños_barcos:
        while True:
            orientacion = random.choice(["H", "V"])
            y = random.randint(0, n - 1)
            x = random.randint(0, n - 1)
            posiciones = validar_posicion(
                tablero, y, x, tamaño, orientacion, n)

            if posiciones:
                for pos_y, pos_x in posiciones:
                    tablero[pos_y][pos_x] = True
                barcos.append(posiciones)
                break

    return tablero, barcos


def ingresar_barcos_manual(
    n: int, tamaños_barcos: List[int]
) -> Tuple[List[List[bool]], List[List[Tuple[int, int]]]]:
    """
    Permite al usuario ingresar manualmente las posiciones de los barcos.

    Args:
        n (int): Tamaño del tablero.
        tamaños_barcos (List[int]): Lista con los tamaños de los barcos a colocar.

    Returns:
        Tuple[List[List[bool]], List[List[Tuple[int, int]]]]: Tupla con el tablero
        y la lista de barcos creados.
    """
    barcos: List[List[Tuple[int, int]]] = []
    tablero: List[List[bool]] = [[False for _ in range(n)] for _ in range(n)]
    print(f"Ingrese las posiciones de los barcos (tamaños: {tamaños_barcos}).")

    for tamaño in tamaños_barcos:
        while True:
            print(f"\nBarco de tamaño {tamaño}:")
            posiciones_barcos = [pos for barco in barcos for pos in barco]
            imprimir_tablero(tablero, posiciones_barcos, barcos)

            try:
                y = int(input("Ingrese la coordenada inicial Y: ")) - 1
                x = int(input("Ingrese la coordenada inicial X: ")) - 1
                orientacion = input(
                    "Ingrese la orientación (H para horizontal, V para vertical): "
                ).upper()
            except ValueError:
                print("Por favor, ingrese valores válidos.")
                continue

            posiciones = validar_posicion(
                tablero, y, x, tamaño, orientacion, n)
            if posiciones:
                for pos_y, pos_x in posiciones:
                    tablero[pos_y][pos_x] = True
                barcos.append(posiciones)
                break

    return tablero, barcos


def validar_posicion(
    tablero: List[List[bool]], y: int, x: int, tamaño: int, orientacion: str, n: int
) -> Optional[List[Tuple[int, int]]]:
    """
    Valida si es posible colocar un barco en la posición indicada.

    Args:
        tablero (List[List[bool]]): Matriz que representa el tablero.
        y (int): Coordenada Y inicial.
        x (int): Coordenada X inicial.
        tamaño (int): Tamaño del barco.
        orientacion (str): 'H' para horizontal, 'V' para vertical.
        n (int): Tamaño del tablero.

    Returns:
        Optional[List[Tuple[int, int]]]: Lista de posiciones si es válido, None si no es válido.
    """
    # Validar coordenadas iniciales
    if y < 0 or y >= n or x < 0 or x >= n:
        print("Coordenadas fuera de rango.")
        return None

    if tablero[y][x]:
        print("Ya hay un barco en esa posición.")
        return None

    posiciones: List[Tuple[int, int]] = []

    if orientacion.upper() == "H":
        # Validar barco horizontal
        if x + tamaño > n:
            print("Barco fuera de rango.")
            return None

        for j in range(tamaño):
            if tablero[y][x + j]:
                print("Ya hay un barco en esa posición.")
                return None

        for j in range(tamaño):
            posiciones.append((y, x + j))

    elif orientacion.upper() == "V":
        # Validar barco vertical
        if y + tamaño > n:
            print("Barco fuera de rango.")
            return None

        for j in range(tamaño):
            if tablero[y + j][x]:
                print("Ya hay un barco en esa posición.")
                return None

        for j in range(tamaño):
            posiciones.append((y + j, x))
    else:
        print("Orientación inválida.")
        return None

    return posiciones


def disparar(
    tablero: List[List[bool]],
    barcos: List[List[Tuple[int, int]]],
    disparos: List[Tuple[int, int]],
    y: int,
    x: int,
) -> Tuple[bool, bool]:
    """
    Dispara a una coordenada especificada en el tablero.

    Args:
        tablero (List[List[bool]]): Tablero de juego.
        barcos (List[List[Tuple[int, int]]]): Lista de barcos (cada barco es una lista de coordenadas).
        disparos (List[Tuple[int, int]]): Lista de coordenadas ya disparadas.
        y (int): Coordenada Y del disparo.
        x (int): Coordenada X del disparo.

    Returns:
        Tuple[bool, bool]: Una tupla con dos valores booleanos:
            - El primero indica si el disparo fue acertado (True) o fallido (False).
            - El segundo indica si el barco fue hundido (True) o no (False).
    """
    if (y, x) in disparos:
        print("Ya disparaste a esta coordenada.")
        return False, False

    disparos.append((y, x))

    if tablero[y][x]:  # Hay un barco en la posición
        for barco in barcos:
            if (y, x) in barco:
                # Verificar si el barco está completamente hundido
                if all(pos in disparos for pos in barco):
                    print("¡Hundiste un barco!")
                    return True, True  # Acierto y barco hundido
        return True, False  # Acierto pero el barco no está hundido
    return False, False  # Disparo fallido


def preguntar(n: int, disparos: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Solicita y valida coordenadas de disparo al usuario.

    Args:
        n (int): Tamaño del tablero (n x n).
        disparos (List[Tuple[int, int]]): Lista de coordenadas ya disparadas.

    Returns:
        Tuple[int, int]: Coordenadas validadas en formato (y, x).
    """
    while True:
        y = input("Coordenada Y: ")
        x = input("Coordenada X: ")

        if x.isnumeric() and y.isnumeric():
            x_int, y_int = int(x), int(y)

            if 1 <= x_int <= n and 1 <= y_int <= n:
                if (y_int - 1, x_int - 1) in disparos:
                    print("Ya disparaste a esa coordenada")
                else:
                    return y_int - 1, x_int - 1
            else:
                print("Valor fuera de rango")
        else:
            print("Formato incorrecto")


def imprimir_tablero(
    tablero: List[List[bool]],
    disparos: List[Tuple[int, int]],
    barcos: List[List[Tuple[int, int]]],
    intentosFaltantes: int = -1,
) -> None:
    """
    Imprime el tablero de juego en la consola con formato mejorado y colores.

    Args:
        tablero (List[List[bool]]): Matriz que representa el tablero de juego.
        disparos (List[Tuple[int, int]]): Lista de coordenadas donde se ha disparado.
        barcos (List[List[Tuple[int, int]]]): Lista de barcos (cada barco es una lista de coordenadas).
        intentosFaltantes (int, optional): Número de intentos restantes. Por defecto -1.

    Returns:
        None: Esta función no retorna ningún valor.
    """
    # Códigos ANSI para colores
    RESET = "\033[0m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    BOLD = "\033[1m"
    MAGENTA = "\033[95m"  # Para barcos hundidos

    n = len(tablero)

    # Identificar barcos hundidos
    barcos_hundidos = []
    for barco in barcos:
        if all(pos in disparos for pos in barco):
            barcos_hundidos.extend(barco)

    # Imprimir encabezado de columnas
    print(f"\n{BOLD}{CYAN}   ", end="")
    for j in range(n):
        print(f" {j + 1}  ", end="")
    print(RESET)

    # Imprimir línea separadora
    print(f"{BOLD}{CYAN}  +" + "---+" * n + RESET)

    # Imprimir filas del tablero
    for i in range(n):
        print(f"{BOLD}{CYAN}{i + 1} |", end=RESET)

        for j in range(n):
            if (i, j) in disparos:
                if (i, j) in barcos_hundidos:  # Barco hundido
                    print(f" {MAGENTA}X {CYAN}|", end="")
                elif tablero[i][j]:  # Hit (acierto)
                    print(f" {RED}X {CYAN}|", end="")
                else:  # Miss (fallo)
                    print(f" {BLUE}O {CYAN}|", end="")
            else:  # Celda no atacada
                if (i, j) in barcos_hundidos:  # Mostrar barcos hundidos
                    print(f" {MAGENTA}X {CYAN}|", end="")
                else:
                    print(f" {GREEN}· {CYAN}|", end="")
        print(RESET)

        # Imprimir línea separadora
        print(f"{BOLD}{CYAN}  +" + "---+" * n + RESET)

    # Imprimir información adicional
    barcos_no_hundidos = []

    # Recorrer cada barco en la lista de barcos
    for b in barcos:
        # Verificar si todas las posiciones del barco están en la lista de disparos
        barco_hundido = all(pos in disparos for pos in b)

        # Si el barco no está completamente hundido, añadirlo a la lista
        if not barco_hundido:
            barcos_no_hundidos.append(b)

    # Contar el número de barcos que no están completamente hundidos
    cantidad_barcos_no_hundidos = len(barcos_no_hundidos)

    print(f"\n{BOLD}Barcos faltantes: {RED}{
          cantidad_barcos_no_hundidos}{RESET}")
    if intentosFaltantes != -1:
        print(f"{BOLD}Intentos faltantes: {BLUE}{intentosFaltantes}{RESET}")


def terminado(intentosFaltantes: int, barcos: int) -> bool:
    """
    Verifica si el juego ha terminado.

    Args:
        intentosFaltantes (int): Número de intentos restantes.
        barcos (int): Número de barcos restantes.

    Returns:
        bool: True si el juego ha terminado, False en caso contrario.
    """
    if intentosFaltantes <= 0:
        print("Te quedaste sin intentos")
        return True

    if barcos <= 0:
        print("¡Hundiste todos los barcos!")
        return True

    return False


def jugar_modo_un_jugador(n: int, tamaños_barcos: List[int]) -> None:
    """
    Ejecuta el modo de un jugador.

    Args:
        n (int): Tamaño del tablero.
        tamaños_barcos (List[int]): Lista de tamaños de barcos a colocar.

    Returns:
        None: Esta función no retorna ningún valor.
    """
    intentosFaltantes = int(0.8 * n * n)
    fallidos = 0
    aciertos = 0
    disparos: List[Tuple[int, int]] = []
    tablero, barcos = generar_tablero(n)

    while True:
        imprimir_tablero(tablero, disparos, barcos, intentosFaltantes)
        y, x = preguntar(n, disparos)
        intentosFaltantes -= 1

        acertado, hundido = disparar(tablero, barcos, disparos, y, x)
        if acertado:
            print("Tiro acertado")
            aciertos += 1
            if hundido:
                print("¡Hundiste un barco!")
        else:
            print("Tiro fallido")
            fallidos += 1

        # Usar la versión expandida del conteo de barcos
        barcos_no_hundidos = []
        for b in barcos:
            barco_hundido = all(pos in disparos for pos in b)
            if not barco_hundido:
                barcos_no_hundidos.append(b)

        cantidad_barcos_no_hundidos = len(barcos_no_hundidos)

        if terminado(intentosFaltantes, cantidad_barcos_no_hundidos):
            # Imprimir tablero final
            imprimir_tablero(tablero, disparos, barcos)
            print("Fin del juego")
            break

    # Estadísticas finales
    print(f"Disparos: {len(disparos)}")
    print(f"Aciertos: {aciertos}")
    print(f"Fallos: {fallidos}")


def jugar_modo_dos_jugadores(n: int, tamaños_barcos: List[int]) -> None:
    """
    Ejecuta el modo de dos jugadores.

    Args:
        n (int): Tamaño del tablero.
        tamaños_barcos (List[int]): Lista de tamaños de barcos a colocar.

    Returns:
        None: Esta función no retorna ningún valor.
    """
    tablero1, barcos1 = None, None
    tablero2, barcos2 = None, None

    # Jugador 1 elige cómo armar su tablero
    print("\nJugador 1:")
    if input("¿Desea armar su tablero manualmente? (s/n): ").lower() == "s":
        tablero1, barcos1 = ingresar_barcos_manual(n, tamaños_barcos)
    else:
        tablero1, barcos1 = generar_tablero(n)

    # Jugador 2 elige cómo armar su tablero
    print("\nJugador 2:")
    if input("¿Desea armar su tablero manualmente? (s/n): ").lower() == "s":
        tablero2, barcos2 = ingresar_barcos_manual(n, tamaños_barcos)
    else:
        tablero2, barcos2 = generar_tablero(n)

    disparos1: List[Tuple[int, int]] = []
    disparos2: List[Tuple[int, int]] = []
    aciertos1, fallidos1 = 0, 0
    aciertos2, fallidos2 = 0, 0
    turno_jugador1 = True
    ganador = ""

    while True:
        jugador_actual = "Jugador 1" if turno_jugador1 else "Jugador 2"
        print(f"\n=== Turno de {jugador_actual} ===")

        # Mostrar tablero del oponente con los disparos del jugador actual
        if turno_jugador1:
            imprimir_tablero(tablero2, disparos1, barcos2)
            y, x = preguntar(n, disparos1)

            acertado, hundido = disparar(tablero2, barcos2, disparos1, y, x)
            if acertado:
                aciertos1 += 1
                print("¡Tiro acertado!")
                if hundido:
                    print("¡Hundiste un barco!")
            else:
                fallidos1 += 1
                print("Tiro fallido")

            barcos_no_hundidos = []
            for b in barcos2:
                barco_hundido = all(pos in disparos1 for pos in b)
                if not barco_hundido:
                    barcos_no_hundidos.append(b)

            cantidad_barcos_no_hundidos = len(barcos_no_hundidos)
            if cantidad_barcos_no_hundidos == 0:
                ganador = "Jugador 1"
                print("¡Jugador 1 gana!")
                break
        else:
            imprimir_tablero(tablero1, disparos2, barcos1)
            y, x = preguntar(n, disparos2)

            acertado, hundido = disparar(tablero1, barcos1, disparos2, y, x)
            if acertado:
                aciertos2 += 1
                print("¡Tiro acertado!")
                if hundido:
                    print("¡Hundiste un barco!")
            else:
                fallidos2 += 1
                print("Tiro fallido")

            barcos_no_hundidos = []
            for b in barcos1:
                barco_hundido = all(pos in disparos2 for pos in b)
                if not barco_hundido:
                    barcos_no_hundidos.append(b)

            cantidad_barcos_no_hundidos = len(barcos_no_hundidos)
            if cantidad_barcos_no_hundidos == 0:
                ganador = "Jugador 2"
                print("¡Jugador 2 gana!")
                break

        turno_jugador1 = not turno_jugador1

    # Mostrar tableros finales
    print("\n=== Tablero final del Jugador 1 ===")
    imprimir_tablero(tablero1, disparos2, barcos1)
    print("\n=== Tablero final del Jugador 2 ===")
    imprimir_tablero(tablero2, disparos1, barcos2)

    # Resumen del juego
    print("\n=== Resumen del juego ===")
    print(f"Ganador: {ganador}")
    print(f"Jugador 1: {aciertos1} aciertos, {fallidos1} fallos")
    print(f"Jugador 2: {aciertos2} aciertos, {fallidos2} fallos")


# Programa principal
def main() -> None:
    """
    Función principal del juego de batalla naval.

    Esta función inicia el juego, pide la configuración inicial y ejecuta
    el modo de juego seleccionado.

    Args:
        None: No recibe parámetros.

    Returns:
        None: Esta función no retorna ningún valor.
    """
    # Determinar número de jugadores
    jugadores: bool = False
    while True:
        jugadores_input = input("Cantidad de jugadores (1/2): ")
        if jugadores_input.isnumeric():
            if int(jugadores_input) in [1, 2]:
                jugadores = bool(int(jugadores_input) - 1)
                break
            else:
                print("Formato incorrecto")

    # Determinar tamaño del tablero
    while True:
        if jugadores:
            n_input = input("Tamaño de los tableros: ")
        else:
            n_input = input("Tamaño del tablero: ")

        if n_input.isnumeric():
            n = int(n_input)
            break
        else:
            print("Formato incorrecto")

    # Generar tamaños de barcos proporcional al tablero
    tamaños_barcos = generar_tamaños_barcos(n)

    # Ejecutar el modo de juego correspondiente
    if jugadores:
        jugar_modo_dos_jugadores(n, tamaños_barcos)
    else:
        jugar_modo_un_jugador(n, tamaños_barcos)


if __name__ == "__main__":
    main()
