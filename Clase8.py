import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Libimg

# --- Variables globales ---
imagen_actual = None
submenu_abierto = None  # Para saber si hay un menú desplegado


# ----------- FUNCIONES PRINCIPALES -----------

def abrir_imagen():
    global imagen_actual
    ruta = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"), ("Todos", "*.*")]
    )
    if not ruta:
        return
    imagen_actual = Image.open(ruta).resize((400, 300))
    mostrar_imagen(imagen_actual)


def guardar_imagen():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "No hay imagen para guardar.")
        return
    ruta = filedialog.asksaveasfilename(
        title="Guardar imagen como",
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp"), ("GIF", "*.gif"), ("TIFF", "*.tiff"), ("Todos", "*.*")]
    )
    if not ruta:
        return
    imagen_actual.save(ruta)
    messagebox.showinfo("Éxito", f"Imagen guardada en:\n{ruta}")


def mostrar_imagen(img):
    foto = ImageTk.PhotoImage(img)
    lbl.config(image=foto)
    lbl.image = foto


# ----------- MENÚS DESPLEGABLES -----------

def cerrar_submenu():
    """Cierra el menú desplegable actual si existe."""
    global submenu_abierto
    if submenu_abierto and submenu_abierto.winfo_exists():
        submenu_abierto.destroy()
        submenu_abierto = None


def menu_archivo(event=None):
    """Despliega un menú con opciones de archivo."""
    global submenu_abierto
    cerrar_submenu()

    submenu_abierto = tk.Toplevel(root)
    submenu_abierto.overrideredirect(True)  # sin bordes ni título
    submenu_abierto.geometry(f"+{btn_archivo.winfo_rootx()}+{btn_archivo.winfo_rooty() + btn_archivo.winfo_height()}")
    submenu_abierto.configure(bg="#e0e0e0")

    opciones = [("Abrir imagen", abrir_imagen),
                ("Guardar imagen", guardar_imagen)]

    for texto, comando in opciones:
        b = tk.Button(submenu_abierto, text=texto, width=20, anchor="w",
                      relief="flat", bg="#f0f0f0", command=lambda c=comando: (c(), cerrar_submenu()))
        b.pack(fill="x", padx=2, pady=1)

    # Cerrar si el usuario hace clic fuera
    submenu_abierto.bind("<FocusOut>", lambda e: cerrar_submenu())
    submenu_abierto.focus_force()
    
def menu_editar(event=None):
    """Despliega un menú con opciones de edición."""
    global submenu_abierto
    cerrar_submenu()

    submenu_abierto = tk.Toplevel(root)
    submenu_abierto.overrideredirect(True)
    submenu_abierto.geometry(f"+{btn_editar.winfo_rootx()}+{btn_editar.winfo_rooty() + btn_editar.winfo_height()}")
    submenu_abierto.configure(bg="#e0e0e0")

    opciones = [
                ("Brillo", aplicar_brillo),
                ("Ajuste RGB", ajustar_rgb),
                ("Extraer RGB", extraer_capas_rgb),
                ("Contraste Log", ajustar_contraste_log),
                ("Contraste Exp", ajustar_contraste_exp),
                ("Rotar", rotar_imagen),
                ("Histograma", histograma),
                ("Negativa", negativa)
                ]


    for texto, comando in opciones:
        b = tk.Button(submenu_abierto, text=texto, width=20, anchor="w",
                      relief="flat", bg="#f0f0f0", command=lambda c=comando: (c(), cerrar_submenu()))
        b.pack(fill="x", padx=2, pady=1)

    submenu_abierto.bind("<FocusOut>", lambda e: cerrar_submenu())
    submenu_abierto.focus_force()

# ----------- FUNCIONES DE EDICIÓN -----------
    #FUNCION BRILLO
