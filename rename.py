import os
import shutil

# ---------------------------
# Configura estas variables
city_name = "florencia"          # <- Aquí pones el nombre de la ciudad
images_folder = "pruebas_rgb"      # carpeta donde están las imágenes originales
masks_folder = "pruebas_mask"        # carpeta donde están las máscaras originales
output_images = "images_seleccionadas/0.1m"  # carpeta de salida para imágenes renombradas
output_masks = "mask_seleccionadas/0.1m"    # carpeta de salida para máscaras renombradas
# ---------------------------

# Crear carpetas de salida si no existen
os.makedirs(output_images, exist_ok=True)
os.makedirs(output_masks, exist_ok=True)

# Función para renombrar y copiar imágenes
def rename_and_copy_images(folder, output_folder, city):
    for filename in os.listdir(folder):
        if filename.endswith(".tif"):
            new_name = f"{city}_{filename}"
            src_path = os.path.join(folder, filename)
            dst_path = os.path.join(output_folder, new_name)
            shutil.copy(src_path, dst_path)
            print(f"{filename} -> {new_name}")

# Función para renombrar y copiar máscaras
def rename_and_copy_masks(folder, output_folder, city):
    for filename in os.listdir(folder):
        if filename.endswith(".tif"):
            # Eliminar "_mask" del nombre
            new_name = filename.replace("_mask", "")
            new_name = f"{city}_{new_name}"
            src_path = os.path.join(folder, filename)
            dst_path = os.path.join(output_folder, new_name)
            shutil.copy(src_path, dst_path)
            print(f"{filename} -> {new_name}")

# Renombrar imágenes
rename_and_copy_images(images_folder, output_images, city_name)

# Renombrar máscaras
rename_and_copy_masks(masks_folder, output_masks, city_name)

print("¡Renombrado completado!")