from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    src_img = cv2.imread("img5.jpg")
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    _, bw_img = cv2.threshold(
        src=gray_img,
        thresh=cv2.THRESH_BINARY,
        type=cv2.THRESH_OTSU,
        maxval=255
    )

    kernel = cv2.getStructuringElement(
        shape=cv2.MORPH_ELLIPSE,
        ksize=(20, 20)
    )

    bw_img = cv2.morphologyEx(
        src=bw_img,
        kernel=kernel,
        op=cv2.MORPH_OPEN
    )

    contours, A = cv2.findContours(
        image=bw_img,
        mode=cv2.RETR_TREE,
        method=cv2.CHAIN_APPROX_NONE
    )
    A = A[0]

    gray_vec = np.reshape(gray_img, (gray_img.shape[1] * gray_img.shape[0], 1))
    seg_k = 14
    _, label_mat, _ = cv2.kmeans(
        data=(gray_vec/255).astype(np.float32),
        K=seg_k,
        bestLabels=1,
        criteria=(cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 10, 1),
        attempts=10,
        flags=cv2.KMEANS_RANDOM_CENTERS
    )
    label_mat = np.reshape(label_mat, (gray_img.shape[0], gray_img.shape[1]))
    hsv_img = np.ones_like(src_img).astype(np.float32)
    hsv_img[:, :, 0] = (label_mat*0.7 / (seg_k - 1)).astype(np.float32)
    hsv_img = (hsv_img * 255).astype(np.uint8)
    hsv_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)

    # print(label_mat.shape)
    # print(cv2.cvtColor(np.array([[[255, 255, 255]]]).astype(np.uint8), cv2.COLOR_HSV2RGB))

    # plt.figure()
    # plt.imshow(src_img[:, :, [2, 1, 0]])
    # plt.imshow(bw_img, 'gray')
    # for ii in range(len(contours)):
    #     now_vec = contours[ii]
    #     if A[ii, 2] != -1:
    #         l_color = 'b'
    #     else:
    #         l_color = 'r'
    #     plt.plot(now_vec[:, :, 0], now_vec[:, :, 1], color=l_color, linewidth=2)
    print(label_mat.dtype)
    plt.figure()
    plt.imshow(hsv_img)
    plt.show()