def aplicar_brillo():
    """Muestra una barra deslizante (-1 a 1) para ajustar el brillo usando Libimg.brillo()."""
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de aplicar brillo.")
        return

    # Crear ventana flotante
    ventana_brillo = tk.Toplevel(root)
    ventana_brillo.title("Ajustar brillo")
    ventana_brillo.geometry("320x180")
    ventana_brillo.resizable(False, False)
    ventana_brillo.configure(bg="#f5f5f5")

    tk.Label(
        ventana_brillo,
        text="Selecciona el brillo:",
        bg="#f5f5f5",
        font=("Arial", 10)
    ).pack(pady=10)

    # Variable de brillo
    brillo_valor = tk.DoubleVar(value=0.0)

    # Slider
    slider = tk.Scale(
        ventana_brillo,
        from_=-1,
        to=1,
        resolution=0.01,
        orient=tk.HORIZONTAL,
        length=240,
        variable=brillo_valor,
        bg="#f5f5f5"
    )
    slider.pack()

    # Imagen temporal para vista previa
    imagen_original = imagen_actual.copy()

    # Función que aplica el brillo en tiempo real
    def vista_previa(valor):
        global imagen_actual
        valor = float(valor)
        img_np = np.array(imagen_original, dtype=np.float32)
        img_modificada = Libimg.brillo(img_np, valor)
        img_pil = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(img_pil)

    slider.config(command=vista_previa)

    # Función para confirmar el cambio
    def confirmar():
        global imagen_actual
        valor = brillo_valor.get()
        img_np = np.array(imagen_original, dtype=np.float32)
        img_modificada = Libimg.brillo(img_np, valor)
        imagen_actual = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_brillo.destroy()

    # Función para cancelar (restaurar original)
    def cancelar():
        mostrar_imagen(imagen_original)
        ventana_brillo.destroy()

    # Botones inferiores
    frame_botones = tk.Frame(ventana_brillo, bg="#f5f5f5")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=5)


    #FUNCION ROTAR
def rotar_imagen():
    """Muestra una barra deslizante (-180° a 180°) para rotar la imagen usando Libimg.rotar()."""
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de aplicar rotación.")
        return

    # Crear ventana flotante
    ventana_rotar = tk.Toplevel(root)
    ventana_rotar.title("Rotar imagen")
    ventana_rotar.geometry("340x200")
    ventana_rotar.resizable(False, False)
    ventana_rotar.configure(bg="#f5f5f5")

    tk.Label(
        ventana_rotar,
        text="Ángulo de rotación (-180° a 180°):",
        bg="#f5f5f5",
        font=("Arial", 10)
    ).pack(pady=10)

    # Variable del ángulo
    angulo_valor = tk.DoubleVar(value=0.0)

    # Slider
    slider = tk.Scale(
        ventana_rotar,
        from_=-180,
        to=180,
        resolution=1,
        orient=tk.HORIZONTAL,
        length=260,
        variable=angulo_valor,
        bg="#f5f5f5"
    )
    slider.pack()

    # Guardar imagen original para restaurar si se cancela
    imagen_original = imagen_actual.copy()

    # Función para mostrar vista previa
    def vista_previa(valor):
        global imagen_actual
        valor = float(valor)

        # Convertir PIL a numpy
        img_np = np.array(imagen_original, dtype=np.float32)

        # Aplicar rotación usando tu función de Libimg
        try:
            img_modificada = Libimg.rotar(img_np, valor)
        except TypeError:
            # Si tu función no acepta el parámetro, muestra aviso
            print("⚠️ Ajusta la función li.rotar(img, angulo) para aceptar el ángulo de rotación.")
            return

        # Convertir de vuelta a PIL
        img_pil = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(img_pil)

    slider.config(command=vista_previa)

    # Función para confirmar la rotación
    def confirmar():
        global imagen_actual
        valor = angulo_valor.get()
        img_np = np.array(imagen_original, dtype=np.float32)
        img_modificada = Libimg.rotar(img_np, valor)
        imagen_actual = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_rotar.destroy()

    # Función para cancelar
    def cancelar():
        mostrar_imagen(imagen_original)
        ventana_rotar.destroy()

    # Botones
    frame_botones = tk.Frame(ventana_rotar, bg="#f5f5f5")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=5)

    #BRILLO POR CANAL RGB
    
