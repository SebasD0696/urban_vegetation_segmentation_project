# rescale_images_rgb.py
import os
import cv2

# Carpeta de imágenes originales
img_dir = "images_seleccionadas/0.1m"
out_dir = "images_seleccionadas"

# Crear carpetas de salida para todas las imágenes
out_dir_0_2m = os.path.join(out_dir, "0.2m")
out_dir_0_4m = os.path.join(out_dir, "0.4m")
os.makedirs(out_dir_0_2m, exist_ok=True)
os.makedirs(out_dir_0_4m, exist_ok=True)

# Función para reescalar
def rescale_image(img_path, scale_factor):
    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ No se pudo leer {img_path}")
        return None
    new_size = (img.shape[1] // scale_factor, img.shape[0] // scale_factor)
    img_rescaled = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    return img_rescaled

# Procesar todas las imágenes de la carpeta
images = sorted(os.listdir(img_dir))
for img_name in images:
    if not img_name.lower().endswith((".png", ".jpg", ".tif", ".jpeg")):
        continue  # saltar archivos que no sean imágenes
    
    img_path = os.path.join(img_dir, img_name)
    
    # Reescalar a 0.2 m (factor 2)
    img_0_2m = rescale_image(img_path, 2)
    if img_0_2m is not None:
        cv2.imwrite(os.path.join(out_dir_0_2m, img_name), img_0_2m)
    
    # Reescalar a 0.4 m (factor 4)
    img_0_4m = rescale_image(img_path, 4)
    if img_0_4m is not None:
        cv2.imwrite(os.path.join(out_dir_0_4m, img_name), img_0_4m)

print("Todas las imágenes RGB han sido reescaladas a 0.2m y 0.4m.")