# 🖼️ Procesador de Imágenes con Tkinter y Libimg

## 📌 Descripción General
Este proyecto implementa un **procesador de imágenes interactivo en Python**, desarrollado con **Tkinter** como interfaz gráfica y una librería personalizada llamada **`Libimg`**, la cual contiene diversas funciones de procesamiento digital de imágenes (PDI).

La aplicación permite **abrir, visualizar, editar y guardar imágenes** mediante un conjunto de herramientas visuales y controles dinámicos (sliders, checkboxes y selecciones de área).

---

## ⚙️ Tecnologías Utilizadas

- **Python 3.10+**
- **Tkinter** — interfaz gráfica
- **PIL (Pillow)** — manejo y conversión de imágenes
- **Matplotlib** — visualización de histogramas
- **NumPy** — cálculos matriciales y operaciones de pixelado
- **Librería personalizada `Libimg`** — funciones matemáticas y geométricas para el procesamiento de imágenes

---

## 🚀 Funcionalidades Principales

### 🗂️ Menú Archivo
- **Abrir imagen:** permite cargar archivos `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.tiff`.  
- **Guardar imagen:** exporta el resultado en múltiples formatos.  

 <img src="imagenesreadme\opcionesarchivo.png" width="500">
---

### 🎨 Menú Editar
Incluye una amplia variedad de herramientas visuales:

<img src="imagenesreadme\opcioneseditar.png" width="500">

#### 💡 Ajustes de Color y Brillo
- **Brillo global:** control mediante barra deslizante (-1 a 1).

<img src="imagenesreadme\brillo.png" width="500">

- **Ajuste RGB:** control independiente por canal con sliders. 

<img src="imagenesreadme\ajusteRGB.png" width="500">

- **Extracción RGB:** permite apagar canales (R, G o B) con checkboxes.

<img src="imagenesreadme\extraccionRGB.png" width="500">

- **Extracción CMYK:** conversión a CMYK con opción de activar/desactivar canales.  

<img src="imagenesreadme\extraccionCYMK.png" width="500">

#### 🌓 Contraste
- **Contraste logarítmico:** mejora áreas oscuras.

<img src="imagenesreadme\contrasteLOG.png" width="500">

- **Contraste exponencial:** resalta zonas brillantes.  

<img src="imagenesreadme\contrasteEXP.png" width="500">

#### 🔄 Transformaciones Geométricas
- **Rotar imagen:** ángulo entre -180° y 180°.  

<img src="imagenesreadme\rotar.png" width="500">

- **Recortar:** selección de área con el mouse directamente sobre la imagen.

<img src="imagenesreadme\recortar.png" width="500">

- **Zoom:** ampliación por área seleccionada y factor configurable.

<img src="imagenesreadme\zoom.png" width="500">

#### ⚫ Escala y Filtros
- **Escala de grises:** por promedio, luminancia o tonalidad.  

<img src="imagenesreadme\escalagrises.png" width="500">

- **Negativo:** inversión de los valores de color.

<img src="imagenesreadme\negativa.png" width="500">

- **Binarización:** umbral ajustable entre 0.0 y 1.0.

<img src="imagenesreadme\binarizar.png" width="500">

- **Histograma:** muestra gráficos por canal (R, G, B).  

<img src="imagenesreadme\histograma.png" width="500">

#### 🔀 Operaciones entre imágenes
- **Fusión:** mezcla dos imágenes del mismo tamaño.

<img src="imagenesreadme\fusionarimg.png" width="500">

- **Fusión ecualizada:** combina imágenes con un peso ajustable (slider).  

<img src="imagenesreadme\ecualizarimg.png" width="500">
---

## 📘 Librería `Libimg`

La librería complementaria **`Libimg.py`** incluye todas las funciones de procesamiento matemático, como:

| Función | Descripción |
|----------|--------------|
| `brillo(img, valor)` | Modifica la luminosidad de una imagen |
| `ajuste_canal(img, canal, brillo)` | Ajusta brillo por canal RGB |
| `rotar(img, angulo)` | Rota la imagen según grados dados |
| `contrastelog(img, factor)` | Aumenta contraste mediante escala logarítmica |
| `contraste(img, factor)` | Ajusta contraste exponencial |
| `grises`, `luminocidad`, `tonalidad` | Convierte a diferentes modos de escala de grises |
| `binarizar(img, umbral)` | Convierte la imagen en binaria según umbral |
| `Suma`, `Suma_ponderada` | Funde dos imágenes |
| `Resta` | Aplica negativo |
| `historiagrama(img, canal)` | Calcula histograma de un canal específico |
| `recortar(img, x1, y1, x2, y2)` | Recorta una región definida por coordenadas |
| `ampliacion_area(img, factor, x1, y1, x2, y2)` | Realiza zoom por región |
| `separar_cmyk(img, c, m, y, k)` | Convierte RGB a CMYK y permite apagar canales |

---

## 🖥️ Interfaz Gráfica

- Botones principales:
  - `Archivo ▼`
  - `Editar ▼`
  - `Salir`
- La imagen se muestra dentro de un `Label` dinámico (`lbl`).
- Submenús desplegables automáticos (desaparecen al perder el foco).
- Ventanas emergentes (`Toplevel`) para cada transformación.
- Controles interactivos: **sliders**, **checkboxes**, **canvas** de selección.

---

## 🧩 Estructura del Proyecto

```bash
📂 Proyecto_Procesador_Imagenes/
├── Clase8.py          # Interfaz principal (Tkinter)
├── Libimg.py          # Librería personalizada de procesamiento
├── README.md          # (este archivo)
├── 📂 Imagenes de prueba/  # Carpeta opcional para pruebas
└── 📂 Imagenesreadme/ # Carpeta de imagenes para el readme