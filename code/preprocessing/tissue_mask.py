import openslide
import numpy as np
import cv2

slide = openslide.OpenSlide("data/wsi/sample.svs")

level = slide.level_count - 1
w, h = slide.level_dimensions[level]

img = np.array(
    slide.read_region((0, 0), level, (w, h))
)[:, :, :3]

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

_, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((7, 7), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.dilate(mask, kernel, iterations=2)

cv2.imwrite("outputs/tissue_mask_lowres.png", mask)

print("Saved outputs/tissue_mask_lowres.png")


