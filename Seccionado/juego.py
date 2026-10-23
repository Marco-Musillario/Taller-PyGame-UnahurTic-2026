import pygame

# Creacion de la ventana 

class Juego:
    def __init__(self) -> None:
        pygame.init()
        self.activo : bool = True

        self.filas : int = 16
        self.columnas : int = 16

        self.tamanio_de_casilla : int = 32
        self.pantalla_ancho : int = self.columnas * self.tamanio_de_casilla
        self.pantalla_alto : int = self.filas * self.tamanio_de_casilla
        
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))

    def procesar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.activo = False

    def logica(self):
        pass

    def dibujar(self):
        pass

    def bucle_principal(self):
        while self.activo:
            self.procesar_eventos()
            self.logica()
            self.dibujar()
        pygame.quit()

if __name__ == "__main__":
    juego = Juego()
    juego.bucle_principal()