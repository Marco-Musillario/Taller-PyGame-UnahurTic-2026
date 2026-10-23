# Taller-PyGame-UnahurTic-2026

Repositorio de organización para el taller de PyGame que se va a dar en la jornada **Unahur Tic 2026**.

En el taller vamos a trabajar sobre un **Buscaminas** hecho con PyGame. Partimos de un juego que ya funciona y, entre todos, lo vamos a leer, entender y mejorar con una serie de retos. Al final, cada persona puede seguir agregando las mejoras que quiera en su propio repositorio.

### Página de [PyGame](https://pyga.me/)

**IMPORTANTE:** existen dos versiones de pygame: la original (llamada `pygame`) y `pygame-ce`, que está más actualizada y tiene más features. Por lo tanto, vamos a usar **`pygame-ce`**.

---

## El proyecto: Buscaminas

El juego es un Buscaminas clásico de 16x16 casillas con 40 bombas. Tiene:

- Tablero generado al azar en el primer clic (la casilla del primer clic nunca es una bomba).
- Descubrimiento automático de las casillas vecinas cuando no hay bombas cerca.
- Banderas para marcar las casillas sospechosas.
- Cronómetro y contador de banderas en el título de la ventana.
- Carteles de victoria y derrota, y sonido de explosión.

### Cómo se juega

| Acción | Control |
|---|---|
| Descubrir una casilla | Clic izquierdo |
| Marcar / desmarcar con bandera | Clic derecho |
| Reiniciar al terminar la partida | Tecla `R` |

El título de la ventana muestra `Busca Minas | banderas restantes | segundos`.

## Requisitos e instalación

Necesitas Python 3 y `pygame-ce` (versión 2.5.8 o superior). Está indicado en `requirements.txt`:

```
pygame-ce>=2.5.8
```

Instalación:

```bash
pip install -r requirements.txt
```

**Cuidado:** si tienes instalado el `pygame` original, desinstálalo antes (`pip uninstall pygame`), porque ambos paquetes usan el mismo nombre de módulo y pueden pisarse.

Para ejecutarlo, **hazlo desde la carpeta del proyecto**, porque las rutas a `assets/` son relativas:

```bash
python juego.py
```

## Estructura del código

| Archivo | Contenido |
|---|---|
| `juego.py` | Clase `Juego`: ventana, recursos (imágenes, fuente, sonido), bucle principal, eventos, lógica y dibujo. |
| `tablero.py` | Clases `Casilla` y `Tablero`: generación de bombas, números de proximidad, banderas, descubrimiento de casillas y condición de victoria. |
| `assets/` | Imágenes, fuente y sonido que usa el juego. |

El bucle principal de `Juego` repite en cada frame tres pasos: `procesar_eventos()`, `logica()` y `dibujar()`. Conviene tenerlo presente para ubicar dónde va cada cambio.

---

## Retos

Cada reto está pensado para resolverse en el código del taller. Están ordenados de menor a mayor dificultad, aproximadamente. Un buen método de trabajo: **un reto, un commit**.

### Básicos

**Reto 1: clic derecho solo después del primer clic izquierdo**
Hoy se puede poner una bandera antes de empezar. Si el primer clic cae justo sobre esa bandera, se generan las bombas pero no se descubre nada, y el siguiente clic ya no está protegido. Impide marcar casillas hasta que se haya hecho al menos un clic izquierdo.
*Pista:* el tablero ya sabe si las bombas fueron generadas (`generado`).

**Reto 2: reemplazar el contador negativo por una validación**
Se pueden poner más banderas que bombas y el contador del título pasa a ser negativo. Cambia el comportamiento para que no se puedan colocar más banderas que bombas.
*Pista:* mira `marcar_casilla` y `cantidad_marcadas` en `tablero.py`.

**Reto 3: más imágenes generadas con código**
La bomba y la bandera se cargan desde archivos PNG, mientras que los números ya se generan con código. Reemplaza la bomba, la bandera o los carteles de victoria y derrota por imágenes dibujadas con `pygame.draw` y `pygame.Surface`.
*Pista:* las imágenes están en el diccionario `recursos` de `Juego`.

