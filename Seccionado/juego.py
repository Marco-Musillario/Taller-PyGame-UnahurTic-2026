import pygame
from tablero import Tablero

# Creacion de la ventana 

class Juego:
    def __init__(self) -> None:
        pygame.init()
        self.activo : bool = True
        self.derrota : bool = False
        self.victoria : bool = False

        self.filas : int = 16
        self.columnas : int = 16
        self.cantidad_de_bombas : int = 40

        self.tamanio_de_casilla : int = 32
        self.pantalla_ancho : int = self.columnas * self.tamanio_de_casilla
        self.pantalla_alto : int = self.filas * self.tamanio_de_casilla
        
        self.pantalla : pygame.Surface = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))

        self.tablero = Tablero(self.filas, self.columnas, self.cantidad_de_bombas)
        
        self.recursos : dict[str, pygame.Surface ] = {}
        self.fuente : pygame.font.Font = pygame.font.Font("assets/bytebounce.medium.ttf", size=50)

        self.recursos["casilla_cubierta_0"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_cubierta_0"].fill("darkolivegreen3")
        self.recursos["casilla_cubierta_1"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_cubierta_1"].fill("darkolivegreen2")
        
        self.recursos["casilla_descubierta_0"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_descubierta_0"].fill("burlywood3")
        self.recursos["casilla_descubierta_1"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla)).convert()
        self.recursos["casilla_descubierta_1"].fill("burlywood2")

        self.recursos["marcador"] = pygame.image.load("assets/Marcador.png").convert_alpha()
        self.recursos["bomba"] = pygame.image.load("assets/Bomba.png").convert_alpha()

        self.recursos["cartel_derrota"]= pygame.image.load("assets/game_over.png").convert()
        self.recursos["cartel_victoria"]= pygame.image.load("assets/ganador.png").convert()

        colores_numeros : list[str] = ["blue", "green", "red", "blue4", "darkred", "cyan4", "black", "dimgrey"]
        self.recursos["0"] = pygame.Surface((self.tamanio_de_casilla,self.tamanio_de_casilla), pygame.SRCALPHA).convert_alpha()
    
        for i in range(8):
            numero : int = i + 1
            
            numero_imagen : pygame.Surface = self.fuente.render( text= str(numero), antialias= True, color= colores_numeros[i])
            fondo : pygame.Surface = pygame.Surface( size= (self.tamanio_de_casilla,self.tamanio_de_casilla), flags= pygame.SRCALPHA)
            fondo.blit(numero_imagen, numero_imagen.get_rect(center=(self.tamanio_de_casilla // 2 , self.tamanio_de_casilla // 2)))
            self.recursos[str(numero)] = fondo.convert_alpha()

    def procesar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.activo = False
            if event.type == pygame.MOUSEBUTTONDOWN and not (self.derrota or self.victoria):
                mx : int = event.pos[0] // self.tamanio_de_casilla
                my : int = event.pos[1] // self.tamanio_de_casilla
                match event.button:
                    case 1:
                        if not self.tablero.generado:
                            self.tablero.generar_bombas((mx,my))
                        self.tablero.descubrir_casilla(mx, my)
                    case 3:
                        self.tablero.marcar_casilla(mx, my)

        keys = pygame.key.get_just_pressed()
                
        if keys[pygame.K_r] and (self.derrota or self.victoria):
            self.tablero = Tablero(self.filas, self.columnas, self.cantidad_de_bombas)
            self.derrota = False

    def logica(self):
        if self.tablero.explosion:
            self.derrota = True
        self.victoria = self.tablero.limpio()

    def dibujar(self):
        self.pantalla.fill("purple")

        for c in range(self.columnas):
            for f in range(self.filas):
                coordenadas : tuple[int,int] = (c*self.tamanio_de_casilla, f*self.tamanio_de_casilla)
                casilla = self.tablero.casillas[c][f]
                archivo : str = "casilla_" + ("descubierta_" if casilla.descubierta else "cubierta_" ) + str((c+f)%2)
                terreno : pygame.Surface = self.recursos[archivo]
                self.pantalla.blit(terreno, coordenadas)
                if casilla.marcada:
                    self.pantalla.blit(self.recursos["marcador"], coordenadas)
                elif casilla.descubierta:
                    simbolo : str = "bomba" if casilla.mina else str(casilla.proximidades)
                    self.pantalla.blit(self.recursos[simbolo], coordenadas)

        if self.derrota:
            self.pantalla.blit(self.recursos["cartel_derrota"], self.recursos["cartel_derrota"].get_rect(center= (self.pantalla_ancho//2, self.pantalla_alto//2)))
        elif self.victoria: 
            self.pantalla.blit(self.recursos["cartel_victoria"], self.recursos["cartel_victoria"].get_rect(center= (self.pantalla_ancho//2, self.pantalla_alto//2)))

        pygame.display.flip()

    def bucle_principal(self):
        while self.activo:
            self.procesar_eventos()
            self.logica()
            self.dibujar()
        pygame.quit()

if __name__ == "__main__":
    juego = Juego()
    juego.bucle_principal()