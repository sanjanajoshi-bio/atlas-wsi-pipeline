import openslide
import numpy as np
import cv2

slide = openslide.OpenSlide("data/wsi/sample.svs")
thumb = slide.get_thumbnail((2000, 2000))
thumb = np.array(thumb)[:, :, :3]

cv2.imwrite(
    "outputs/figures/slide_thumbnail.png",
    cv2.cvtColor(thumb, cv2.COLOR_RGB2BGR)
)

print("Saved slide_thumbnail.png")

