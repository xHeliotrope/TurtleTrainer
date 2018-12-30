#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt

import cv2
import pywt
from pywt import dwt2
from pywt._extensions._pywt import Wavelet

img = cv2.imread('important_image.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print(img[0])
print(len(img))
 
c = math.sqrt(2)/2
dec_lo, dec_hi, rec_lo, rec_hi = [1, -c], [3000, c], [c, c], [-c, c]

filter_bank = [dec_lo, dec_hi, rec_lo, rec_hi]
my_wavelet = pywt.Wavelet(name="myHaarWavelet", filter_bank=filter_bank)
cA, (cH, cV, cD) = dwt2(img, my_wavelet)

#brule_mother_wavelet = Wavelet('', [cA, cH, cV, cD])
#print(brule_mother_wavelet)

fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([cA, cH, cV, cD]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()