### Intermedios

**Reto 4: área segura de 3x3 en el primer clic**
Hoy solo la casilla del primer clic está libre de bombas. Haz que también lo estén sus ocho vecinas, de modo que el primer clic siempre abra una zona.
*Atención:* al reservar 9 casillas, la validación de `Tablero.__init__` (bombas contra casillas) también debe cambiar, o con muchas bombas la generación nunca termina.

**Reto 5: reemplazar la recursividad por una implementación iterativa**
`descubrir_casilla` se llama a sí misma para abrir las zonas vacías. Con tableros muy grandes, la recursión puede alcanzar el límite de Python. Reescríbela usando una lista como pila o una cola de casillas pendientes.
*Prueba:* cambia `filas`, `columnas` y la cantidad de bombas en `Juego` para comprobar tu versión en un tablero grande.

**Reto 6: pantalla de score y resumen**
Al terminar la partida, muestra una pantalla de resumen con el tiempo, la cantidad de banderas usadas y si ganaste o perdiste. Opcional: guarda y muestra el mejor tiempo.

### Avanzados

**Reto 7: pantalla de inicio**
Agrega una pantalla inicial con el título del juego y un botón para empezar. Vas a necesitar un **estado del juego** (por ejemplo, `"inicio"`, `"jugando"`, `"resumen"`) que decida qué se dibuja y qué eventos se procesan.

**Reto 8: separar el código en partes más pequeñas**
`Juego` hace muchas cosas a la vez: carga recursos, procesa eventos, calcula la lógica y dibuja. Divide el código en piezas con responsabilidades limitadas (por ejemplo, una clase o módulo para los recursos, otro para el dibujo, otro para la entrada), y verifica que el juego siga funcionando igual.

---

## Más propuestas

Si terminas los retos o prefieres otro camino, prueba alguna de estas ideas:

- **Niveles de dificultad:** fácil, medio y difícil, con distintos tamaños de tablero y cantidad de bombas.
- **Banderas erróneas:** al perder, mostrar con otra imagen las banderas colocadas sobre casillas que no tenían bomba.
- **Carteles que no tapen el tablero:** mostrar el resultado en una franja aparte o de forma que se pueda ver cómo quedó la partida.
- **Marca de interrogación:** un tercer estado para las casillas (cubierta, bandera, interrogación).
- **Pausa:** una tecla que detenga el cronómetro y oculte el tablero.
- **Temas de color:** cambiar los colores del tablero con una tecla o desde el inicio.
- **Más sonidos:** al marcar una casilla, al ganar o al descubrir una zona grande.
- **Pista:** un botón que descubra una casilla segura.
- **Rutas con `Path`:** usar `pathlib` para que el juego funcione sin importar desde qué carpeta se ejecute.
- **Sonido desacoplado:** hoy `Tablero` recibe el sonido para reproducirlo; busca una forma de que solo `Juego` se encargue de él.

---

## Trabaja en tu propio repositorio

Puedes quedarte con el juego y seguir mejorándolo después del taller. Una forma simple:

1. Haz un **fork** de este repositorio en GitHub (o crea uno nuevo con una copia del código).
2. Clónalo en tu computadora:
   ```bash
   git clone <URL-de-tu-fork>
   cd <carpeta-del-repo>
   ```
3. Crea una rama para tus cambios:
   ```bash
   git checkout -b mis-mejoras
   ```
4. Haz **un commit por cada reto o mejora**, con un mensaje que diga qué cambió y por qué:
   ```bash
   git add .
   git commit -m "Impide marcar casillas antes del primer clic izquierdo"
   ```
5. Sube tus cambios:
   ```bash
   git push origin mis-mejoras
   ```

Puedes inventar tus propios retos, cambiar el aspecto del juego o convertirlo en otro juego distinto. Si tienes una idea que te parece buena para el taller, cuéntanosla.

---

## Sobre este README

El README original del repositorio se conserva en [`original.md`](original.md).