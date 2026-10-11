import pygame, random

generador = random.Random()

class Casilla:
    def __init__(self):
        self.mina = False
        self.descubierta = False
        self.marcada = False
        self.proximidades = 0

class Tablero:
    def __init__(self, filas, columnas, cantidad_de_bombas):
        self.filas = filas
        self.columnas = columnas
        self.cantidad_total_de_bombas = cantidad_de_bombas
        self.casillas : list[list[Casilla]]= []
        self.explosion = False
        self.generado = False

        for c in range(columnas):
            columna = []
            for f in range(filas):
                columna.append(Casilla())
            self.casillas.append(columna)

    def generar_bombas(self, evitar : tuple[int,int] | None = None):
        cantidad_puesta = 0
        while cantidad_puesta < self.cantidad_total_de_bombas:
            x = random.randrange(self.columnas)
            y = random.randrange(self.filas)
            if not self.casillas[x][y].mina and (x,y) != evitar:
                self.casillas[x][y].mina = True
                self.generar_proximidades(x,y)
                cantidad_puesta = cantidad_puesta + 1
                
    def generar_proximidades(self, _x, _y):
        for x in range(_x-1, _x+2):
            if x >= 0 and x < self.columnas:
                for y in range(_y-1, _y+2):
                    if y >= 0 and y < self.filas:
                        self.casillas[x][y].proximidades = self.casillas[x][y].proximidades + 1

    def descubrir_casilla(self, _x, _y):
        if self.casillas[_x][_y].marcada or self.casillas[_x][_y].descubierta:
            return 
        
        self.casillas[_x][_y].descubierta = True

        # Game over
        if self.casillas[_x][_y].mina:
            self.explosion = True
            return

        # Si hay alguna mina cerca, solo se revela esta casilla
        if self.casillas[_x][_y].proximidades != 0:
            return

        # Si no hay minas cerca, se revelan las casillas vecinas
        for x in range(_x-1, _x+2):
                    if x >= 0 and x < self.columnas:
                        for y in range(_y-1, _y+2):
                            if y >= 0 and y < self.filas:
                                self.descubrir_casilla(x,y)     

    def explotar_minas(self):
        for x in range(self.columnas):
            for y in range(self.filas):
                if self.casillas[x][y].mina and not self.casillas[x][y].marcada:
                    self.casillas[x][y].descubierta = True

    def cantidad_descubiertas_limpias(self):
        cantidad = 0
        for columna in self.casillas:
            for casilla in columna:
                if casilla.descubierta and not casilla.mina:
                    cantidad = cantidad + 1
        return cantidad
                     

def main():
    pygame.init()

    running = True
    game_over = False

    filas = 16
    columnas = 16
    cantidad_de_bombas = 40
    casillas_limpias = (filas * columnas) - cantidad_de_bombas

    tamanio_de_casilla = 32
    pantalla_ancho = filas * tamanio_de_casilla
    pantalla_alto = columnas * tamanio_de_casilla

    recursos = {}
    recursos["bomba"] = pygame.image.load("assets/Bomba.png")
    recursos["marcador"] = pygame.image.load("assets/Marcador.png")
    recursos["font"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=50)
    recursos["font2"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=20)

    recursos["casilla_cubierta_1"] = pygame.surface.Surface((32,32))
    recursos["casilla_cubierta_1"].fill("darkolivegreen3")
    recursos["casilla_cubierta_2"] = pygame.surface.Surface((32,32))
    recursos["casilla_cubierta_2"].fill("darkolivegreen2")
    
    recursos["casilla_descubierta_1"] = pygame.surface.Surface((32,32))
    recursos["casilla_descubierta_1"].fill("burlywood3")
    recursos["casilla_descubierta_2"] = pygame.surface.Surface((32,32))
    recursos["casilla_descubierta_2"].fill("burlywood2")

    recursos["game_over"]= pygame.image.load("assets/game_over.png")
    recursos["ganador"]= pygame.image.load("assets/ganador.png")

    colores_numeros = ["blue", "green", "red", "blue4", "darkred", "cyan4", "black", "dimgrey"]
    recursos["0"] = pygame.surface.Surface((32,32), pygame.SRCALPHA)

    for i in range(8):
        numero = i + 1
        surf1 = recursos["font"].render( text= str(numero), antialias= True, color= colores_numeros[i])
        surf2 = pygame.surface.Surface( size= (32,32), flags= pygame.SRCALPHA)
        surf2.blit(surf1, surf1.get_rect(center=(tamanio_de_casilla // 2 , tamanio_de_casilla // 2)))
        recursos[str(numero)] = surf2

    pygame.display.set_caption("Busca minas")
    pygame.display.set_icon(recursos["bomba"])
    
    pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
    
    clock = pygame.time.Clock()

    tablero = Tablero(filas, columnas, cantidad_de_bombas)
    tablero_limpio = False

    # Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx = event.pos[0] // 32
                my = event.pos[1] // 32
                match event.button:
                    case 1:
                        if not tablero.generado:
                            tablero.generado = True
                            tablero.generar_bombas((mx,my))
                        tablero.descubrir_casilla(mx, my)
                    case 3:
                        if not tablero.casillas[mx][my].descubierta:
                            tablero.casillas[mx][my].marcada = not tablero.casillas[mx][my].marcada

        keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_r] and (game_over or tablero_limpio):
            tablero = Tablero(filas, columnas, cantidad_de_bombas)
            game_over = False
            tablero_limpio = False

        if tablero.explosion:
            tablero.explotar_minas()
            game_over = True

        if tablero.cantidad_descubiertas_limpias() == casillas_limpias:
            tablero_limpio = True

        pantalla.fill("purple")
        
        for c in range(columnas):
                for f in range(filas):

                    coordenadas = (c*32, f*32)
                    paridad = ((c+f)%2 == 0)
                    if not tablero.casillas[c][f].descubierta :
                        terreno = recursos["casilla_cubierta_1"] if paridad else recursos["casilla_cubierta_2"]
                        pantalla.blit(terreno, coordenadas)
                        if tablero.casillas[c][f].marcada:
                            pantalla.blit(recursos["marcador"], coordenadas)
                    else:
                        terreno = recursos["casilla_descubierta_1"] if paridad else recursos["casilla_descubierta_2"]
                        pantalla.blit(terreno, coordenadas)
                        if tablero.casillas[c][f].mina:
                            pantalla.blit(recursos["bomba"], coordenadas)
                        else:
                            pantalla.blit(recursos[str(tablero.casillas[c][f].proximidades)], coordenadas)
        if game_over:
            pantalla.blit(recursos["game_over"], recursos["game_over"].get_rect(center= (pantalla_ancho//2, pantalla_alto//2)))
        if tablero_limpio: 
            pantalla.blit(recursos["ganador"], recursos["ganador"].get_rect(center= (pantalla_ancho//2, pantalla_alto//2)))
        pygame.display.flip()
        clock.tick(60)

    

    pygame.quit()
    return

if __name__ == "__main__":
    main()