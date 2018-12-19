#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import cv2
from pywt import dwt2

img = cv2.imread('important_image.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cA, (cH, cV, cD) = dwt2(img, 'db1')

fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([cA, cH, cV, cD]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()
