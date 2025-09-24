# Este archivo inicia la app, para ejecutarlo

import os
from juego import Memorice

if __name__ == "__main__":
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))  # src/
    ruta_imagenes = os.path.abspath(os.path.join(carpeta_actual, "../imagenes"))
    ruta_resultados = os.path.abspath(os.path.join(carpeta_actual, "../results"))

    juego = Memorice(tamano_tablero=6, carpeta_imagenes=ruta_imagenes,
                      ruta_resultados=ruta_resultados)
    juego.iniciar()
