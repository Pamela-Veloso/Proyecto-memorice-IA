# Este archivo contiene la lógica del juego, la interfaz gráfica con Tkinter 
# y la IA con algoritmo de búsqueda simple (hash para memorizar cartas).

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import time
import json

CARD_SIZE = 80  # tamaño de cartas
DELAY = 1000    # milisegundos entre jugadas de la IA

class Memorice:
    def __init__(self, tamano_tablero, carpeta_imagenes, ruta_resultados):
        self.tamano_tablero = tamano_tablero
        self.total_cartas = tamano_tablero * tamano_tablero
        self.carpeta_imagenes = carpeta_imagenes
        self.ruta_resultados = ruta_resultados

        # Crear ventana primero
        self.root = tk.Tk()
        self.root.title("Memorice IA")
        self.labels = []

        # Cargar imágenes
        archivos = os.listdir(self.carpeta_imagenes)[:self.total_cartas // 2]
        self.imagenes = [self._cargar_imagen(f) for f in archivos]

        # Duplicar y barajar
        self.tablero = self.imagenes * 2
        random.shuffle(self.tablero)

        # Estado del juego
        self.reveladas = [False] * self.total_cartas
        self.marcadas = [False] * self.total_cartas
        self.memoria_ia = {}
        self.movimientos = 0
        self.parejas_encontradas = 0
        self.tiempo_inicio = None

    # -------------------------------
    #  Carga de imagen con fondo blanco
    # -------------------------------
    def _cargar_imagen(self, archivo):
        ruta = os.path.join(self.carpeta_imagenes, archivo)
        img = Image.open(ruta).convert("RGBA")
        fondo = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(fondo, img)
        img = img.resize((CARD_SIZE, CARD_SIZE), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    # -------------------------------
    #  Crear reverso de carta
    # -------------------------------
    def _hacer_reverso(self):
        img = Image.new("RGBA", (CARD_SIZE, CARD_SIZE), (200, 200, 200, 255))
        return ImageTk.PhotoImage(img)

    # -------------------------------
    #  Iniciar juego
    # -------------------------------
    def iniciar(self):
        self.tiempo_inicio = time.time()
        self.card_back = self._hacer_reverso()

        # Crear tablero visual
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        for i in range(self.total_cartas):
            lbl = tk.Label(frame, image=self.card_back, bd=2, relief="raised")
            r, c = divmod(i, self.tamano_tablero)
            lbl.grid(row=r, column=c, padx=5, pady=5)
            lbl.bind("<Button-1>", lambda e, idx=i: self.on_click(idx))
            self.labels.append(lbl)

        self.root.after(DELAY, self.jugar_ia)
        self.root.mainloop()

    # -------------------------------
    #  Click manual (opcional)
    # -------------------------------
    def on_click(self, idx):
        if not self.reveladas[idx] and not self.marcadas[idx]:
            self.revelar_carta(idx)

    # -------------------------------
    #  IA juega
    # -------------------------------
    def jugar_ia(self):
        if self.parejas_encontradas == self.total_cartas // 2:
            self.terminar_juego()
            return

        # Buscar par conocido en memoria
        for img, idx in list(self.memoria_ia.items()):
            if not self.marcadas[idx]:
                try:
                    j = self.tablero.index(img, idx + 1)
                except ValueError:
                    continue
                if not self.marcadas[j]:
                    self.revelar_carta(idx)
                    self.revelar_carta(j)
                    self.chequear_par(idx, j)
                    self.root.after(DELAY, self.jugar_ia)
                    return

        # Elegir dos cartas al azar
        ocultas = [i for i in range(self.total_cartas)
                   if not self.reveladas[i] and not self.marcadas[i]]
        if len(ocultas) >= 2:
            i, j = random.sample(ocultas, 2)
            self.revelar_carta(i)
            self.revelar_carta(j)
            self.chequear_par(i, j)

        self.root.after(DELAY, self.jugar_ia)

    # -------------------------------
    #  Revelar carta
    # -------------------------------
    def revelar_carta(self, idx):
        self.labels[idx].config(image=self.tablero[idx])
        self.reveladas[idx] = True
        self.memoria_ia[self.tablero[idx]] = idx

    # -------------------------------
    #  Revisar si las cartas coinciden
    # -------------------------------
    def chequear_par(self, i, j):
        self.movimientos += 1
        if self.tablero[i] == self.tablero[j]:
            self.marcadas[i] = True
            self.marcadas[j] = True
            self.parejas_encontradas += 1
        else:
            self.root.after(500, lambda: (self.ocultar_carta(i), self.ocultar_carta(j)))

    # -------------------------------
    #  Ocultar carta
    # -------------------------------
    def ocultar_carta(self, idx):
        if not self.marcadas[idx]:
            self.labels[idx].config(image=self.card_back)
            self.reveladas[idx] = False

    # -------------------------------
    #  Guardar resultados
    # -------------------------------
    def terminar_juego(self):
        tiempo_total = int(time.time() - self.tiempo_inicio)
        messagebox.showinfo("¡Juego terminado!",
                            f"Movimientos: {self.movimientos}\nTiempo: {tiempo_total} segundos")
        # Guardar en results
        os.makedirs(self.ruta_resultados, exist_ok=True)
        archivo = os.path.join(self.ruta_resultados, f"resultado_{int(time.time())}.json")
        with open(archivo, "w") as f:
            json.dump({"movimientos": self.movimientos,
                       "tiempo_segundos": tiempo_total}, f)
