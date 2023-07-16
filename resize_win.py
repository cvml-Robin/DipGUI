from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys


class ResizeWin(QMainWindow):
    change_size_signal_ = pyqtSignal(tuple)

    def __init__(self, glob_ratio=1):
        super(ResizeWin, self).__init__(parent=None)
        self.glob_ratio = glob_ratio
        self.glob_style = "font-size:%dpt;font-weight:bold;font-family:Calibri" % (16 * glob_ratio)
        self.setFixedSize(500, 400)
        self.setStyleSheet(self.glob_style)
        self.setWindowTitle("Resize Parameter")

        self.input_height = QLineEdit(self)
        self.input_width = QLineEdit(self)
        self.interp_box = QComboBox(self)
        self.input_height_text = QLabel(self)
        self.input_width_text = QLabel(self)
        self.interp_text = QLabel(self)

        self.input_height.setGeometry(QRect(240, 20, 200, 70))
        self.input_width.setGeometry(QRect(240, 100, 200, 70))
        self.interp_box.setGeometry(QRect(240, 180, 200, 70))
        self.input_height_text.setGeometry(QRect(20, 20, 200, 70))
        self.input_width_text.setGeometry(QRect(20, 100, 200, 70))
        self.interp_text.setGeometry(QRect(20, 180, 200, 70))

        self.input_height.setText("500")
        self.input_width.setText("500")
        self.interp_box.addItems(['BiNearest', 'BiLinear', 'BiCubic', 'Area'])
        self.input_height_text.setText("Height:")
        self.input_width_text.setText("Width:")
        self.interp_text.setText("Interpolate:")

        self.input_height_text.setAlignment(Qt.AlignCenter)
        self.input_width_text.setAlignment(Qt.AlignCenter)
        self.interp_text.setAlignment(Qt.AlignCenter)

        self.input_height.editingFinished.connect(self.change_height_)
        self.input_width.editingFinished.connect(self.change_width_)
        self.interp_box.currentIndexChanged.connect(self.choose_interp_)

        self.preview_btn = QPushButton(self)
        self.confirm_button = QPushButton(self)
        self.preview_btn.setText("Preview")
        self.confirm_button.setText("Confirm")
        self.preview_btn.setGeometry(QRect(40, 300, 180, 70))
        self.confirm_button.setGeometry(QRect(500-180-40, 300, 180, 70))
        self.confirm_button.setStyleSheet(self.glob_style)
        self.preview_btn.clicked.connect(self.preview_fcn_)
        self.confirm_button.clicked.connect(self.confirm_fcn_)

        self.new_width = 500
        self.new_height = 500
        self.interp_idx = 0

        self.show()

    def change_height_(self):
        try:
            int(self.input_height.text())
            self.new_height = int(self.input_height.text())
        except:
            self.input_height.setText("500")
            self.new_height = 500

    def change_width_(self):
        try:
            int(self.input_width.text())
            self.new_width = int(self.input_width.text())
        except:
            self.input_width.setText("500")
            self.new_width = 500

    def choose_interp_(self):
        self.interp_idx = self.interp_box.currentIndex()

    def preview_fcn_(self):
        self.change_size_signal_.emit((self.new_height, self.new_width, self.interp_idx, False))

    def confirm_fcn_(self):
        self.change_size_signal_.emit((self.new_height, self.new_width, self.interp_idx, True))


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = ResizeWin()
    win.show()
    sys.exit(app.exec_())
