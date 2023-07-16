from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
from functools import partial


class MoreStrucElementWin(QMainWindow):
    more_struct_signal_ = pyqtSignal(np.ndarray)

    def __init__(self, width=5, height=5):
        super(MoreStrucElementWin, self).__init__(parent=None)
        desk_top = QDesktopWidget()
        desk_info = desk_top.geometry()
        self.desk_width = desk_info.width()
        self.desk_height = desk_info.height()
        desk_hw_ratio = self.desk_height / self.desk_width
        if (height / width) < desk_hw_ratio:
            if width * 25 < self.desk_width:
                chk_size = 20
                chk_gap = 5
            else:
                chk_size = (self.desk_width * 0.9 - 40) / width
                chk_gap = int(chk_size / 5)
                chk_size = int(chk_size - chk_gap)
        else:
            if height * 25 < self.desk_height:
                chk_size = 20
                chk_gap = 5
            else:
                chk_size = (self.desk_height * 0.9 - 120) / height
                chk_gap = int(chk_size / 5)
                chk_size = int(chk_size - chk_gap)
        chk_w = (chk_size + chk_gap)

        self.win_width = int((chk_size + chk_gap) * width + 40)
        self.win_height = int((chk_size + chk_gap) * height + 100)

        self.column_n = width
        self.row_n = height
        self.setFixedSize(self.win_width, self.win_height)
        self.chk_box = []
        self.struct_img = np.zeros((height, width))
        for jj in range(height):
            for ii in range(width):
                now_check_box = QCheckBox(self)
                now_check_box.setGeometry(
                    QRect(
                        ii * chk_w + 20, jj * chk_w + 20, chk_size, chk_size
                    )
                )
                now_check_box.setStyleSheet(
                    "QCheckBox::indicator{width:%dpx;height:%dpx}" % (chk_size, chk_size)
                )
                now_idx = jj * width + ii
                now_check_box.stateChanged.connect(partial(self.check_box_fcn_, now_idx))
                self.chk_box.append(now_check_box)
        self.confirm_btn = QPushButton(self)
        self.confirm_btn.setGeometry(
            QRect(
                int(self.win_width/2-100), self.win_height-70, 180, 60
            )
        )
        self.confirm_btn.setText("Confirm")
        self.confirm_btn.setStyleSheet("font-size:16pt;font-weight:bold;font-family:Calibri")
        self.confirm_btn.clicked.connect(self.confirm_fcn_)
        self.show()

    def check_box_fcn_(self, idx):
        now_ci = idx % self.column_n
        now_ri = int(idx/self.column_n)
        if self.chk_box[idx].isChecked():
            self.struct_img[now_ri, now_ci] = 1
        else:
            self.struct_img[now_ri, now_ci] = 0

    def confirm_fcn_(self):
        self.more_struct_signal_.emit(self.struct_img.astype(np.uint8))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MoreStrucElementWin(width=3, height=3)
    win.show()
    sys.exit(app.exec_())
