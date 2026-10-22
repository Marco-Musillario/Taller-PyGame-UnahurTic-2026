# Importar Pygame y random
import pygame, random

# Crear un generador de números aleatorios
generador = random.Random()

# Definir la clase Casilla y los atributos de cada casilla del tablero
class Casilla:
    def __init__(self):
        self.mina : bool= False           # Indica si la casilla tiene una mina
        self.descubierta : bool = False   # Indica si la casilla ha sido descubierta
        self.marcada : bool = False       # Indica si la casilla ha sido marcada por el jugador
        self.proximidades : int = 0       # Indica la cantidad de minas en las casillas adyacentes

# Definir la clase Tablero y los atributos del tablero de juego
class Tablero:
    def __init__(self, filas : int, columnas : int, cantidad_de_bombas : int) -> None:
        self.filas : int = filas                                                                     # Indica la cantidad de filas del tablero
        self.columnas : int = columnas                                                               # Indica la cantidad de columnas del tablero
        self.cantidad_total_de_bombas : int = cantidad_de_bombas                                     # Indica la cantidad total de bombas en el tablero
        self.casillas : list[list[Casilla]] = []                                                     # Lista de listas que representa las casillas del tablero
        self.explosion : bool = False                                                                # Indica si ha ocurrido una explosión en el juego
        self.generado : bool = False                                                                 # Indica si el tablero ha sido generado con minas
        self.casillas_limpias : int = (self.filas * self.columnas) - self.cantidad_total_de_bombas   # Indica la cantidad de casillas sin minas en el tablero

        # Crear las casillas del tablero
        for c in range(columnas):
            columna : list[Casilla] = []          # Lista que representa una columna de casillas
            # Crear las casillas de la columna
            for f in range(filas):
                columna.append(Casilla())         # Agregar una casilla a la columna
            self.casillas.append(columna)         # Agregar la columna al tablero

    # Generar las minas en el tablero evitando la casilla inicial del jugador
    def generar_bombas(self, evitar : tuple[int,int] ) -> None:
        cantidad_puesta : int = 0                 # Contador de la cantidad de minas puestas en el tablero
        # Generar minas aleatoriamente en el tablero hasta alcanzar la cantidad total de bombas
        while cantidad_puesta < self.cantidad_total_de_bombas:
            x : int = generador.randrange(self.columnas) # Generar un número aleatorio para la columna
            y : int = generador.randrange(self.filas)    # Generar un número aleatorio para la fila

            if not self.casillas[x][y].mina and (x,y) != evitar: # Verificar que la casilla no tenga mina y no sea la casilla inicial del jugador
                self.casillas[x][y].mina = True                  # Colocar una mina en la casilla
                self.generar_proximidades(x,y)                   # Generar las proximidades de la casilla con mina
                cantidad_puesta = cantidad_puesta + 1            # Incrementar el contador de minas puestas
        self.generado = True                                     # Indicar que el tablero ha sido generado con minas
                
    # Generar las proximidades de una casilla con mina, incrementando el contador de proximidades de las casillas adyacentes
    def generar_proximidades(self, _x : int, _y : int) -> None:
        # Recorrer las casillas adyacentes a la casilla con mina y aumentar su contador de proximidades
        for x in range(_x-1, _x+2):
            if x >= 0 and x < self.columnas:                                                    # Verificar que la casilla esté dentro del tablero
                for y in range(_y-1, _y+2):                                                     # Recorrer las casillas adyacentes a la casilla con mina
                    if y >= 0 and y < self.filas:                                               # Verificar que la casilla esté dentro del tablero
                        self.casillas[x][y].proximidades = self.casillas[x][y].proximidades + 1 # Aumentar el contador de proximidades de la casilla adyacente

    # Marcar o desmarcar una casilla como mina
    def marcar_casilla(self, x : int, y : int):
        if not self.casillas[x][y].descubierta:                           # Verificar que la casilla no esté descubierta
            self.casillas[x][y].marcada = not self.casillas[x][y].marcada # Marcar o desmarcar la casilla como mina

    # Descubrir una casilla y sus adyacentes si no hay minas cerca
    def descubrir_casilla(self, _x : int, _y : int) -> None:
        if self.casillas[_x][_y].marcada or self.casillas[_x][_y].descubierta: # Verificar que la casilla no esté marcada ni descubierta
            return                                                             # Si la casilla está marcada o descubierta, no hacer nada
        
        self.casillas[_x][_y].descubierta = True # Marcar la casilla como descubierta

        # Game over
        if self.casillas[_x][_y].mina: # Verificar si la casilla tiene una mina
            self.explosion = True      # Indicar que ha ocurrido una explosión
            return                     # Salir de la función

        # Si hay alguna mina cerca, solo se revela esta casilla
        if self.casillas[_x][_y].proximidades != 0: # Verificar si la casilla tiene minas cerca
            return                                  # Salir de la función

        # Si no hay minas cerca, se revelan las casillas vecinas
        for x in range(_x-1, _x+2):
            if x >= 0 and x < self.columnas:        # Verificar que la casilla esté dentro del tablero
                # Recorrer las casillas adyacentes a la casilla descubierta y descubrirlas
                for y in range(_y-1, _y+2):
                    if y >= 0 and y < self.filas:   # Verificar que la casilla esté dentro del tablero
                        self.descubrir_casilla(x,y) # Llamar recursivamente a la función para descubrir las casillas adyacentes

    def descubrir_adyacentes(self, _x: int, _y: int) -> None:
        casilla = self.casillas[_x][_y] # Obtener la casilla en las coordenadas dadas

        if not casilla.descubierta:     # Verificar si la casilla no está descubierta
            return                      # Salir de la función

        banderas: int = 0 # Contador de banderas adyacentes a la casilla

        # Contar la cantidad de banderas adyacentes a la casilla
        for x in range(_x - 1, _x + 2):
            if x >= 0 and x < self.columnas:            # Verificar que la casilla esté dentro del tablero
                # Recorrer las casillas adyacentes a la casilla descubierta y contar las banderas
                for y in range(_y - 1, _y + 2):
                    if y >= 0 and y < self.filas:       # Verificar que la casilla esté dentro del tablero
                        if self.casillas[x][y].marcada: # Verificar si la casilla adyacente está marcada como mina
                            banderas += 1               # Incrementar el contador de banderas adyacentes

        if banderas != casilla.proximidades: # Verificar si la cantidad de banderas adyacentes es diferente a la cantidad de minas cerca
            return                           # Salir de la función 

        # Si la cantidad de banderas adyacentes es igual a la cantidad de minas cerca, se revelan las casillas vecinas
        for x in range(_x - 1, _x + 2):
            if x >= 0 and x < self.columnas: # Verificar que la casilla esté dentro del tablero
                # Recorrer las casillas adyacentes a la casilla descubierta y descubrirlas
                for y in range(_y - 1, _y + 2):
                    if y >= 0 and y < self.filas: # Verificar que la casilla esté dentro del tablero
                        if not self.casillas[x][y].marcada: # Verificar si la casilla adyacente no está marcada como mina
                            self.descubrir_casilla(x, y) # Llamar recursivamente a la función para descubrir las casillas adyacentes

    # Explota todas las minas en el tablero y reproduce un sonido de explosión
    def explotar_minas(self, sonido : pygame.Sound) -> None:
        # Recorrer todas las casillas del tablero y descubrir las que tienen minas
        for x in range(self.columnas):
            for y in range(self.filas):
                if self.casillas[x][y].mina: # Verificar si la casilla tiene una mina
                    self.casillas[x][y].descubierta = True # Marcar la casilla como descubierta
                    sonido.play() # Reproducir el sonido de explosión
        self.explosion = False # Indicar que ha ocurrido una explosión

    # Contar la cantidad de casillas descubiertas sin minas
    def cantidad_descubiertas_limpias(self) -> int:
        cantidad : int = 0 # Inicializar el contador de casillas descubiertas sin minas
        # Recorrer todas las casillas del tablero y contar las que están descubiertas y no tienen minas
        for columna in self.casillas:
            for casilla in columna:
                if casilla.descubierta and not casilla.mina: # Verificar si la casilla está descubierta y no tiene mina
                    cantidad = cantidad + 1 # Incrementar el contador de casillas descubiertas sin minas
        return cantidad

    # Verificar si el jugador ha ganado el juego, es decir, si todas las casillas sin minas han sido descubiertas
    def limpio(self) -> bool:
        return self.cantidad_descubiertas_limpias() == self.casillas_limpias # Verificar si la cantidad de casillas descubiertas sin minas es igual a la cantidad total de casillas sin minas

