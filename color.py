#!/usr/bin/env python3

# rgb -> hex
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def get_img(name):
    return Image.open(name, 'r').convert('L')

img = get_img('important_image.jpeg')

im_arr = np.asarray(img)

dft_array = np.fft.fft2(im_arr) 
freq = np.fft.fftfreq(im_arr.shape[-1])
print(freq)
print(dft_array.shape)
#plt.plot(freq, dft_array.real, freq, dft_array.imag)
#plt.show()

#im = Image.fromarray(im_arr)
#im.show()
