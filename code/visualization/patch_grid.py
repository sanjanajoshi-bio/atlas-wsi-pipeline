import cv2
import numpy as np
from pathlib import Path

patches = sorted(Path("data/patches").glob("*.png"))[:64]
imgs = [cv2.imread(str(p)) for p in patches]

grid = []
for i in range(0, 64, 8):
    grid.append(np.hstack(imgs[i:i+8]))

grid = np.vstack(grid)
cv2.imwrite("outputs/figures/patch_grid.png", grid)

print("Saved patch_grid.png")

