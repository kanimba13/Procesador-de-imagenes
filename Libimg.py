import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def layer(img,capa):
    img_capa=np.zeros_like(img)
    match capa:
        case 'r':
            img_capa[:,:,0]=img[:,:,0]
        case 'g':
            img_capa[:,:,1]=img[:,:,1]
        case 'b':
            img_capa[:,:,2]=img[:,:,2]
        case 'y':
            img_capa[:, :, 0] = img[:, :, 0]
            img_capa[:, :, 1] = img[:, :, 1] 
        case 'c':
            img_capa[:, :, 1] = img[:, :, 1]
            img_capa[:, :, 2] = img[:, :, 2]
        case 'm':
            img_capa[:, :, 0] = img[:, :, 0]
            img_capa[:, :, 2] = img[:, :, 2]
        case default:
            print("Opcion no valida")
            return img
    return img_capa

def layer_prog(img, r, g, b):
    img_np = np.array(img, dtype=np.float32)
    combined = np.zeros_like(img_np)
    if img_np.ndim == 3 and img_np.shape[2] >= 3:
        if r:
            combined[:, :, 0] = img_np[:, :, 0]
        if g:
            combined[:, :, 1] = img_np[:, :, 1]
        if b:
            combined[:, :, 2] = img_np[:, :, 2]
    return combined

def Resta(img):
    imgN=255-img
    return imgN

def Suma(img1,img2):
    if img1.max()>1:
        img1=img1/255
    if img2.max()>1:
        img2=img2/255
    imgF=(img1+img2)/2
    return imgF.astype(np.float32)

def Suma_ponderada(img1,img2,factor):
    if img1.max()>1:
        img1=img1/255
    if img2.max()>1:
        img2=img2/255
    imgF=img1*factor+img2*(1-factor)
    return imgF.astype(np.float32)

def grises(img):
    imgG=(img[:,:,0]+img[:,:,1]+img[:,:,2])/3
    return imgG

def luminocidad(img):
    imgL=0.299*img[:,:,0]+0.587*img[:,:,1]+0.114*img[:,:,2]
    return imgL

def tonalidad(img):
    imgT=(np.maximum(img[:,:,0], img[:,:,1], img[:,:,2])+np.minimum(img[:,:,0], img[:,:,1], img[:,:,2]))/2
    return imgT

def comparacion_grises(img):
    img=img/255
    imgG=(img[:,:,0]+img[:,:,1]+img[:,:,2])/3
    imgL=0.299*img[:,:,0]+0.587*img[:,:,1]+0.114*img[:,:,2]
    imgT=(np.maximum(img[:,:,0], img[:,:,1], img[:,:,2])+np.minimum(img[:,:,0], img[:,:,1], img[:,:,2]))/2
    plt.subplot(2,3,2)
    plt.imshow(img)
    plt.axis('off')
    plt.title('Original')
    plt.subplot(2,3,4)
    plt.imshow(imgG, cmap='gray')
    plt.axis('off')
    plt.title('Grises')
    plt.subplot(2,3,5)
    plt.imshow(imgL, cmap='gray')
    plt.axis('off')
    plt.title('Luminocidad')
    plt.subplot(2,3,6)
    plt.imshow(imgT, cmap='gray')
    plt.axis('off')
    plt.title('Tonalidad')
    plt.show()
    
def brillo(img, brillo):
    img_brillo=np.copy(img)/255
    img_brillo=img_brillo+brillo
    img_brillo=np.clip(img_brillo, 0, 1)
    img_brillo=img_brillo*255
    return img_brillo

def ajuste_canal(img, canal,brillo):
    img=img/255
    img_canal=img.copy()
    img_canal[:,:,canal]=np.clip(img_canal[:,:,canal]+brillo, 0, 1)
    return img_canal*255

def contraste(img, contraste):
    img_contraste=np.clip(contraste*(np.exp(img-1)), 0, 1)
    return img_contraste

def contrastelog(img, contraste):
    img_contraste=np.clip(contraste*np.log10(1+img), 0, 1)
    return img_contraste

