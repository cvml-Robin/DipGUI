import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import re


class ImageInfoWin(QMainWindow):
    def __init__(self, src_img=None, file_path=""):
        super(ImageInfoWin, self).__init__(parent=None)
        self.setFixedSize(700, 300)
        self.setWindowTitle("File Info")
        self.glob_style = 'font-size:13pt;font-family:宋体'
        self.info_label = QLabel(self)
        self.info_label.setGeometry(QRect(5, 5, 600, 300))
        self.src_img = src_img
        # self.src_img = np.random.random((500, 500, 3)).astype(np.uint8)
        h, w, _ = self.src_img.shape
        data_dtype = self.src_img.dtype
        file_format = re.findall("[.][^.]+", file_path)[0]
        info_str = 'Height: %d\nWidth: %d\nDepth: %s\nFormat: %s\nPath: %s' % (
            h,
            w,
            data_dtype,
            file_format,
            file_path
        )
        self.info_label.setText(info_str)
        self.setStyleSheet(self.glob_style)
        self.info_label.setAlignment(Qt.AlignTop)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ImageInfoWin()
    win.show()
    sys.exit(app.exec_())
