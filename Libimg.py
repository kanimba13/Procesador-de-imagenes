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
    imgN=1-img
    return imgN
def Suma(img1,img2):
    if img1.size!=img2.size:
        img2=img2.resize(img1.size)
        img2=np.array(img2)/255
        img1=np.array(img1)/255
    else:
        img1=np.array(img1)/255
        img2=np.array(img2)/255
    imgF=(img1+img2)/2
    return imgF
def Suma_ponderada(img1,img2,factor):
    if img1.size!=img2.size:
        img2=img2.resize(img1.size)
        img2=np.array(img2)/255
        img1=np.array(img1)/255
    else:
        img1=np.array(img1)/255
        img2=np.array(img2)/255
    imgF=img1*factor+img2*(1-factor)
    return imgF
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
    gris=(img[:,:,0]+img[:,:,1]+img[:,:,2])/3
    imgBin=gris>umbral
    return imgBin
def trasladar():
    img=plt.imread('img1.jpg')/255
    plt.figure("TRASLACION sin np.roll")
    plt.subplot(1,2,1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1,2,2)
    plt.title("Trasladada")
    trasladada=np.zeros_like(img)
    dx, dy=100, 50
    h, w=img.shape[:2]
    x_origen_inicio=0
    x_origen_fin=w-dx
    y_origen_inicio=0
    y_origen_fin=h-dy

    trasladada[dy:h, dx:w]=img[y_origen_inicio:y_origen_fin, x_origen_inicio:x_origen_fin]
    plt.imshow(trasladada)
    plt.axis("off")
    plt.show()
def recortar():
    img=plt.imread('img1.jpg')/255
    plt.figure("RECORTE")
    plt.subplot(1,2,1)
    plt.title("Original\nTamaño original: "+str(img.shape))
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1,2,2)
    xi, xf=50,200
    yi, yf=100,300
    img_recortada=img[yi:yf, xi:xf]
    plt.title("Recortada\nTamaño recortada: "+str(img_recortada.shape))
    plt.imshow(img_recortada)
    plt.axis("off")
    plt.show()
def rotar():
    img = plt.imread('img1.jpg')
    angulo = 45
    ang = np.radians(angulo)
    h, w = img.shape[:2]
    cos_ang = np.cos(ang)
    sin_ang = np.sin(ang)
    if ang > 0 and ang <= np.pi / 2:
        c = int(round(h * sin_ang + w * cos_ang)) + 1
        d = int(round(h * cos_ang + w * sin_ang)) + 1
        b = np.zeros((c, d, img.shape[2]), dtype=img.dtype) if img.ndim == 3 else np.zeros((c, d), dtype=img.dtype)

        for i in range(c):
            for j in range(d):
                iii = i - int(w * sin_ang) - 1
                ii = int(round(j * sin_ang + iii * cos_ang))
                jj = int(round(j * cos_ang - iii * sin_ang))
                if 0 <= ii < h and 0 <= jj < w:
                    b[i, j] = img[ii, jj]
    elif ang > np.pi / 2 and ang <= np.pi:
        c = int(round(h * sin_ang + w * cos_ang)) + 1
        d = int(round(h * sin_ang + w * cos_ang)) + 1
        e = -w * cos_ang
        b = np.zeros((c, d, img.shape[2]), dtype=img.dtype) if img.ndim == 3 else np.zeros((c, d), dtype=img.dtype)
        for i in range(c):
            iii = c - i - 1
            for j in range(d):
                jjj = d - j - 1
                ii = int(round(jjj * sin_ang + iii * cos_ang))
                jj = int(round(jjj * cos_ang - iii * sin_ang - e))
                if 0 <= ii < h and 0 <= jj < w:
                    b[i, j] = img[ii, jj]
    else:
        raise ValueError("El ángulo debe estar entre 0 y 180 grados")
    plt.figure("ROTACION")
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.title("Rotada " + str(angulo) + " grados")
    plt.imshow(b)
    plt.axis("off")
    plt.show()
def resolucion(img, zoom_factor):
    img_baja=img[::zoom_factor, ::zoom_factor]
    return img_baja
def ampliacion_area():
    img=plt.imread('img1.jpg')/255
    zoom_area=100
    h,w=img.shape[:2]
    star_row=h//2-zoom_area//2
    end_row=h//2+zoom_area//2
    star_col=w//2-zoom_area//2
    end_col=w//2+zoom_area//2

    recorte=img[star_row:end_row, star_col:end_col]
    zoom_factor=5
    zoomed=np.kron(recorte, np.ones((zoom_factor, zoom_factor, 1)))

    plt.figure("AMPLIACION DE AREA")
    plt.subplot(1,2,1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")
    plt.subplot(1,2,2)
    plt.title("Ampliada")
    plt.imshow(zoomed)
    plt.axis("off")
    plt.show()
def historiagrama(img, tipo):
    if img.max()<=1:
        img=(img*255).astype(np.uint8)
    r=img[:,:,0]
    g=img[:,:,1]
    b=img[:,:,2]
    match tipo:
        case 0:
            h_r=plt.hist(r.ravel(), bins=256, color='red', alpha=0.7)
            return h_r
        case 1:
            h_g=plt.hist(g.ravel(), bins=256, color='green', alpha=0.7)
            return h_g
        case 2:
            h_b=plt.hist(b.ravel(), bins=256, color='blue', alpha=0.7)
            return h_b
        case _:
            return img