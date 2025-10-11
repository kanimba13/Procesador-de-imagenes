import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import Libimg as li
#Importar la libreria de transformaciones
# Variable global
imagen_actual = None

def abrir_imagen():
    global imagen_actual
    ruta = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes","*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"), ("Todos","*.*")]
    )
    if not ruta:
        return
    imagen_actual = Image.open(ruta).resize((400,300))
    mostrar_imagen(imagen_actual)

def mostrar_imagen(img):
    foto = ImageTk.PhotoImage(img)
    lbl.config(image=foto)
    lbl.image = foto

def aplicar_brillo_btn():
    global imagen_actual
    if imagen_actual is None:
        return
    try:
        while True:
            valor = float(entry.get())  # lee el valor del Entry
            if not -1.0 <= valor <= 1.0:
                messagebox.showerror("Error", "Ingresa un número entre -1.0 y 1.0")
                return
            break
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido")
        return

    # Convertir PIL a numpy
    img_np = np.array(imagen_actual, dtype=np.float32)

    # Usar directamente la función de brillo
    img_np = li.brillo(img_np, valor)

    # Convertir numpy a PIL
    imagen_np = Image.fromarray(img_np.astype(np.uint8))

    mostrar_imagen(imagen_np)

# -------- Interfaz --------
root = tk.Tk()
root.title("Visor de imágenes con brillo")
root.geometry("600x450")

btn = tk.Button(root, text="Abrir imagen...", command=abrir_imagen)
btn.place(x=10,y=10)

lbl_texto = tk.Label(root, text="Brillo:")
lbl_texto.place(x=150,y=15)

entry = tk.Entry(root)          #Caja para ingresar el texto
entry.place(x=200,y=15, width=60)
entry.insert(0,"0.1")

btn_brillo = tk.Button(root, text="Aplicar brillo", command=aplicar_brillo_btn)
btn_brillo.place(x=270,y=10)

lbl = tk.Label(root)
lbl.place(x=100,y=60)

root.mainloop()