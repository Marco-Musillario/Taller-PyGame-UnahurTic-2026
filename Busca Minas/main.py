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
        self.explotado = False

        for c in range(columnas):
            columna = []
            for f in range(filas):
                columna.append(Casilla())
            self.casillas.append(columna)
        self.generar_bombas()

    def generar_bombas(self):
        cantidad_puesta = 0
        while cantidad_puesta < self.cantidad_total_de_bombas:
            x = random.randrange(self.columnas)
            y = random.randrange(self.filas)
            if not self.casillas[x][y].mina:
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
            self.explotado = True
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

def main():
    pygame.init()

    running = True
    filas = 16
    columnas = 16
    tamanio_de_casilla = 32
    cantidad_de_bombas = 40

    recursos = {}
    recursos["bomba"] = pygame.image.load("assets/Bomba.png")
    recursos["marcador"] = pygame.image.load("assets/Marcador.png")
    recursos["font"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=50)

    recursos["casilla_cubierta_1"] = pygame.surface.Surface((32,32))
    recursos["casilla_cubierta_1"].fill("darkolivegreen3")
    recursos["casilla_cubierta_2"] = pygame.surface.Surface((32,32))
    recursos["casilla_cubierta_2"].fill("darkolivegreen2")
    
    recursos["casilla_descubierta_1"] = pygame.surface.Surface((32,32))
    recursos["casilla_descubierta_1"].fill("burlywood3")
    recursos["casilla_descubierta_2"] = pygame.surface.Surface((32,32))
    recursos["casilla_descubierta_2"].fill("burlywood2")

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
    pantalla_ancho = filas * tamanio_de_casilla
    pantalla_alto = columnas * tamanio_de_casilla
    pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
    
    clock = pygame.time.Clock()

    tablero = Tablero(filas, columnas, cantidad_de_bombas)

    # Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx = event.pos[0] // 32
                my = event.pos[1] // 32
                match event.button:
                    case 1:
                        tablero.descubrir_casilla(mx, my)
                        if not tablero.casillas[mx][my].marcada:
                            tablero.casillas[mx][my].descubierta = True
                    case 3:
                        if not tablero.casillas[mx][my].descubierta:
                            tablero.casillas[mx][my].marcada = not tablero.casillas[mx][my].marcada

        pantalla.fill("blue")
        
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
        pygame.display.flip()
        print(clock.tick(60))

    

    pygame.quit()
    return

if __name__ == "__main__":
    main()