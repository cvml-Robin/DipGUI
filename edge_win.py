from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
from utils import check_input_
from functools import partial


class EdgeWin(QMainWindow):
    edge_signal_ = pyqtSignal(tuple)

    def __init__(self):
        super(EdgeWin, self).__init__(parent=None)
        self.setFixedSize(500, 400)
        self.setWindowTitle("Edge(Canny)")
        self.glob_style = "font-size:15pt;font-weight:bold;font-family:Calibri"
        self.thresh1_text = QLabel(self)
        self.thresh2_text = QLabel(self)
        self.aperture_size_text = QLabel(self)

        self.thresh1_edit = QLineEdit(self)
        self.thresh2_edit = QLineEdit(self)
        self.aperture_size_edit = QComboBox(self)
        self.preview_btn = QPushButton(self)
        self.confirm_btn = QPushButton(self)

        self.thresh1_text.setGeometry(QRect(20, 20, 150, 70))
        self.thresh2_text.setGeometry(QRect(20, 100, 150, 70))
        self.aperture_size_text.setGeometry(QRect(20, 180, 150, 70))

        self.thresh1_edit.setGeometry(QRect(175, 20, 150, 70))
        self.thresh2_edit.setGeometry(QRect(175, 100, 150, 70))
        self.aperture_size_edit.setGeometry(QRect(175, 180, 150, 70))
        self.confirm_btn.setGeometry(QRect(250, 280, 200, 70))
        self.preview_btn.setGeometry(QRect(20, 280, 200, 70))
        self.thresh1_text.setText("Thresh1")
        self.thresh2_text.setText("Thresh2")
        self.aperture_size_text.setText("Aperture\nSize")

        self.thresh1_edit.setText("0")
        self.thresh2_edit.setText("128")
        self.aperture_size_edit.addItems(["3", "5", "7"])
        self.confirm_btn.setText("Confirm")
        self.preview_btn.setText("Preview")
        self.setStyleSheet(self.glob_style)
        self.show()
        self.thresh1_edit.editingFinished.connect(self.thresh1_edit_fcn_)
        self.thresh2_edit.editingFinished.connect(self.thresh2_edit_fcn_)
        self.aperture_size_edit.currentIndexChanged.connect(self.aperture_size_edit_fcn_)

        self.confirm_btn.clicked.connect(partial(self.confirm_fcn_, True))
        self.preview_btn.clicked.connect(partial(self.confirm_fcn_, False))
        self.thresh1 = 0
        self.thresh2 = 128
        self.aperture_size = 3

    def thresh1_edit_fcn_(self):
        now_val = check_input_(
            tool=self.thresh1_edit,
            min_val=0,
            max_val=255,
            digit=0,
            f_d=int,
            default_val=0
        )
        self.thresh1 = now_val

    def thresh2_edit_fcn_(self):
        now_val = check_input_(
            tool=self.thresh2_edit,
            min_val=0,
            max_val=255,
            digit=0,
            f_d=int,
            default_val=128
        )
        self.thresh2 = now_val

    def aperture_size_edit_fcn_(self):
        c_id = self.aperture_size_edit.currentIndex()
        self.aperture_size = c_id * 2 + 3

    def confirm_fcn_(self, is_confirm):
        edge_info = (self.thresh1, self.thresh2, self.aperture_size, is_confirm)
        self.edge_signal_.emit(edge_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EdgeWin()
    win.show()
    sys.exit(app.exec_())