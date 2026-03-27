
import os
import random
import shutil
import numpy as np
from PIL import Image

IMAGES_DIR = "total_imagenes/tiles_florencia"
MASKS_DIR = "total_imagenes/masks_florencia"

OUTPUT_IMAGES = "pruebas_rgb"
OUTPUT_MASKS = "pruebas_mask"

NUM_SAMPLES = 100

# umbrales
DARK_THRESHOLD = 5
BRIGHT_THRESHOLD = 245

MIN_VALID_RATIO = 0.7


os.makedirs(OUTPUT_IMAGES, exist_ok=True)
os.makedirs(OUTPUT_MASKS, exist_ok=True)


filenames = [
    f for f in os.listdir(IMAGES_DIR)
    if f.lower().endswith((".png",".jpg",".tif"))
]

print("Total images:",len(filenames))


def has_information(image_path):

    img = np.array(Image.open(image_path))

    brightness = img.mean(axis=2)

    dark = brightness < DARK_THRESHOLD
    bright = brightness > BRIGHT_THRESHOLD

    invalid = dark | bright

    invalid_ratio = np.sum(invalid) / brightness.size

    valid_ratio = 1 - invalid_ratio

    if valid_ratio < MIN_VALID_RATIO:
        return False

    return True


def find_mask(image_name):

    base = os.path.splitext(image_name)[0]

    for ext in [".png",".jpg",".tif"]:
        mask_name = base + "_mask" + ext
        mask_path = os.path.join(MASKS_DIR,mask_name)

        if os.path.exists(mask_path):
            return mask_path

    return None


valid_files = []

for name in filenames:

    img_path = os.path.join(IMAGES_DIR,name)

    if has_information(img_path):
        valid_files.append(name)

print("Valid images:",len(valid_files))


selected = random.sample(valid_files,min(NUM_SAMPLES,len(valid_files)))

print("Selected:",len(selected))


for name in selected:

    shutil.copy(
        os.path.join(IMAGES_DIR,name),
        os.path.join(OUTPUT_IMAGES,name)
    )

    mask_path = find_mask(name)

    if mask_path:

        shutil.copy(
            mask_path,
            os.path.join(OUTPUT_MASKS,os.path.basename(mask_path))
        )

print("Done!")