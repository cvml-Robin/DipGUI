from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt

img = np.random.random((1000, 1000, 3))
img = (img * 255).astype(np.uint8)
fft_img = np.fft.fft2(img)
amp_img = np.abs(fft_img)
rad_img = np.angle(fft_img)
amp_img = np.log(1 + amp_img)
amp_img = amp_img / np.max(amp_img)
plt.figure()
plt.imshow(amp_img)
plt.show()