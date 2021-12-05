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


def hisEqualColor(img):
    """Convert image to a more equalized version"""
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img
