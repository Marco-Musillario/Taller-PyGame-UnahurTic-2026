import pygame

# Clase juego y estructura basica

class Juego:
    def __init__(self) -> None:
        pygame.init()
        self.activo : bool = True

    def procesar_eventos(self):
        pass

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