# Proyecto Memorice IA

**Autor:** Pamela Veloso - Sebastián Saravia 
**Curso:** Aplicaciones de Inteligencia Artificial  
**Fecha:** [24-09-2025]

---
## Cómo ejecutarlo paso a paso

1. Clonar el repositorio:
   git clone https://github.com/Pamela-Veloso/Proyecto-memorice-IA.git
2. Entrar a la carpeta del proyecto:
   cd Proyecto-memorice-IA
3. Activar el entorno virtual (si usan Windows):
   venv\Scripts\activate
4. Instalar dependencias:
   pip install -r requirements.txt
   Dentro de esto esta la librería Pillow, sino correr el comando:
   pip install pillow
5. Ejecutar el juego:
   python src/main.py

## Contenido del repositorio

## Descripción
Este proyecto es un juego **Memorice (Memory)** con un agente automático (IA) que juega sobre un **tablero 6×6 (36 cartas, 18 parejas)** implementado en Python con **interfaz gráfica (Tkinter)**.  
El agente memoriza las cartas que aparecen y utiliza esa información para emparejarlas. El sistema mide y reporta el **tiempo de resolución** y el **número de movimientos**, y guarda un registro de cada ejecución en la carpeta `results/`.


---

## Objetivos
- Implementar un agente que resuelva el juego usando un **algoritmo de búsqueda informada** (basado en memoria hash simple).  
- Reportar el **tiempo de resolución** del juego y el número de movimientos realizados.  

---

## Algoritmo de Búsqueda usado

La IA funciona de la siguiente manera:

1. Guarda en un **diccionario (hash)** la posición de cada carta que ya ha sido revelada.
2. Antes de elegir cartas al azar, busca en su **memoria** si ya conoce un par.
3. Si encuentra un par conocido, selecciona esas cartas primero (movimiento optimizado).
4. Si no hay pares conocidos, elige cartas al azar.
5. Cada jugada que hace la IA actualiza su memoria.

Este método es un **algoritmo de búsqueda informada**, porque la IA utiliza información previa para tomar decisiones más eficientes.

---

## Estructura del Proyecto

ProyectoMemorice/
│
├─ src/
│   ├─ main.py              # archivo principal que inicia el juego
│   └─ juego.py             # lógica del juego y de la IA
│
├─ imagenes/                # aquí van las 18 imágenes de las cartas
│   ├─ img1.png
│   ├─ img2.png
│   ├─ ...
│   └─ img18.png
│
├─ results/                 # se guardan los resultados de las ejecuciones (tiempos, movimientos, etc.)
│   └─ resultados.txt       # generado automáticamente al jugar
│
├─ venv/                    # entorno virtual de Python
│
├─ requirements.txt         # dependencias necesarias (tkinter, pillow)
│
└─ README.md                # documentación principal del proyecto


## Ejecución del juego

Correr el siguiente script en la terminal de visualstudio, para que el juego inicio automáticamente: 

python src/main.py

- Se abrirá una ventana con el tablero 6×6.

- La IA comienza a jugar automáticamente.

- Al terminar, aparecerá un mensaje con movimientos y tiempo, y se guardará un archivo JSON en results/.

## Documentación del código

1) El archivo src/main.py:

           - Resuelve rutas (imagenes, results) y crea la instancia del juego.

           - Ejecuta juego.iniciar().

2) El archivo src/juego.py:

    Clase Memorice con:

           - Carga y preprocesado de imágenes.

           - Generación del tablero (duplicación de 18 imágenes, shuffle).

           - Interfaz con tkinter (labels para cada carta).

           - Lógica del agente IA y funciones para revelar/ocultar cartas.

           - Cálculo de movimientos y tiempo.

           - Guardado de resultados en results/resultado_<timestamp>.json.

## Algoritmo de búsqueda implementado (Justificación)

**Idea general:**

- El agente usa un enfoque muy simple pero efectivo: **memoria hash + exploración aleatoria**.

**Comportamiento por turno (pseudocódigo simple):**

1) Si ya conoce un par (por memoria), lo selecciona y lo empareja.
2) Si no hay par conocido:
            Selecciona dos posiciones que aún no estén emparejadas (aleatorio).
            Revela la primera carta → la guarda en memoria.
            Revela la segunda carta → también la guarda.

3) Si las dos cartas coinciden → las marca como emparejadas.
4) Repite hasta completar todas las parejas.

## Estructuras

memoria_ia: diccionario {imagen: posicion} que guarda la última posición vista para cada imagen.

Búsqueda de pareja conocida: comprobación en memoria_ia y búsqueda de la segunda aparición con .index().

## Complejidad y justificación

Acceso a la memoria: O(1) promedio (lookup en diccionario).

Búsqueda de la otra instancia con .index() es O(n) en peor caso, pero el tablero es pequeño (36 elementos), por lo que es eficiente en la práctica.

**Este es un algoritmo simple que representa una búsqueda informada porque usa información acumulada (memoria) para reducir errores, en contraste con un agente totalmente aleatorio**.

## Cómo probamos el agente (metodología experimental)

Para evaluar la eficiencia (optimización) y la correcta ejecución:

1) Ejecutar el juego N veces (por ejemplo N = 5), cada ejecución se cierra al completar.
2) Cada ejecución genera un archivo JSON en results/ con dos campos:

{ "movimientos": 52, "tiempo_segundos": 34 }

3) Agregar todas las ejecuciones y calcular:

     -Media y desviación estándar de movimientos.
     -Media y desviación estándar de tiempo.

4) Interpretación:

     -Menor media de movimientos → agente más eficiente.
     -Menor media de tiempo → agente más rápido.

## Requisitos del Proyecto que se cumplen:

**1) Correcta ejecución del algoritmo:**

      El juego termina correctamente y el agente completa la partida.

      Se guardan resultados por ejecución (JSON) en results/.

**2) Optimización del agente:**

       El agente usa memoria para emparejar pares conocidos antes de explorar al azar.

       Método experimental propuesto (ejecutar N runs y comparar media) permite cuantificar eficiencia frente a un agente aleatorio.

**3) Calidad del código:**

       Código modular (clase Memorice), funciones con propósito único, nombres en español y comentarios.

       README con información del proyecto.

**4) Uso y justificación del algoritmo de búsqueda:**

     Etrade-off entre simplicidad y efectividad; apropiado para un tablero pequeño y para demostrar búsqueda informada. 
     
     “Una búsqueda informada simple basada en memoria (hash). Primero busca pares conocidos en su memoria; si no los hay, explora aleatoriamente.”

¿Por qué no usamos un algoritmo más complejo como A o BFS?*

“El problema es parcialmente observable: la información se revela al voltear cartas. A* o BFS aplican en espacios totalmente observables; sería necesario modelar creencias (POMDP), que es más complejo y no requerido para esta práctica.”
