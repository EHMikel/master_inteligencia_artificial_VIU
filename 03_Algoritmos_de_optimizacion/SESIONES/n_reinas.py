import numpy as np
import random

def colocar_reina(m, fila, col, tab):
    '''
    esta funcion coloca una reina en un tablero de ajedrez donde las posiciones que no estan en peligro son 0s, la casilla donde se coloca la reina será un numero de un dígito,
    y las casillas en peligro serán un numero de dos digitos. La función devuelve el tablero con la nueva reina colocada y sus posiciones de peligro.
    '''

    # las zonas en peligro seran m +10 para que tenga dos digitos y se pueda diferenciar
    tab[fila, :] = m + 10  # zona de peligro horizontal
    tab[:, col] = m + 10  # zona de peligro vertical

    # colocamos la reina
    tab[fila, col] = m

    # las diagonales
    diag_c1 = min((tab.shape[0] - 1) - col, fila)
    diag_c2 = min(col, fila)
    diag_c3 = min(col, (tab.shape[0] - 1) - fila)
    diag_c4 = min((tab.shape[0] - 1) - col, (tab.shape[0] - 1) - fila)

    # cuadrante 1
    for n in range(1, diag_c1 + 1):
        tab[fila - n, col + n] = m + 10

    # cuadrante 2
    for n in range(1, diag_c2 + 1):
        tab[fila - n, col - n] = m + 10

    # cuadrate 3
    for n in range(1, diag_c3 + 1):
        tab[fila + n, col - n] = m + 10

    # cuadrante 4
    for n in range(1, diag_c4 + 1):
        tab[fila + n, col + n] = m + 10

    return tab

def factible_choices(tablero):

    fact_choices = []
    size = tablero.shape[0]

    for fila in range(size):

        if 0 not in tablero[fila,:]:
            continue

        for col in range(size):

            if 0 not in tablero[:, col]:
                continue

            if tablero[fila,col] == 0:
                fact_choices.append([fila, col])

    return fact_choices


def n_reinas(n: object, tablero: object) -> object:

    if n < 1:
        return True

    if np.count_nonzero(tablero == 0) < n:
        return False

    casillas_factibles = factible_choices(tablero)

    tablero_viejo = tablero.copy()
    while len(casillas_factibles) > 0:

        casilla_elegida = random.choice(casillas_factibles)
        fila = casilla_elegida[0]
        col = casilla_elegida[1]
        tablero_nuevo = colocar_reina(np.random.randint(low=1, high=10), fila, col, tablero)

        if n_reinas(n - 1, tablero_nuevo):
            print(casilla_elegida)
            return True

        else:
            casillas_factibles.remove(casilla_elegida)
            tablero = tablero_viejo.copy()

    return False

if __name__ == '__main__':

    reinas = 16
    tablero = np.zeros((reinas,reinas), dtype= int)

    n_reinas(reinas, tablero)
    #print(tablero)