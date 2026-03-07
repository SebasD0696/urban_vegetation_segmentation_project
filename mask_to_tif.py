import glob
import os
import rasterio
from rasterio.merge import merge

# -----------------------------
# 1️⃣ Carpeta con las máscaras
# -----------------------------
masks_dir = r"C:\Users\Usuario\Downloads\Segmentacion_Project\Floridablanca\Floridablanca_Mask"

# -----------------------------
# 2️⃣ Buscar todos los GeoTIFF
# -----------------------------
mask_files = glob.glob(os.path.join(masks_dir, "*.tif"))

print("Máscaras encontradas:", len(mask_files))

# -----------------------------
# 3️⃣ Abrir rasters
# -----------------------------
src_files = [rasterio.open(f) for f in mask_files]

# -----------------------------
# 4️⃣ Crear mosaico
# -----------------------------
mosaic, transform = merge(src_files)

# -----------------------------
# 5️⃣ Copiar metadata
# -----------------------------
meta = src_files[0].meta.copy()

meta.update({
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": transform
})

# -----------------------------
# 6️⃣ Guardar resultado
# -----------------------------
output_path = r"C:\Users\Usuario\Downloads\Segmentacion_Project\Floridablanca\segmentacion_final.tif"

with rasterio.open(output_path, "w", **meta) as dest:
    dest.write(mosaic)

print("Mapa reconstruido:", output_path)