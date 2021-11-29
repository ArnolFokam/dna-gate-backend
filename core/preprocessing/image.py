from cv2 import cv2
import numpy as np


def bytes2image(bytes_string):
    """"convert bytes string to opencv (BGR) image"""
    im_array = np.asarray(bytearray(bytes_string), dtype=np.uint8)
    im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
    return im


def image2bytes(image, ext='jpg'):
    """convert opencv (BGR) image to bytes string"""
    _, buffer = cv2.imencode(f'.{ext}', image)
    return buffer.tobytes()
