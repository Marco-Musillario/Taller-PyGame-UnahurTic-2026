import pygame

class Casilla:
    def __init__(self):
        self.mina : bool = False
        self.descubierta : bool = False
        self.marcada : bool = False
        self.proximidades : int = 0

class Tablero:
    def __init__(self, filas : int, columnas : int, cantidad_de_bombas : int) -> None:
        self.filas : int = filas
        self.columnas : int = columnas
        self.cantidad_total_de_bombas : int = cantidad_de_bombas
        self.casillas : list[list[Casilla]] = []
        self.casillas_limpias : int = (filas * columnas) - cantidad_de_bombas
        self.cantidad_marcadas : int = 0
        self.explosion : bool = False
        self.generado : bool = False

        for c in range(columnas):
            columna : list[Casilla] = []
            for f in range(filas):
                columna.append(Casilla())
            self.casillas.append(columna)

    def descubrir_casilla(self, x : int, y : int) -> None:
        casilla = self.casillas[x][y]
        if casilla.marcada or casilla.descubierta:
            return 
        
        casilla.descubierta = True

    def marcar_casilla(self, x : int, y : int):
        casilla = self.casillas[x][y]
        if casilla.descubierta:
            return

        if casilla.marcada:
            casilla.marcada = False
            self.cantidad_marcadas -= 1
        else:
            casilla.marcada = True
            self.cantidad_marcadas += 1