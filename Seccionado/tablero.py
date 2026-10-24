import pygame, random

generador = random.Random()

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

        if self.casillas[x][y].mina:
            self.explosion = True
            return

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

    def generar_bombas(self, evitar : tuple[int,int] ) -> None:
            cantidad_puesta : int = 0
            while cantidad_puesta < self.cantidad_total_de_bombas:
                x : int = generador.randrange(self.columnas)
                y : int = generador.randrange(self.filas)
                if not self.casillas[x][y].mina and (x,y) != evitar:
                    self.casillas[x][y].mina = True
                    cantidad_puesta += 1
                    self.generar_proximidades(x,y)
            self.generado = True

    def generar_proximidades(self, x : int, y : int) -> None:
        for _x in range(x-1, x+2):
            if _x >= 0 and _x < self.columnas:
                for _y in range(y-1, y+2):
                    if _y >= 0 and _y < self.filas:
                        self.casillas[_x][_y].proximidades += 1
    
    def cantidad_descubiertas_limpias(self) -> int:
        cantidad : int = 0
        for columna in self.casillas:
            for casilla in columna:
                if casilla.descubierta and not casilla.mina:
                    cantidad += 1
        return cantidad

    def limpio(self) -> bool:
        return self.cantidad_descubiertas_limpias() == self.casillas_limpias

    def explotar_minas(self, sonido : pygame.Sound) -> None:
        for x in range(self.columnas):
            for y in range(self.filas):
                if self.casillas[x][y].mina:
                    self.casillas[x][y].descubierta = True
        sonido.play()
        self.explosion = False