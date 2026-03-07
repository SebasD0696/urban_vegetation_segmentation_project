import os
import rasterio
import numpy as np

# ---- CONFIGURACIÓN ----
input_tif = r"C:\Users\Usuario\Downloads\Segmentacion_Project\Floridablanca\Floridablanca_Recortado.tif"
output_folder = r"C:\Users\Usuario\Downloads\Segmentacion_Project\Floridablanca\Floridablanca_tiles"
tile_size = 512

os.makedirs(output_folder, exist_ok=True)

with rasterio.open(input_tif) as src:

    width = src.width
    height = src.height
    count = src.count
    profile = src.profile

    tile_id = 0

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):

            window = rasterio.windows.Window(x, y, tile_size, tile_size)
            tile = src.read(window=window)

            # Verificar si existe banda alpha
            if count == 4:
                alpha = tile[3]  # banda alpha

                # Si todo es transparente (alpha = 0)
                if np.all(alpha == 0):
                    continue

            # Actualizar perfil para el tile
            profile.update({
                "height": tile.shape[1],
                "width": tile.shape[2],
                "transform": rasterio.windows.transform(window, src.transform)
            })

            output_path = os.path.join(output_folder, f"tile_{tile_id}.tif")

            with rasterio.open(output_path, "w", **profile) as dst:
                dst.write(tile)

            tile_id += 1

print("Proceso terminado. Tiles guardados:", tile_id)