def binarizar(img, umbral):
    if img.max()>1:
        img=img/255.0
    gris=(img[:,:,0]+img[:,:,1]+img[:,:,2])/3.0
    imgBin=gris>umbral
    return imgBin.astype(np.float32)

def trasladar(img, dx, dy):
    img=img/255
    trasladada=np.zeros_like(img)
    h, w=img.shape[:2]
    x_origen_inicio=0
    x_origen_fin=w-dx
    y_origen_inicio=0
    y_origen_fin=h-dy

    trasladada[dy:h, dx:w]=img[y_origen_inicio:y_origen_fin, x_origen_inicio:x_origen_fin]
    return trasladada

def recortar(img, x1, y1, x2, y2):
    if img.max() > 1:
        img = img / 255.0
    y1, y2 = max(0, int(y1)), min(img.shape[0], int(y2))
    x1, x2 = max(0, int(x1)), min(img.shape[1], int(x2))
    img_recortada = img[y1:y2, x1:x2]
    return img_recortada
    
def rotar(img, angulo):
    """Rota una imagen en grados positivos o negativos."""
    ang = np.radians(angulo)
    h, w = img.shape[:2]
    cos_ang = np.cos(ang)
    sin_ang = np.sin(ang)

    c = int(abs(h * cos_ang) + abs(w * sin_ang))
    d = int(abs(h * sin_ang) + abs(w * cos_ang))

    b = np.zeros((c, d, img.shape[2]), dtype=img.dtype) if img.ndim == 3 else np.zeros((c, d), dtype=img.dtype)

    # Centro de la imagen
    cx, cy = w // 2, h // 2
    nx, ny = d // 2, c // 2

    for i in range(c):
        for j in range(d):
            x = (j - nx)
            y = (i - ny)
            xx = int(cos_ang * x + sin_ang * y + cx)
            yy = int(-sin_ang * x + cos_ang * y + cy)
            if 0 <= yy < h and 0 <= xx < w:
                b[i, j] = img[yy, xx]

    return b

    
def resolucion(img, zoom_factor):
    img_baja=img[::zoom_factor, ::zoom_factor]
    return img_baja

def ampliacion_area(img, zoom_factor, x1, y1, x2, y2):
    # Normalizar si está en rango 0-255
    if img.max() > 1:
        img = img / 255.0

    # Asegurar límites válidos
    h, w = img.shape[:2]
    x1, x2 = max(0, int(x1)), min(w, int(x2))
    y1, y2 = max(0, int(y1)), min(h, int(y2))

    # Recortar el área seleccionada
    recorte = img[y1:y2, x1:x2]
    if recorte.size == 0:
        raise ValueError("Área seleccionada vacía o fuera de los límites de la imagen.")

    # Ampliar usando Kronecker (zoom sin interpolación)
    zoom_factor = max(1, int(zoom_factor))
    if recorte.ndim == 2:
        recorte = np.expand_dims(recorte, axis=-1)
    zoomed = np.kron(recorte, np.ones((zoom_factor, zoom_factor, 1)))

    # Escalar de nuevo a 0-255
    zoomed = np.clip(zoomed * 255, 0, 255).astype(np.uint8)
    zoomed=resolucion(zoomed, zoom_factor//2) if zoom_factor>2 else zoomed
    if zoomed.shape[2] == 1:
        zoomed = zoomed.squeeze(-1)
    return zoomed
    
def historiagrama(img, tipo):
    if img.max()<=1:
        img=(img*255).astype(np.uint8)
    r=img[:,:,0]
    g=img[:,:,1]
    b=img[:,:,2]
    match tipo:
        case 0:
            h_r,_=np.histogram(r, bins=256, range=(0,255))
            return h_r
        case 1:
            h_g,_=np.histogram(g, bins=256, range=(0,255))
            return h_g
        case 2:
            h_b,_=np.histogram(b, bins=256, range=(0,255))
            return h_b
        case _:
            return img