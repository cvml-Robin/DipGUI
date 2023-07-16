import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
from utils import check_input_
from functools import partial


class AdaptiveThreshWin(QMainWindow):
    adaptive_thresh_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(AdaptiveThreshWin, self).__init__(parent=None)
        self.setFixedSize(370, 450)
        self.setWindowTitle("Adaptive Threshold")
        self.glob_style = 'font-size:16pt;font-weight:bold;font-family:Calibri'

        self.thresh_method_text = QLabel(self)
        self.thresh_ksize_text = QLabel(self)
        self.thresh_const_text = QLabel(self)
        self.thresh_type_text = QLabel(self)

        self.thresh_method_edit = QComboBox(self)
        self.thresh_ksize_edit = QLineEdit(self)
        self.thresh_const_edit = QLineEdit(self)
        self.thresh_type_edit = QComboBox(self)

        self.preview_btn = QPushButton(self)
        self.confirm_btn = QPushButton(self)

        self.thresh_method_text.setGeometry(QRect(20, 20, 150, 70))
        self.thresh_ksize_text.setGeometry(QRect(20, 100, 150, 70))
        self.thresh_const_text.setGeometry(QRect(20, 180, 150, 70))
        self.thresh_type_text.setGeometry(QRect(20, 260, 150, 70))

        self.thresh_method_edit.setGeometry(QRect(200, 20, 150, 70))
        self.thresh_ksize_edit.setGeometry(QRect(200, 100, 150, 70))
        self.thresh_const_edit.setGeometry(QRect(200, 180, 150, 70))
        self.thresh_type_edit.setGeometry(QRect(200, 260, 150, 70))

        self.preview_btn.setGeometry(QRect(30, 350, 140, 60))
        self.confirm_btn.setGeometry(QRect(200, 350, 140, 60))

        self.thresh_method_text.setText("Method")
        self.thresh_ksize_text.setText("Ksize")
        self.thresh_const_text.setText("Const")
        self.thresh_type_text.setText("Type")

        self.thresh_method_edit.addItems(["Mean", "Gauss"])
        self.thresh_ksize_edit.setText("5")
        self.thresh_const_edit.setText("5")
        self.thresh_type_edit.addItems(["Binary", "Binary Inv"])
        self.preview_btn.setText("Preview")
        self.confirm_btn.setText("Confirm")

        self.show()
        self.setStyleSheet(self.glob_style)

        self.thresh_method_edit.currentIndexChanged.connect(self.edit_thresh_method_)
        self.thresh_type_edit.currentIndexChanged.connect(self.edit_thresh_type_)
        self.thresh_ksize_edit.editingFinished.connect(self.edit_thresh_ksize_)
        self.thresh_const_edit.editingFinished.connect(self.edit_thresh_const_)

        self.preview_btn.clicked.connect(partial(self.do_adaptive_thresh_fcn_, False))
        self.confirm_btn.clicked.connect(partial(self.do_adaptive_thresh_fcn_, True))

        self.thresh_info = dict(
            method=cv2.ADAPTIVE_THRESH_MEAN_C,
            type=cv2.THRESH_BINARY,
            ksize=5,
            C=5
        )

    def edit_thresh_method_(self):
        self.thresh_info['method'] = self.thresh_method_edit.currentIndex()

    def edit_thresh_ksize_(self):
        now_val = check_input_(
            tool=self.thresh_ksize_edit,
            default_val=3,
            min_val=3,
            max_val=501,
            digit=0,
            f_d=int
        )
        if now_val % 2 == 0:
            now_val = now_val + 1
        self.thresh_ksize_edit.setText(str(now_val))
        self.thresh_info['ksize'] = now_val

    def edit_thresh_const_(self):
        now_val = check_input_(
            tool=self.thresh_const_edit,
            min_val=-255,
            max_val=255,
            default_val=0,
            digit=0,
            f_d=int
        )
        self.thresh_info['C'] = now_val

    def edit_thresh_type_(self):
        self.thresh_info['type'] = self.thresh_type_edit.currentIndex()

    def do_adaptive_thresh_fcn_(self, is_confirm):
        self.thresh_info['is_confirm'] = is_confirm
        self.adaptive_thresh_signal_.emit(self.thresh_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AdaptiveThreshWin()
    win.show()
    sys.exit(app.exec_())
