# rgb -> hex
from Pillow import Image

def greyscale(r, g, b):
    return .2126 * r + .7152 * g + .0722 * b

def get_img(name):
    img = Image.read(name, 'r')

img = get_img('important_image.jpeg')