# Definir la clase Juego y los atributos del juego
class Juego:
    # Inicializar el juego y sus atributos
    def __init__(self) -> None:
        pygame.init()                      # Inicializar Pygame
        self.running : bool = True         # Indica si el juego está en ejecución
        self.game_over : bool = False      # Indica si el juego ha terminado por una explosión
        self.win : bool = False            # Indica si el jugador ha ganado el juego
    
        self.filas : int = 16              # Indica la cantidad de filas del tablero
        self.columnas : int = 16           # Indica la cantidad de columnas del tablero
        self.cantidad_de_bombas : int = 40 # Indica la cantidad de bombas en el tablero
    
        self.tamanio_de_casilla : int = 32 # Indica el tamaño de cada casilla en píxeles
        self.pantalla_ancho : int = self.columnas * self.tamanio_de_casilla   # Indica el ancho de la pantalla en píxeles
        self.pantalla_alto : int = self.filas * self.tamanio_de_casilla # Indica el alto de la pantalla en píxeles

        pygame.display.set_caption("Busca minas") # Indica el título de la ventana del juego
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto)) # Indica el tamaño de la ventana del juego

        self.recursos : dict[str, pygame.Surface ]= {} # Diccionario que almacena los recursos gráficos del juego

        self.recursos["bomba"] = pygame.image.load("assets/Bomba.png").convert_alpha()       # Cargar la imagen de la bomba y convertirla a un formato compatible con Pygame
        self.recursos["marcador"] = pygame.image.load("assets/Marcador.png").convert_alpha() # Cargar la imagen del marcador y convertirla a un formato compatible con Pygame
        self.recursos["font"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=50)    # Cargar la fuente de texto y establecer su tamaño
        self.recursos["font2"] = pygame.font.Font("assets/bytebounce.medium.ttf", size=20)   # Cargar la fuente de texto y establecer su tamaño
    
        self.recursos["casilla_cubierta_1"] = pygame.Surface((32,32)).convert() # Crear una superficie para la casilla cubierta y convertirla a un formato compatible con Pygame
        self.recursos["casilla_cubierta_1"].fill("darkolivegreen3") # Rellenar la superficie de la casilla cubierta con un color específico
        self.recursos["casilla_cubierta_2"] = pygame.Surface((32,32)).convert() # Crear una superficie para la casilla cubierta y convertirla a un formato compatible con Pygame
        self.recursos["casilla_cubierta_2"].fill("darkolivegreen2") # Rellenar la superficie de la casilla cubierta con un color específico
        
        self.recursos["casilla_descubierta_1"] = pygame.Surface((32,32)).convert() # Crear una superficie para la casilla descubierta y convertirla a un formato compatible con Pygame
        self.recursos["casilla_descubierta_1"].fill("burlywood3") # Rellenar la superficie de la casilla descubierta con un color específico
        self.recursos["casilla_descubierta_2"] = pygame.Surface((32,32)).convert() # Crear una superficie para la casilla descubierta y convertirla a un formato compatible con Pygame
        self.recursos["casilla_descubierta_2"].fill("burlywood2") # Rellenar la superficie de la casilla descubierta con un color específico
    
        self.recursos["game_over"]= pygame.image.load("assets/game_over.png").convert() # Cargar la imagen de "game over" y convertirla a un formato compatible con Pygame
        self.recursos["ganador"]= pygame.image.load("assets/ganador.png").convert() # Cargar la imagen de "ganador" y convertirla a un formato compatible con Pygame
    
        colores_numeros : list[str] = ["blue", "green", "red", "blue4", "darkred", "cyan4", "black", "dimgrey"] # Lista de colores para los números que indican la cantidad de minas cercanas a una casilla
        self.recursos["0"] = pygame.Surface((32,32), pygame.SRCALPHA).convert_alpha() # Crear una superficie transparente para la casilla sin minas y convertirla a un formato compatible con Pygame
    
        # Crear imágenes para los números del 1 al 8 y almacenarlas en el diccionario de recursos
        for i in range(8):
            numero : int = i + 1 # Indicar el número de minas cercanas a la casilla
            numero_imagen : pygame.Surface = self.recursos["font"].render( text= str(numero), antialias= True, color= colores_numeros[i]) # Renderizar el número como una superficie de Pygame con la fuente y el color especificados
            fondo : pygame.Surface = pygame.Surface( size= (32,32), flags= pygame.SRCALPHA) # Crear una superficie transparente para la casilla con minas y convertirla a un formato compatible con Pygame
            fondo.blit(numero_imagen, numero_imagen.get_rect(center=(self.tamanio_de_casilla // 2 , self.tamanio_de_casilla // 2))) # Dibujar el número en el centro de la superficie de la casilla con minas
            self.recursos[str(numero)] = fondo.convert_alpha() # Convertir la superficie de la casilla con minas a un formato compatible con Pygame y almacenarla en el diccionario de recursos

        self.sonidos : dict[str, pygame.Sound]= {} # Diccionario que almacena los sonidos del juego
        self.sonidos["Explosion"] = pygame.mixer.Sound("assets/explosion.mp3") # Cargar el sonido de explosión y convertirlo a un formato compatible con Pygame
    
        pygame.display.set_icon(self.recursos["bomba"]) # Establecer el ícono de la ventana del juego como la imagen de la bomba
        
        self.reloj = pygame.time.Clock() # Crear un reloj para controlar la velocidad de actualización del juego
    
        self.tablero : Tablero = Tablero(self.filas, self.columnas, self.cantidad_de_bombas) # Crear un tablero de juego con las dimensiones y cantidad de bombas especificadas
        return

    # Bucle principal del juego, que se ejecuta mientras el juego esté en ejecución
    def bucle_principal(self):
        while self.running:
            self.input() # Procesar la entrada del usuario
            self.logica() # Actualizar la lógica del juego
            self.dibujar() # Dibujar el estado actual del juego en la pantalla
            self.reloj.tick(60) # Limitar la velocidad de actualización del juego a 60 fotogramas por segundo
        pygame.quit() # Salir de Pygame y cerrar la ventana del juego

    # Procesar la entrada del usuario, incluyendo eventos de teclado y ratón
    def input(self):
        # Procesar los eventos de Pygame, como cerrar la ventana o hacer clic con el ratón
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Verificar si el usuario ha cerrado la ventana del juego
                self.running : bool = False # Indicar que el juego ya no está en ejecución
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and not self.win: # Verificar si el usuario ha hecho clic con el ratón y el juego no ha terminado ni se ha ganado
                mx : int = event.pos[0] // 32 # Convertir las coordenadas del ratón a las coordenadas de la casilla correspondiente en el tablero
                my : int = event.pos[1] // 32 # Convertir las coordenadas del ratón a las coordenadas de la casilla correspondiente en el tablero
                # Convertir las coordenadas del ratón a las coordenadas de la casilla correspondiente en el tablero
                match event.button:
                    # Verificar si el botón del ratón es el izquierdo (1) o el derecho (3) y realizar la acción correspondiente
                    case 1:
                        if not self.tablero.generado:
                            self.tablero.generar_bombas((mx,my))
                        casilla = self.tablero.casillas[mx][my]
                        if casilla.descubierta:
                            self.tablero.descubrir_adyacentes(mx, my)
                        else:
                            self.tablero.descubrir_casilla(mx, my)
                    # Verificar si el botón del ratón es el derecho (3) y marcar o desmarcar la casilla correspondiente en el tablero
                    case 3:
                        self.tablero.marcar_casilla(mx, my)

        # Verificar si el usuario ha presionado la tecla "R" para reiniciar el juego si ha terminado o se ha ganado
        keys = pygame.key.get_just_pressed()
        
        # Reiniciar el juego si se presiona la tecla "R" y el juego ha terminado o se ha ganado
        if keys[pygame.K_r] and (self.game_over or self.win):
            self.tablero = Tablero(self.filas, self.columnas, self.cantidad_de_bombas) # Crear un nuevo tablero de juego con las dimensiones y cantidad de bombas especificadas
            self.game_over = False # Indicar que el juego no ha terminado
            self.win = False # Indicar que el jugador no ha ganado

    # Actualizar la lógica del juego, verificando si el jugador ha perdido o ganado
    def logica(self):
        if self.tablero.explosion:                                 # Verificar si ha ocurrido una explosión en el juego
            self.tablero.explotar_minas(self.sonidos["Explosion"]) # Reproducir el sonido de explosión y descubrir todas las minas en el tablero
            self.game_over = True                                  # Indicar que el juego ha terminado por una explosión
        elif self.tablero.limpio():                                # Verificar si el jugador ha ganado el juego, es decir, si todas las casillas sin minas han sido descubiertas
            self.win = True                                        # Indicar que el jugador ha ganado el juego

    # Dibujar el estado actual del juego en la pantalla, incluyendo las casillas, minas, marcadores y mensajes de fin de juego
    def dibujar(self):
        self.pantalla.fill("purple") # Rellenar la pantalla con un color de fondo específico
        
        for c in range(self.columnas):
                for f in range(self.filas):

                    coordenadas : tuple[int,int] = (c*32, f*32)                                                                            # Calcular las coordenadas de la casilla en la pantalla
                    paridad : bool = ((c+f)%2 == 0)                                                                                        # Calcular la paridad de la casilla para alternar los colores de las casillas descubiertas y cubiertas
                    if not self.tablero.casillas[c][f].descubierta :                                                                       # Verificar si la casilla no está descubierta
                        terreno : pygame.Surface = self.recursos["casilla_cubierta_1"] if paridad else self.recursos["casilla_cubierta_2"] # Seleccionar la superficie de la casilla cubierta correspondiente según la paridad
                        self.pantalla.blit(terreno, coordenadas)                                                                           # Dibujar la superficie de la casilla cubierta en la pantalla
                        if self.tablero.casillas[c][f].marcada:                                                                            # Verificar si la casilla está marcada como mina
                            self.pantalla.blit(self.recursos["marcador"], coordenadas)                                                     # Dibujar la superficie del marcador en la pantalla
                    else:
                        terreno : pygame.Surface = self.recursos["casilla_descubierta_1"] if paridad else self.recursos["casilla_descubierta_2"] # Seleccionar la superficie de la casilla descubierta correspondiente según la paridad
                        self.pantalla.blit(terreno, coordenadas)                                                                                 # Dibujar la superficie de la casilla descubierta en la pantalla
                        if self.tablero.casillas[c][f].mina:                                                                                     # Verificar si la casilla tiene una mina
                            self.pantalla.blit(self.recursos["bomba"], coordenadas)                                                              # Dibujar la superficie de la bomba en la pantalla
                        else:
                            self.pantalla.blit(self.recursos[str(self.tablero.casillas[c][f].proximidades)], coordenadas)                                # Dibujar la superficie del número de minas cercanas en la pantalla
        if self.game_over:                                                                                                                               # Verificar si el juego ha terminado por una explosión
            self.pantalla.blit(self.recursos["game_over"], self.recursos["game_over"].get_rect(center= (self.pantalla_ancho//2, self.pantalla_alto//2))) # Dibujar la superficie de "game over" en el centro de la pantalla
        if self.win:                                                                                                                                     # Verificar si el jugador ha ganado el juego
            self.pantalla.blit(self.recursos["ganador"], self.recursos["ganador"].get_rect(center= (self.pantalla_ancho//2, self.pantalla_alto//2)))     # Dibujar la superficie de "ganador" en el centro de la pantalla
        pygame.display.flip()                                                                                                                            # Actualizar la pantalla con el contenido dibujado

juego = Juego()             # Crear una instancia de la clase Juego para iniciar el juego
if __name__ == "__main__": # Verificar si el script se está ejecutando directamente y no importado como módulo
    juego.bucle_principal() # Iniciar el bucle principal del juego, que se ejecuta mientras el juego esté en ejecución