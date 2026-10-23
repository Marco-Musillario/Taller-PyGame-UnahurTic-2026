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

class Juego:
    def __init__(self) -> None:
        pygame.init()
        self.running : bool = True
        self.game_over : bool = False
    
        self.filas : int = 16
        self.columnas : int = 16
        self.cantidad_de_bombas : int = 40
    
        self.tamanio_de_casilla : int = 32
        self.pantalla_ancho : int = self.filas * self.tamanio_de_casilla
        self.pantalla_alto : int = self.columnas * self.tamanio_de_casilla

        self.tiempo : float = 0

        pygame.display.set_caption("Busca minas | 40 | 000")
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))

        self.recursos : dict[str, pygame.Surface ]= {}

        self.recursos["bomba"] = pygame.image.load("assets/Bomba.png").convert_alpha()
        self.recursos["marcador"] = pygame.image.load("assets/Marcador.png").convert_alpha()
        self.recursos["font"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=50)
        self.recursos["font2"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=20)
    
        self.recursos["casilla_cubierta_0"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_cubierta_0"].fill("darkolivegreen3")
        self.recursos["casilla_cubierta_1"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_cubierta_1"].fill("darkolivegreen2")
        
        self.recursos["casilla_descubierta_0"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_descubierta_0"].fill("burlywood3")
        self.recursos["casilla_descubierta_1"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_descubierta_1"].fill("burlywood2")
    
        self.recursos["game_over"]= pygame.image.load("assets/game_over.png").convert()
        self.recursos["ganador"]= pygame.image.load("assets/ganador.png").convert()
    
        colores_numeros : list[str] = ["blue", "green", "red", "blue4", "darkred", "cyan4", "black", "dimgrey"]
        self.recursos["0"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla), pygame.SRCALPHA).convert_alpha()
    
        for i in range(8):
            numero : int = i + 1
            numero_imagen : pygame.Surface = self.recursos["font"].render( text= str(numero), antialias= True, color= colores_numeros[i])
            fondo : pygame.Surface = pygame.Surface( size= (self.tamanio_de_casilla,self.tamanio_de_casilla), flags= pygame.SRCALPHA)
            fondo.blit(numero_imagen, numero_imagen.get_rect(center=(self.tamanio_de_casilla // 2 , self.tamanio_de_casilla // 2)))
            self.recursos[str(numero)] = fondo.convert_alpha()

        self.sonidos : dict[str, pygame.Sound]= {}
        self.sonidos["Explosion"] = pygame.mixer.Sound("assets/explosion.mp3")
        self.sonidos["Explosion"].set_volume(0.05)
    
        pygame.display.set_icon(self.recursos["bomba"])
        
        self.reloj = pygame.time.Clock()
    
        self.tablero : Tablero = Tablero(self.filas, self.columnas, self.cantidad_de_bombas)
        return

    def bucle_principal(self):
        while self.running:
            self.input()
            self.logica()
            self.dibujar()
            self.tiempo += self.reloj.tick(60)
        pygame.quit()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running : bool = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mx : int = event.pos[0] // self.tamanio_de_casilla
                my : int = event.pos[1] // self.tamanio_de_casilla
                match event.button:
                    case 1:
                        if self.game_over or self.tablero.limpio():
                            continue
                        if not self.tablero.generado:
                            self.tablero.generar_bombas((mx,my))
                        casilla = self.tablero.casillas[mx][my]
                        if casilla.descubierta:
                            self.tablero.descubrir_adyacentes(mx, my)
                        else:
                            self.tablero.descubrir_casilla(mx, my)
                    case 3:
                        self.tablero.marcar_casilla(mx, my)

        keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_r] and (self.game_over or self.tablero.limpio()):
            self.tablero = Tablero(self.filas, self.columnas, self.cantidad_de_bombas)
            self.game_over = False
            self.tiempo = 0

    def logica(self):
        if self.tablero.explosion:
            self.tablero.explotar_minas(self.sonidos["Explosion"])
            self.game_over = True

    def actualizar_titulo(self):
        if not (self.game_over or self.tablero.limpio()):
            pygame.display.set_caption("Busca Minas | {faltantes} | {tiempo:03} ".format(faltantes = self.cantidad_de_bombas - self.tablero.cantidad_marcadas, tiempo= self.tiempo // 1000)) 

    def dibujar(self):
        self.pantalla.fill("purple")
        self.actualizar_titulo()
        for c in range(self.columnas):
                for f in range(self.filas):

                    coordenadas : tuple[int,int] = (c*self.tamanio_de_casilla, f*self.tamanio_de_casilla)
                    casilla = self.tablero.casillas[c][f]
                    archivo : str = "casilla_" + ("descubierta_" if casilla.descubierta else "cubierta_" ) + str((c+f)%2)
                    terreno : pygame.Surface = self.recursos[archivo]
                    self.pantalla.blit(terreno, coordenadas)
                    if casilla.marcada:
                        archivo = "marcador"
                    elif casilla.descubierta:
                        if casilla.mina:
                            archivo = "bomba"
                        else:
                            archivo = str(casilla.proximidades)
                    especial : pygame.Surface = self.recursos[archivo]
                    self.pantalla.blit(especial ,coordenadas)

        if self.game_over:
            self.pantalla.blit(self.recursos["game_over"], self.recursos["game_over"].get_rect(center= (self.pantalla_ancho//2, self.pantalla_alto//2)))
        if self.tablero.limpio(): 
            self.pantalla.blit(self.recursos["ganador"], self.recursos["ganador"].get_rect(center= (self.pantalla_ancho//2, self.pantalla_alto//2)))
        pygame.display.flip()

juego = Juego()
if __name__ == "__main__":
    juego.bucle_principal()