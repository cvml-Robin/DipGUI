from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
from functools import partial
from utils import window_global_style_str, check_input_


class NonLinearTransformWin(QMainWindow):
    non_linear_trans_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(NonLinearTransformWin, self).__init__(parent=None)
        self.setFixedSize(400, 400)
        self.setWindowTitle("NonLinearTransform")
        self.glob_style = window_global_style_str()
        self.coe_text = QLabel(self)
        self.gamma_text = QLabel(self)
        self.const_text = QLabel(self)
        self.coe_edit = QLineEdit(self)
        self.gamma_edit = QLineEdit(self)
        self.const_edit = QLineEdit(self)

        self.coe_text.setGeometry(QRect(10, 20, 200, 50))
        self.gamma_text.setGeometry(QRect(10, 100, 200, 50))
        self.const_text.setGeometry(QRect(10, 180, 200, 50))
        self.coe_edit.setGeometry(QRect(230, 20, 150, 50))
        self.gamma_edit.setGeometry(QRect(230, 100, 150, 50))
        self.const_edit.setGeometry(QRect(230, 180, 150, 50))

        self.coe_text.setText("Coefficient:")
        self.gamma_text.setText("Gamma:")
        self.const_text.setText("Const:")
        self.coe_edit.setText("1.000")
        self.gamma_edit.setText("1.000")
        self.const_edit.setText("0.000")

        self.preview_btn = QPushButton(self)
        self.confirm_btn = QPushButton(self)

        self.preview_btn.setGeometry(QRect(10, 280, 140, 50))
        self.confirm_btn.setGeometry(QRect(240, 280, 140, 50))
        self.preview_btn.setText("Preview")
        self.confirm_btn.setText("Confirm")

        self.trans_info = dict(
            coe=1.0,
            gamma=1.0,
            const=0.0,
            is_confirm=False
        )

        self.coe_edit.editingFinished.connect(self.edit_coe_fcn_)
        self.gamma_edit.editingFinished.connect(self.edit_gamma_fcn_)
        self.const_edit.editingFinished.connect(self.edit_const_fcn_)

        self.preview_btn.clicked.connect(partial(self.emit_fcn_, False))
        self.confirm_btn.clicked.connect(partial(self.emit_fcn_, True))

        self.setStyleSheet(self.glob_style)

    def edit_coe_fcn_(self):
        now_val = check_input_(
            tool=self.coe_edit,
            max_val=65535.0,
            min_val=-65535.0,
            default_val=1.0,
            digit=3,
            f_d=float
        )
        self.trans_info['coe'] = now_val

    def edit_gamma_fcn_(self):
        now_val = check_input_(
            tool=self.gamma_edit,
            max_val=20.000,
            min_val=0.0001,
            default_val=1.0,
            digit=4,
            f_d=float
        )
        self.trans_info['gamma'] = now_val

    def edit_const_fcn_(self):
        now_val = check_input_(
            tool=self.const_edit,
            max_val=1.0,
            min_val=0.0,
            default_val=0.0,
            digit=3,
            f_d=float
        )
        self.trans_info['const'] = now_val

    def emit_fcn_(self, is_confirm):
        self.trans_info['is_confirm'] = is_confirm
        self.non_linear_trans_signal_.emit(self.trans_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NonLinearTransformWin()
    win.show()
    sys.exit(app.exec_())