def ajustar_rgb():
    """Ajusta individualmente los canales R, G y B usando li.ajuste_canal()."""
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de ajustar RGB.")
        return

    # Crear ventana flotante
    ventana_rgb = tk.Toplevel(root)
    ventana_rgb.title("Ajustar canales RGB")
    ventana_rgb.geometry("380x330")
    ventana_rgb.resizable(False, False)
    ventana_rgb.configure(bg="#f5f5f5")

    tk.Label(
        ventana_rgb,
        text="Ajuste individual de canales (-1 a 1):",
        bg="#f5f5f5",
        font=("Arial", 10, "bold")
    ).pack(pady=8)

    # Imagen original para restaurar si se cancela
    imagen_original = imagen_actual.copy()

    # Variables de los tres sliders
    r_valor = tk.DoubleVar(value=0.0)
    g_valor = tk.DoubleVar(value=0.0)
    b_valor = tk.DoubleVar(value=0.0)

    # Crear frame para sliders
    frame_sliders = tk.Frame(ventana_rgb, bg="#f5f5f5")
    frame_sliders.pack(pady=5)

    # Crear un slider con etiqueta dinámica
    def crear_slider(nombre, color, variable):
        frame = tk.Frame(frame_sliders, bg="#f5f5f5")
        frame.pack(pady=5)

        etiqueta = tk.Label(frame, text=f"{nombre}: 0.00", bg="#f5f5f5", fg=color, font=("Arial", 10))
        etiqueta.pack()

        slider = tk.Scale(
            frame,
            from_=-1,
            to=1,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=260,
            variable=variable,
            bg="#f5f5f5",
            highlightthickness=0
        )
        slider.pack()

        # Actualizar etiqueta en tiempo real
        def actualizar_etiqueta(*args):
            etiqueta.config(text=f"{nombre}: {variable.get():.2f}")

        variable.trace_add("write", actualizar_etiqueta)

    # Crear sliders RGB
    crear_slider("Rojo (R)", "red", r_valor)
    crear_slider("Verde (G)", "green", g_valor)
    crear_slider("Azul (B)", "blue", b_valor)

    # --- Vista previa ---
    def vista_previa(*args):
        global imagen_actual
        img_np = np.array(imagen_original, dtype=np.float32)

        # Aplicar ajuste canal por canal usando tu librería
        img_r = Libimg.ajuste_canal(img_np, 0, r_valor.get())
        img_g = Libimg.ajuste_canal(img_r, 1, g_valor.get())
        img_b = Libimg.ajuste_canal(img_g, 2, b_valor.get())

        img_pil = Image.fromarray(img_b.astype(np.uint8))
        mostrar_imagen(img_pil)

    # Asociar sliders a vista previa
    r_valor.trace_add("write", vista_previa)
    g_valor.trace_add("write", vista_previa)
    b_valor.trace_add("write", vista_previa)

    # --- Confirmar cambios ---
    def confirmar():
        global imagen_actual
        img_np = np.array(imagen_original, dtype=np.float32)
        img_r = Libimg.ajuste_canal(img_np, 0, r_valor.get())
        img_g = Libimg.ajuste_canal(img_r, 1, g_valor.get())
        img_b = Libimg.ajuste_canal(img_g, 2, b_valor.get())
        imagen_actual = Image.fromarray(img_b.astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_rgb.destroy()

    # --- Cancelar cambios ---
    def cancelar():
        mostrar_imagen(imagen_original)
        ventana_rgb.destroy()

    # Botones inferiores
    frame_botones = tk.Frame(ventana_rgb, bg="#f5f5f5")
    frame_botones.pack(pady=15)

    tk.Button(frame_botones, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=8)
    tk.Button(frame_botones, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=8)
    
    #CONTRASTE LOGARITMICO
def ajustar_contraste_log():
    """Ajusta el contraste logarítmico usando li.contrastelog() con vista previa y confirmación."""
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de ajustar el contraste.")
        return

    # Crear ventana
    ventana_contraste = tk.Toplevel(root)
    ventana_contraste.title("Contraste logarítmico")
    ventana_contraste.geometry("360x220")
    ventana_contraste.resizable(False, False)
    ventana_contraste.configure(bg="#f5f5f5")

    tk.Label(
        ventana_contraste,
        text="Ajustar contraste logarítmico",
        bg="#f5f5f5",
        font=("Arial", 10, "bold")
    ).pack(pady=8)

    tk.Label(
        ventana_contraste,
        text="Factor de contraste (0.1 - 5):",
        bg="#f5f5f5",
        font=("Arial", 10)
    ).pack()

    # Guardar imagen original para cancelar
    imagen_original = imagen_actual.copy()

    # Variable del valor del slider
    contraste_valor = tk.DoubleVar(value=1.0)

    # Crear slider
    slider = tk.Scale(
        ventana_contraste,
        from_=0.1,
        to=5.0,
        resolution=0.1,
        orient=tk.HORIZONTAL,
        length=260,
        variable=contraste_valor,
        bg="#f5f5f5",
        highlightthickness=0
    )
    slider.pack(pady=10)

    # Etiqueta para mostrar el valor actual
    etiqueta_valor = tk.Label(
        ventana_contraste,
        text=f"Valor actual: {contraste_valor.get():.1f}",
        bg="#f5f5f5",
        font=("Arial", 9)
    )
    etiqueta_valor.pack(pady=5)

    # Actualizar etiqueta cuando se mueve el slider
    def actualizar_etiqueta(*args):
        etiqueta_valor.config(text=f"Valor actual: {contraste_valor.get():.1f}")

    contraste_valor.trace_add("write", actualizar_etiqueta)

    # --- Vista previa ---
    def vista_previa(*args):
        global imagen_actual
        img_np = np.array(imagen_original, dtype=np.float32) / 255.0  # normalizar
        img_modificada = Libimg.contrastelog(img_np, contraste_valor.get())
        img_modificada = np.clip(img_modificada * 255, 0, 255)
        img_pil = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(img_pil)

    # Asociar el slider a la vista previa
    contraste_valor.trace_add("write", vista_previa)

    # --- Confirmar cambios ---
    def confirmar():
        global imagen_actual
        img_np = np.array(imagen_original, dtype=np.float32) / 255.0
        img_modificada = Libimg.contrastelog(img_np, contraste_valor.get())
        img_modificada = np.clip(img_modificada * 255, 0, 255)
        imagen_actual = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_contraste.destroy()

    # --- Cancelar cambios ---
    def cancelar():
        mostrar_imagen(imagen_original)
        ventana_contraste.destroy()

    # Botones
    frame_botones = tk.Frame(ventana_contraste, bg="#f5f5f5")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=8)
    tk.Button(frame_botones, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=8)

    #CONTRASTE EXPONENCIAL
