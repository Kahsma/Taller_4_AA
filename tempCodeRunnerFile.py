def detectar_minas():
    opciones = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                opciones.append((i, j))
    # Verificar si alguna casilla adyacente a una casilla revelada tiene el mismo número de casillas no reveladas alrededor que su número
    for casilla in opciones:
        i, j = casilla
        num_minas, casillas_adyacentes = adjacent_squares(i, j)
        casillas_reveladas_adyacentes = [(x, y) for x, y in casillas_adyacentes if MATRIX[x][y] != '?']
        for casilla_adyacente in casillas_reveladas_adyacentes:
            i_adyacente, j_adyacente = casilla_adyacente
            num_minas_adyacentes, casillas_adyacentes_adyacentes = adjacent_squares(i_adyacente, j_adyacente)
            casillas_desconocidas_adyacentes = [(x, y) for x, y in casillas_adyacentes_adyacentes if MATRIX[x][y] == '?']
            if len(casillas_desconocidas_adyacentes) == num_minas_adyacentes and len(casillas_desconocidas_adyacentes) > 0 and get_index(*casilla) not in MINAS_MARCADAS:
                MINAS_MARCADAS.add(get_index(*casilla))


def solver_fuerza_bruta():
    detectar_minas()

    casillas_seguras = []
    casillas_desconocidas = []

    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                casillas_desconocidas.append((i, j))
            else:
                casilla_completada = revisar_casilla_completada(i, j)
                if casilla_completada:
                    casillas_seguras.append(casilla_completada)

    if has_won():
        return casillas_seguras[0]
    detectar_minas()
    # Si no se encontraron casillas seguras utilizando verificaciones directas, utilizar combinaciones para deducir movimientos seguros
    for tamano_combinacion in range(1, len(casillas_desconocidas) + 1):
        for combinacion in itertools.combinations(casillas_desconocidas, tamano_combinacion):
            for casilla in combinacion:
                if get_index(*casilla) not in MINAS_MARCADAS:
                    return casilla

    # Si no se pueden hacer deducciones, utilizar un movimiento aleatorio
    return jugador_aleatorio()

def jugador_aleatorio():
    while True:
        i = random.randint(0, ROWS - 1)
        j = random.randint(0, COLUMNS - 1)
        if MATRIX[i][j] == '?':
            return i, j