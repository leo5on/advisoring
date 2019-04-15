#!/usr/bin/env python
from skimage import io, feature, color, draw
from skimage.measure import CircleModel, ransac
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.path import Path
from matplotlib.patches import Circle, PathPatch

image = io.imread('/home/leleo/Documents/BIR/computer-vision/sun.jpg')

edges = feature.canny(color.rgb2gray(image), sigma=2)


points = np.array(np.nonzero(edges)).T
model_robust, inliers = ransac(points, CircleModel, min_samples=3, residual_threshold=2, max_trials=1000)
cy, cx, r = model_robust.params
print(cy, cx, r)

f, (ax0, ax1) = plt.subplots(1, 2, figsize=(15, 8))

circle = plt.Circle((cx, cy), radius=r, facecolor='none', linewidth=2)
circle_path = Path(points)
circle_patch = PathPatch(circle)
ax0.add_patch(circle_patch)
ax0.axis('image')

ax1.plot(points[inliers, 1], points[inliers, 0], 'b.', markersize=1)
ax1.plot(points[~inliers, 1], points[~inliers, 0], 'g.', markersize=1)
ax1.axis('image')

ax0.imshow(image)
ax1.imshow(image)

plt.show()