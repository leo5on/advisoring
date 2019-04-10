#!/usr/bin/env python
from skimage import io
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

image = io.mread('/home/leo5on/Documents/BIR/Advisoring/Sensor-calibratrion/sun.jpg')

f, ax = plt.subplots(figsize=(8.8))
ax.imshow(image)