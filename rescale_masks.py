# rescale_masks.py
import os
import cv2

# Carpeta de máscaras originales
mask_dir = "mask_seleccionadas/0.1m"
out_dir = "mask_seleccionadas"

# Crear carpetas de salida para todas las máscaras
out_dir_0_2m = os.path.join(out_dir, "0.2m")
out_dir_0_4m = os.path.join(out_dir, "0.4m")
os.makedirs(out_dir_0_2m, exist_ok=True)
os.makedirs(out_dir_0_4m, exist_ok=True)

# Función para reescalar usando nearest neighbor
def rescale_mask(mask_path, scale_factor):
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    if mask is None:
        print(f"⚠️ No se pudo leer {mask_path}")
        return None
    new_size = (mask.shape[1] // scale_factor, mask.shape[0] // scale_factor)
    mask_rescaled = cv2.resize(mask, new_size, interpolation=cv2.INTER_NEAREST)
    return mask_rescaled

# Procesar todas las máscaras de la carpeta
masks = sorted(os.listdir(mask_dir))
for mask_name in masks:
    if not mask_name.lower().endswith((".png", ".jpg", ".tif", ".jpeg")):
        continue  # saltar archivos que no sean imágenes

    mask_path = os.path.join(mask_dir, mask_name)

    # Reescalar a 0.2 m (factor 2)
    mask_0_2m = rescale_mask(mask_path, 2)
    if mask_0_2m is not None:
        cv2.imwrite(os.path.join(out_dir_0_2m, mask_name), mask_0_2m)

    # Reescalar a 0.4 m (factor 4)
    mask_0_4m = rescale_mask(mask_path, 4)
    if mask_0_4m is not None:
        cv2.imwrite(os.path.join(out_dir_0_4m, mask_name), mask_0_4m)

print("Todas las máscaras han sido reescaladas a 0.2m y 0.4m.")