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

---

### 🎨 Menú Editar
Incluye una amplia variedad de herramientas visuales:

#### 💡 Ajustes de Color y Brillo
- **Brillo global:** control mediante barra deslizante (-1 a 1).
- **Ajuste RGB:** control independiente por canal con sliders.  
- **Extracción RGB:** permite apagar canales (R, G o B) con checkboxes.  
- **Extracción CMYK:** conversión a CMYK con opción de activar/desactivar canales.  

#### 🌓 Contraste
- **Contraste logarítmico:** mejora áreas oscuras.  
- **Contraste exponencial:** resalta zonas brillantes.  

#### 🔄 Transformaciones Geométricas
- **Rotar imagen:** ángulo entre -180° y 180°.  
- **Recortar:** selección de área con el mouse directamente sobre la imagen.  
- **Zoom:** ampliación por área seleccionada y factor configurable.  

#### ⚫ Escala y Filtros
- **Escala de grises:** por promedio, luminancia o tonalidad.  
- **Negativo:** inversión de los valores de color.  
- **Binarización:** umbral ajustable entre 0.0 y 1.0.  
- **Histograma:** muestra gráficos por canal (R, G, B).  

#### 🔀 Operaciones entre imágenes
- **Fusión:** mezcla dos imágenes del mismo tamaño.  
- **Fusión ecualizada:** combina imágenes con un peso ajustable (slider).  

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
└── /imagenes/         # Carpeta opcional para pruebas
