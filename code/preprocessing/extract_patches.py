import openslide
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm

# Parameters (you WILL tune these later)
PATCH_SIZE = 256
TISSUE_THRESHOLD = 0.15   # % of tissue required
OUTPUT_DIR = Path("data/patches")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load slide
slide = openslide.OpenSlide("data/wsi/sample.svs")

# Load low-res mask
mask = cv2.imread("outputs/tissue_mask_lowres.png", cv2.IMREAD_GRAYSCALE)

# Use lowest resolution level for mask
mask_level = slide.level_count - 1
mask_w, mask_h = slide.level_dimensions[mask_level]

# High-res info
level0_w, level0_h = slide.level_dimensions[0]
scale_x = level0_w / mask_w
scale_y = level0_h / mask_h

patch_id = 0

for y in tqdm(range(0, mask_h, PATCH_SIZE // int(scale_y))):
    for x in range(0, mask_w, PATCH_SIZE // int(scale_x)):

        mask_patch = mask[
            y:y + int(PATCH_SIZE / scale_y),
            x:x + int(PATCH_SIZE / scale_x)
        ]

        if mask_patch.size == 0:
            continue

        tissue_ratio = np.mean(mask_patch > 0)

        if tissue_ratio < TISSUE_THRESHOLD:
            continue

        # Map to level 0 coordinates
        x0 = int(x * scale_x)
        y0 = int(y * scale_y)

        patch = slide.read_region(
            (x0, y0),
            0,
            (PATCH_SIZE, PATCH_SIZE)
        )

        patch = np.array(patch)[:, :, :3]

        cv2.imwrite(
            str(OUTPUT_DIR / f"patch_{patch_id}.png"),
            cv2.cvtColor(patch, cv2.COLOR_RGB2BGR)
        )

        patch_id += 1

print(f"Saved {patch_id} patches")

