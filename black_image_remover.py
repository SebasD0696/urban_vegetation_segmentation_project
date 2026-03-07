import os
import numpy as np
from PIL import Image

carpeta = r"C:\Users\Usuario\Downloads\Segmentacion_Project\Floridablanca_completo"

for archivo in os.listdir(carpeta):

    if archivo.lower().endswith((".tif", ".tiff")):
        ruta = os.path.join(carpeta, archivo)

        img = Image.open(ruta)
        arr = np.array(img)

        # Si tiene canal alpha (4 canales)
        if arr.ndim == 3 and arr.shape[2] == 4:
            arr = arr[:, :, :3]  # solo RGB

        # verificar si RGB es completamente negro
        if np.all(arr == 0):
            os.remove(ruta)
            print(f"Eliminada: {archivo}")
        else:
            print(f"Tiene datos: {archivo}")