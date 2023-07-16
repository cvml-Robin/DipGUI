from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys


class ImageRotateWin(QMainWindow):
    change_deg_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(ImageRotateWin, self).__init__(parent=None)
        self.back_gray_val = 190
        self.style_sheet = 'background:rgb(%d, %d, %d)' % (
            self.back_gray_val,
            self.back_gray_val,
            self.back_gray_val
        )
        self.setFixedSize(500, 500)
        self.setWindowTitle("Rotate")
        self.rotate_slid = QSlider(Qt.Horizontal, self)
        self.rotate_slid.setMaximum(360)
        self.rotate_slid.setMinimum(0)
        self.rotate_slid.setGeometry(QRect(50, 50, 400, 40))

        self.deg_text = QLineEdit(self)
        self.deg_text.setGeometry(QRect(50, 120, 400, 50))
        self.deg_text.setStyleSheet("font-size:16pt;font-weight:bold;font-family:Calibri")
        self.deg_text.setText("0")
        # self.rotate_slid.sliderReleased.connect(self.slid_change_fcn_)
        self.rotate_slid.valueChanged.connect(self.slid_change_fcn_)
        self.deg_text.editingFinished.connect(self.change_deg_fcn_)

        self.confirm_button = QPushButton(self)
        self.confirm_button.setGeometry(QRect(250-90, 200, 180, 80))
        self.confirm_button.setText("Confirm")
        self.confirm_button.setStyleSheet("font-size:16pt;font-weight:bold;font-family:Calibri")
        self.confirm_button.clicked.connect(self.confirm_fcn_)
        self.now_deg = 0
        self.show()

    def slid_change_fcn_(self):
        self.now_deg = self.rotate_slid.value()
        self.deg_text.setText('%d' % self.now_deg)
        self.change_deg_signal_.emit(
            dict(
                angle=self.now_deg,
                is_confirm=False
            )
        )

    def change_deg_fcn_(self):
        try:
            self.now_deg = int(self.deg_text.text())
        except:
            self.now_deg = 0
        self.now_deg = np.maximum(np.minimum(self.now_deg, 360), 0)
        self.deg_text.setText('%d' % self.now_deg)
        self.rotate_slid.setValue(self.now_deg)
        self.change_deg_signal_.emit(
            dict(
                angle=self.now_deg,
                is_confirm=False
            )
        )

    def confirm_fcn_(self):
        self.change_deg_signal_.emit(
            dict(
                angle=self.now_deg,
                is_confirm=True
            )
        )
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ImageRotateWin()
    win.show()
    sys.exit(app.exec_())
