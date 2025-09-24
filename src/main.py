# Este archivo es el punto de entrada de la aplicación Memorice.
# Aquí se configuran las rutas principales y se inicializa el juego.

import os
from juego import Memorice  # Importamos la clase que contiene toda la lógica del juego

if __name__ == "__main__":
    # Obtenemos la ruta absoluta de la carpeta actual (donde está main.py → src/)
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

    # Construimos la ruta absoluta a la carpeta de imágenes (subimos un nivel y entramos a /imagenes)
    ruta_imagenes = os.path.abspath(os.path.join(carpeta_actual, "../imagenes"))

    # Construimos la ruta absoluta a la carpeta donde se guardarán los resultados (/results)
    ruta_resultados = os.path.abspath(os.path.join(carpeta_actual, "../results"))

    # Creamos una instancia del juego Memorice con:
    # - Tablero de 6x6 (18 pares de cartas)
    # - Ruta a las imágenes de las cartas
    # - Ruta donde se almacenarán los resultados y métricas
    juego = Memorice(
        tamano_tablero=6,
        carpeta_imagenes=ruta_imagenes,
        ruta_resultados=ruta_resultados
    )

    # Iniciamos el juego llamando al método principal de la clase Memorice
    juego.iniciar()