def ajustar_contraste_exp():
    """Ajusta el contraste exponencial usando li.contraste() con vista previa y confirmación."""
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de ajustar el contraste.")
        return

    # Crear ventana
    ventana_contraste = tk.Toplevel(root)
    ventana_contraste.title("Contraste exponencial")
    ventana_contraste.geometry("360x220")
    ventana_contraste.resizable(False, False)
    ventana_contraste.configure(bg="#f5f5f5")

    tk.Label(
        ventana_contraste,
        text="Ajustar contraste exponencial",
        bg="#f5f5f5",
        font=("Arial", 10, "bold")
    ).pack(pady=8)

    tk.Label(
        ventana_contraste,
        text="Factor de contraste (0.1 - 5):",
        bg="#f5f5f5",
        font=("Arial", 10)
    ).pack()

    # Guardar imagen original
    imagen_original = imagen_actual.copy()

    # Variable del valor del slider
    contraste_valor = tk.DoubleVar(value=1.0)

    # Slider
    slider = tk.Scale(
        ventana_contraste,
        from_=0.1,
        to=5.0,
        resolution=0.1,
        orient=tk.HORIZONTAL,
        length=260,
        variable=contraste_valor,
        bg="#f5f5f5",
        highlightthickness=0
    )
    slider.pack(pady=10)

    # Etiqueta con valor actual
    etiqueta_valor = tk.Label(
        ventana_contraste,
        text=f"Valor actual: {contraste_valor.get():.1f}",
        bg="#f5f5f5",
        font=("Arial", 9)
    )
    etiqueta_valor.pack(pady=5)

    def actualizar_etiqueta(*args):
        etiqueta_valor.config(text=f"Valor actual: {contraste_valor.get():.1f}")

    contraste_valor.trace_add("write", actualizar_etiqueta)

    # --- Vista previa ---
    def vista_previa(*args):
        global imagen_actual
        img_np = np.array(imagen_original, dtype=np.float32) / 255.0  # normalizar
        img_modificada = Libimg.contraste(img_np, contraste_valor.get())
        img_modificada = np.clip(img_modificada * 255, 0, 255)
        img_pil = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(img_pil)

    contraste_valor.trace_add("write", vista_previa)

    # --- Confirmar ---
    def confirmar():
        global imagen_actual
        img_np = np.array(imagen_original, dtype=np.float32) / 255.0
        img_modificada = Libimg.contraste(img_np, contraste_valor.get())
        img_modificada = np.clip(img_modificada * 255, 0, 255)
        imagen_actual = Image.fromarray(img_modificada.astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_contraste.destroy()

    # --- Cancelar ---
    def cancelar():
        mostrar_imagen(imagen_original)
        ventana_contraste.destroy()

    # Botones
    frame_botones = tk.Frame(ventana_contraste, bg="#f5f5f5")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=8)
    tk.Button(frame_botones, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=8)

    #FUNCION EXTRAER RGB
