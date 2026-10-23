import pygame, random
generador = random.Random()

class Casilla:
    def __init__(self):
        self.mina : bool= False
        self.descubierta : bool = False
        self.marcada : bool = False
        self.proximidades : int = 0

class Tablero:
    def __init__(self, filas : int, columnas : int, cantidad_de_bombas : int) -> None:
        if cantidad_de_bombas >= filas * columnas:
            raise ValueError("Hay más bombas que casillas disponibles")
        self.filas : int = filas
        self.columnas : int = columnas
        self.cantidad_total_de_bombas : int = cantidad_de_bombas
        self.casillas : list[list[Casilla]] = []
        self.explosion : bool = False
        self.generado : bool = False
        self.casillas_limpias : int = (self.filas * self.columnas) - self.cantidad_total_de_bombas
        self.cantidad_marcadas : int = 0

        for c in range(columnas):
            columna : list[Casilla] = []
            for f in range(filas):
                columna.append(Casilla())
            self.casillas.append(columna)

    def generar_bombas(self, evitar : tuple[int,int] ) -> None:
        cantidad_puesta : int = 0
        while cantidad_puesta < self.cantidad_total_de_bombas:
            x : int = generador.randrange(self.columnas)
            y : int = generador.randrange(self.filas)
            if not self.casillas[x][y].mina and (x,y) != evitar:
                self.casillas[x][y].mina = True
                self.generar_proximidades(x,y)
                cantidad_puesta += 1
        self.generado = True
                
    def generar_proximidades(self, x : int, y : int) -> None:
        for _x in range(x-1, x+2):
            if _x >= 0 and _x < self.columnas:
                for _y in range(y-1, y+2):
                    if _y >= 0 and _y < self.filas:
                        self.casillas[_x][_y].proximidades += 1

    def marcar_casilla(self, x : int, y : int):
        if not self.casillas[x][y].descubierta:
            if self.casillas[x][y].marcada:
                self.casillas[x][y].marcada = False
                self.cantidad_marcadas -= 1
            else:
                self.casillas[x][y].marcada = True
                self.cantidad_marcadas += 1

    def descubrir_casilla(self, x : int, y : int) -> None:
        if self.casillas[x][y].marcada or self.casillas[x][y].descubierta:
            return 
        
        self.casillas[x][y].descubierta = True

        # Game over
        if self.casillas[x][y].mina:
            self.explosion = True
            return

        # Si hay alguna mina cerca, solo se revela esta casilla
        if self.casillas[x][y].proximidades != 0:
            return

        # Si no hay minas cerca, se revelan las casillas vecinas
        for _x in range(x-1, x+2):
            if _x >= 0 and _x < self.columnas:
                for _y in range(y-1, y+2):
                    if _y >= 0 and _y < self.filas:
                        self.descubrir_casilla(_x,_y)    

    def descubrir_adyacentes(self, x: int, y: int) -> None:
        casilla = self.casillas[x][y]

        if not casilla.descubierta:
            return

        banderas: int = 0

        for _x in range(x - 1, x + 2):
            if _x >= 0 and _x < self.columnas:
                for _y in range(y - 1, y + 2):
                    if _y >= 0 and _y < self.filas:
                        if self.casillas[_x][_y].marcada:
                            banderas += 1

        if banderas != casilla.proximidades:
            return

        for _x in range(x - 1, x + 2):
            if _x >= 0 and _x < self.columnas:
                for _y in range(y - 1, y + 2):
                    if _y >= 0 and _y < self.filas:
                        if not self.casillas[_x][_y].marcada:
                            self.descubrir_casilla(_x, _y) 

    def explotar_minas(self, sonido : pygame.Sound) -> None:
        for x in range(self.columnas):
            for y in range(self.filas):
                if self.casillas[x][y].mina:
                    self.casillas[x][y].descubierta = True
        sonido.play()
        self.explosion = False

    def cantidad_descubiertas_limpias(self) -> int:
        cantidad : int = 0
        for columna in self.casillas:
            for casilla in columna:
                if casilla.descubierta and not casilla.mina:
                    cantidad += 1
        return cantidad

    def limpio(self) -> bool:
        return self.cantidad_descubiertas_limpias() == self.casillas_limpias