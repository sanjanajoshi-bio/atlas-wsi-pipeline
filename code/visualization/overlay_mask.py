import cv2
import numpy as np

slide = cv2.imread("outputs/figures/slide_thumbnail.png")
mask = cv2.imread("outputs/tissue_mask.png", 0)

mask = cv2.resize(mask, (slide.shape[1], slide.shape[0]))

overlay = slide.copy()
overlay[mask > 0] = [255, 0, 0]

out = cv2.addWeighted(overlay, 0.4, slide, 0.6, 0)

cv2.imwrite("outputs/figures/tissue_overlay.png", out)
print("Saved tissue_overlay.png")