def extraer_capas_rgb():
    """Extrae canales RGB usando Libimg.ajuste_canal(img, canal, brillo) con checkboxes (0 o -1)."""
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de extraer capas.")
        return

    # Ventana
    ventana_rgb = tk.Toplevel(root)
    ventana_rgb.title("Extracción de capas RGB")
    ventana_rgb.geometry("320x260")
    ventana_rgb.resizable(False, False)
    ventana_rgb.configure(bg="#f5f5f5")

    tk.Label(ventana_rgb, text="Selecciona los canales a conservar:",
             bg="#f5f5f5", font=("Arial", 10, "bold")).pack(pady=8)

    # Imagen original (PIL) y su copia en numpy (sin normalizar aquí)
    imagen_original = imagen_actual.copy()
    img_np_orig = np.array(imagen_original, dtype=np.float32)  # valores 0-255

    # Checkbuttons (inician marcados = conservar)
    var_r = tk.BooleanVar(value=True)
    var_g = tk.BooleanVar(value=True)
    var_b = tk.BooleanVar(value=True)

    frame_checks = tk.Frame(ventana_rgb, bg="#f5f5f5")
    frame_checks.pack(pady=6)
    tk.Checkbutton(frame_checks, text="Rojo (R)", variable=var_r, bg="#f5f5f5").pack(anchor="w")
    tk.Checkbutton(frame_checks, text="Verde (G)", variable=var_g, bg="#f5f5f5").pack(anchor="w")
    tk.Checkbutton(frame_checks, text="Azul (B)", variable=var_b, bg="#f5f5f5").pack(anchor="w")

    # Función que aplica ajuste por canal usando Libimg.ajuste_canal
    def aplicar_ajustes(img_np):
        """
        img_np: numpy array 0-255 (float or uint8). devuelve numpy array 0-255.
        """
        # Empezamos con la imagen original cada vez para evitar acumulación de errores
        img_temp = img_np.copy()

        # Para cada canal llamamos a la función con brillo 0 (conservar) o -1 (apagar)
        # IMPORTANTE: Libimg.ajuste_canal espera img, canal, brillo
        brillo_r = 0.0 if var_r.get() else -1.0
        brillo_g = 0.0 if var_g.get() else -1.0
        brillo_b = 0.0 if var_b.get() else -1.0

        # llamar por canal — la función devuelve la imagen completa en rango 0-255
        img_temp = Libimg.ajuste_canal(img_temp, 0, brillo_r)
        img_temp = Libimg.ajuste_canal(img_temp, 1, brillo_g)
        img_temp = Libimg.ajuste_canal(img_temp, 2, brillo_b)

        return img_temp

    # Vista previa (convierte a PIL y muestra)
    def vista_previa(*_):
        img_mod_np = aplicar_ajustes(img_np_orig)
        # ajuste_canal devuelve valores en 0-255 (según tu función), convierto a uint8
        img_pil = Image.fromarray(np.clip(img_mod_np, 0, 255).astype(np.uint8))
        mostrar_imagen(img_pil)

    # Asociar cambios
    var_r.trace_add("write", vista_previa)
    var_g.trace_add("write", vista_previa)
    var_b.trace_add("write", vista_previa)

    # Confirmar: aplicar definitivamente a imagen_actual
    def confirmar():
        global imagen_actual
        img_mod_np = aplicar_ajustes(img_np_orig)
        imagen_actual = Image.fromarray(np.clip(img_mod_np, 0, 255).astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_rgb.destroy()
        messagebox.showinfo("Listo", "Capas RGB actualizadas correctamente.")

    # Cancelar: restaurar original
    def cancelar():
        mostrar_imagen(imagen_original)
        ventana_rgb.destroy()

    # Botones
    frame_bot = tk.Frame(ventana_rgb, bg="#f5f5f5")
    frame_bot.pack(pady=12)
    tk.Button(frame_bot, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=6)
    tk.Button(frame_bot, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=6)

    # Mostrar vista inicial
    vista_previa()

def histograma():
    # Muestra el histograma de la imagen actual.
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de mostrar el histograma.")
        return
    # Crear ventana
    ventana_hist = tk.Toplevel(root)
    ventana_hist.title("Histograma de la imagen")
    ventana_hist.geometry("600x500")
    ventana_hist.resizable(False, False)
    ventana_hist.configure(bg="#f5f5f5")
    img_np = np.array(imagen_actual, dtype=np.float32) / 255.0  # Normalizar a 0-1
    # Obtener histogramas por canal
    h_r=Libimg.historiagrama(img_np, 0)
    h_g=Libimg.historiagrama(img_np, 1)
    h_b=Libimg.historiagrama(img_np, 2)
    # Crear figura con subplots
    fig, axs = plt.subplots(2, 2, figsize=(6, 5))
    axs[0, 0].plot(h_r, color='red')
    axs[0, 0].set_title('Histograma Rojo')
    axs[0, 1].plot(h_g, color='green')
    axs[0, 1].set_title('Histograma Verde')
    axs[1, 0].plot(h_b, color='blue')
    axs[1, 0].set_title('Histograma Azul')
    axs[1, 1].axis('off')  # Cuadro vacío
    plt.tight_layout()
    # Integrar figura en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_hist)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)  # Cerrar figura para liberar memoria
def negativa():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showinfo("Atención", "Primero abre una imagen antes de aplicar negativa.")
        return
    ventana_neg = tk.Toplevel(root)
    ventana_neg.title("Negativa de la imagen")
    ventana_neg.geometry("300x100")
    ventana_neg.resizable(False, False)
    ventana_neg.configure(bg="#f5f5f5")
    tk.Label(
        ventana_neg,
        text="Aplicar negativa a la imagen actual?",
        bg="#f5f5f5",
        font=("Arial", 10)
    ).pack(pady=10)
    def vista_previa():
        global imagen_actual
        img_np = np.array(imagen_actual, dtype=np.float32)
        img_modificada = Libimg.Resta(img_np)
        img_pil = Image.fromarray(np.clip(img_modificada, 0, 255).astype(np.uint8))
        mostrar_imagen(img_pil)
    def confirmar():
        global imagen_actual
        img_np = np.array(imagen_actual, dtype=np.float32)
        img_modificada = Libimg.Resta(img_np)
        imagen_actual = Image.fromarray(np.clip(img_modificada, 0, 255).astype(np.uint8))
        mostrar_imagen(imagen_actual)
        ventana_neg.destroy()
    def cancelar():
        mostrar_imagen(imagen_actual)
        ventana_neg.destroy()

    # Botones de confirmación
    frame_bot = tk.Frame(ventana_neg, bg="#f5f5f5")
    frame_bot.pack(pady=12)
    tk.Button(frame_bot, text="Confirmar", width=10, command=confirmar).pack(side="left", padx=6)
    tk.Button(frame_bot, text="Cancelar", width=10, command=cancelar).pack(side="left", padx=6)

    # Mostrar vista inicial
    vista_previa()


# ----------- INTERFAZ PRINCIPAL -----------

root = tk.Tk()
root.title("Procesador de imágenes")
root.geometry("600x450")
root.configure(bg="#f5f5f5")

# Botones principales
btn_archivo = tk.Button(root, text="Archivo ▼", command=menu_archivo)
btn_archivo.place(x=10, y=10)

btn_editar = tk.Button(root, text="Editar ▼", command=menu_editar)
btn_editar.place(x=90, y=10)

btn_salir = tk.Button(root, text="Salir", command=root.quit)
btn_salir.place(x=540, y=10)

# Label donde se muestra la imagen
lbl = tk.Label(root, bg="white", relief="sunken", width=400, height=300)
lbl.place(x=100, y=60)

root.mainloop()
