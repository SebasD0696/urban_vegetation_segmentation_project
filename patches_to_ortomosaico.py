import os
import glob
import rasterio
from rasterio.merge import merge


# ============================================================
# CONFIGURACIÓN
# ============================================================

INPUT_DIR = r"C:\Users\Usuario\Downloads\municipios\tumaco\tiles"                 # Carpeta con los .tif/.tiff
OUTPUT_FILE = r"C:\Users\Usuario\Downloads\municipios\tumaco\ortomosaico.tif"     # Archivo de salida


# ============================================================
# BUSCAR IMÁGENES
# ============================================================

tiff_files = sorted(
    glob.glob(os.path.join(INPUT_DIR, "*.tif")) +
    glob.glob(os.path.join(INPUT_DIR, "*.tiff"))
)

if not tiff_files:
    raise FileNotFoundError(
        f"No se encontraron archivos TIFF en: {INPUT_DIR}"
    )

print(f"Se encontraron {len(tiff_files)} imágenes.")


# ============================================================
# ABRIR RASTERS
# ============================================================

src_files = []

for file in tiff_files:
    print(f"Abriendo: {os.path.basename(file)}")

    src = rasterio.open(file)
    src_files.append(src)


# ============================================================
# COMPROBAR CRS
# ============================================================

crs_list = [src.crs for src in src_files]

if len(set(crs_list)) > 1:
    raise ValueError(
        "Las imágenes no tienen el mismo CRS.\n"
        f"CRS encontrados: {set(crs_list)}"
    )

print(f"CRS: {src_files[0].crs}")


# ============================================================
# MERGE
# ============================================================

print("\nCreando ortomosaico...")

mosaic, out_transform = merge(src_files)


# ============================================================
# METADATOS
# ============================================================

out_meta = src_files[0].meta.copy()

out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_transform,
    "crs": src_files[0].crs,
    "compress": "deflate",
    "BIGTIFF": "IF_SAFER"
})


# ============================================================
# GUARDAR
# ============================================================

print(f"\nGuardando: {OUTPUT_FILE}")

with rasterio.open(OUTPUT_FILE, "w", **out_meta) as dest:
    dest.write(mosaic)


# ============================================================
# CERRAR ARCHIVOS
# ============================================================

for src in src_files:
    src.close()


print("\n========================================")
print("ORTOMOSAICO CREADO CORRECTAMENTE")
print("========================================")
print(f"Archivo: {OUTPUT_FILE}")
print(f"Dimensiones: {mosaic.shape[2]} x {mosaic.shape[1]}")
print(f"Bandas: {mosaic.shape[0]}")
print(f"CRS: {src_files[0].crs}")