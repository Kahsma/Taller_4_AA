    create_board()
    print(draw_board())

    # Realizar un movimiento aleatorio al principio
    i, j = jugador_aleatorio()
    juego_terminado = update_board((i, j))

    if juego_terminado:
        ()
        print("Juego terminado!")
    else:
        while not has_won():
            movimiento = solver_fuerza_bruta()
            if movimiento is None:
                print("No quedan movimientos.")
                break

            i, j = movimiento
            juego_terminado = update_board((i, j))

            if juego_terminado:
                reveal_mines()
                print("Juego terminado!")
                break

    print(draw_board())