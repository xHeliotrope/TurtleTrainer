#!/usr/bin/env python3

# rgb -> hex
import numpy as np
from PIL import Image
import PIL

def greyscale(r, g, b):
    return .2126 * r + .7152 * g + .0722 * b

def get_img(name):
    return Image.open(name, 'r')

img = get_img('important_image.jpeg')

im_arr = np.fromstring(img.tobytes(), dtype=np.uint8)

im = PIL.Image.fromarray(im_arr)
im.show()
