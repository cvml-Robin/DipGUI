from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
from morphology_struct_more_win import MoreStrucElementWin
from functools import partial

class MorphologyWin(QMainWindow):
    morph_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(MorphologyWin, self).__init__(parent=None)
        self.setFixedSize(620, 720)
        self.setWindowTitle("Morphology Settings")
        self.glob_style = 'font-size:16pt;font-weight:bold;font-family:Calibri'
        self.tab_widget = QTabWidget(self)
        self.tab_common = QWidget(self.tab_widget)
        self.tab_more = QWidget(self.tab_widget)

        self.tab_widget.addTab(self.tab_common, "Common")
        self.tab_widget.addTab(self.tab_more, "More")
        self.tab_widget.setGeometry(QRect(10, 10, 600, 700))

        self.ksize_text = QLabel(self.tab_common)
        self.shape_text = QLabel(self.tab_common)
        self.type_text = QLabel(self.tab_common)
        self.anchor_point_text = QLabel(self.tab_common)
        self.use_anchor_text = QLabel(self.tab_common)
        self.use_more_text = QLabel(self.tab_common)
        self.show_element_text = QLabel(self.tab_common)

        self.ksize_edit_w = QSpinBox(self.tab_common)
        self.ksize_edit_h = QSpinBox(self.tab_common)
        self.shape_edit = QComboBox(self.tab_common)
        self.type_edit = QComboBox(self.tab_common)
        self.anchor_edit_x = QSpinBox(self.tab_common)
        self.anchor_edit_y = QSpinBox(self.tab_common)
        self.use_anchor = QCheckBox(self.tab_common)
        self.use_more_check = QCheckBox(self.tab_common)
        self.show_element = QCheckBox(self.tab_common)

        self.ksize_text.setGeometry(QRect(20, 20, 220, 50))
        self.shape_text.setGeometry(QRect(20, 100, 220, 50))
        self.type_text.setGeometry(QRect(20, 180, 220, 50))
        self.anchor_point_text.setGeometry(QRect(20, 260, 220, 50))
        self.use_anchor_text.setGeometry(QRect(20, 340, 220, 50))
        self.use_more_text.setGeometry(QRect(20, 420, 220, 50))
        self.show_element_text.setGeometry(QRect(20, 500, 220, 50))

        self.ksize_edit_w.setGeometry(QRect(300, 20, 90, 50))
        self.ksize_edit_h.setGeometry(QRect(410, 20, 90, 50))
        self.shape_edit.setGeometry(QRect(300, 100, 200, 50))
        self.type_edit.setGeometry(QRect(300, 180, 200, 50))
        self.anchor_edit_x.setGeometry(QRect(300, 260, 90, 50))
        self.anchor_edit_y.setGeometry(QRect(410, 260, 90, 50))
        self.use_anchor.setGeometry(QRect(300, 340, 50, 50))
        self.use_more_check.setGeometry(QRect(300, 420, 50, 50))
        self.show_element.setGeometry(QRect(300, 500, 50, 50))

        self.ksize_text.setText("Kernel Size(W, H)")
        self.shape_text.setText("Kernel Shape")
        self.type_text.setText("Type")
        self.anchor_point_text.setText("Anchor Point(X,Y)")
        self.use_anchor_text.setText("Use Anchor Point")
        self.use_more_text.setText("Use More Struct")
        self.show_element_text.setText("Show Element")

        self.ksize_edit_w.setMaximum(10000)
        self.ksize_edit_w.setMinimum(2)
        self.ksize_edit_h.setMaximum(10000)
        self.ksize_edit_h.setMinimum(2)
        self.anchor_edit_x.setMinimum(-1)
        self.anchor_edit_y.setMinimum(-1)
        self.anchor_edit_x.setMaximum(1)
        self.anchor_edit_y.setMaximum(1)
        self.anchor_edit_x.setValue(-1)
        self.anchor_edit_y.setValue(-1)
        self.anchor_edit_x.setEnabled(False)
        self.anchor_edit_y.setEnabled(False)
        self.use_anchor.setChecked(False)
        self.shape_edit.addItems(["Rect", "Cross", "Ellipse"])
        self.type_edit.addItems(
            ["Erode", "Dilate", "Open", "Close", "Gradient", "TopHat", "BlackHat", "HitMiss"]
        )

        self.more_edit_ksize_text = QLabel(self.tab_more)
        self.more_edit_w = QSpinBox(self.tab_more)
        self.more_edit_h = QSpinBox(self.tab_more)
        self.more_start_btn = QPushButton(self.tab_more)

        self.more_edit_ksize_text.setGeometry(QRect(20, 20, 200, 50))
        self.more_edit_w.setGeometry(QRect(300, 20, 90, 50))
        self.more_edit_h.setGeometry(QRect(410, 20, 90, 50))
        self.more_start_btn.setGeometry(QRect(190, 120, 200, 70))

        self.more_edit_ksize_text.setText("Kernel Size(W, H)")
        self.more_edit_w.setMinimum(2)
        self.more_edit_h.setMinimum(2)
        self.more_edit_w.setMaximum(50)
        self.more_edit_h.setMaximum(50)
        self.more_start_btn.setText("Start Design")

        self.preview_btn = QPushButton(self)
        self.confirm_btn = QPushButton(self)
        self.preview_btn.setGeometry(QRect(300-220, 620, 200, 50))
        self.confirm_btn.setGeometry(QRect(300+20, 620, 200, 50))
        self.preview_btn.setText("Preview")
        self.confirm_btn.setText("Confirm")

        self.show()
        self.setStyleSheet(self.glob_style)

        self.ksize_edit_w.valueChanged.connect(self.edit_ksize_w_fcn_)
        self.ksize_edit_h.valueChanged.connect(self.edit_ksize_h_fcn_)
        self.shape_edit.currentTextChanged.connect(self.edit_shape_fcn_)
        self.type_edit.currentTextChanged.connect(self.edit_type_fcn_)
        self.use_anchor.stateChanged.connect(self.use_anchor_fcn_)
        self.anchor_edit_x.valueChanged.connect(self.edit_anchor_x)
        self.anchor_edit_y.valueChanged.connect(self.edit_anchor_y)
        self.use_more_check.stateChanged.connect(self.use_more_check_fcn_)
        self.show_element.stateChanged.connect(self.show_element_check_)
        self.more_edit_w.valueChanged.connect(self.edit_more_w)
        self.more_edit_h.valueChanged.connect(self.edit_more_h)

        self.more_start_btn.clicked.connect(self.more_start_fcn_)

        self.preview_btn.clicked.connect(partial(self.emit_fcn_, False))
        self.confirm_btn.clicked.connect(partial(self.emit_fcn_, True))

        self.tab_widget.currentChanged.connect(self.tab_id_change_fcn_)

        self.morph_info = dict(
            h=2,
            w=2,
            shape=0,
            type=0,
            ax=-1,
            ay=-1,
            use_anchor=False,
            use_more=False,
            struct_element=np.zeros((2, 2)),
            is_confirm=False,
            show_element=False
        )
        self.more_win = 0
        self.use_more_check.setEnabled(False)

    def show_element_check_(self):
        self.morph_info['show_element'] = self.show_element.isChecked()

    def tab_id_change_fcn_(self):
        if type(self.more_win) == int:
            if self.tab_widget.currentIndex() == 1:
                self.preview_btn.setEnabled(False)
                self.confirm_btn.setEnabled(False)
            else:
                self.preview_btn.setEnabled(True)
                self.confirm_btn.setEnabled(True)

    def edit_ksize_w_fcn_(self):
        new_w = int(self.ksize_edit_w.value())
        self.anchor_edit_x.setMaximum(new_w-1)
        self.morph_info['w'] = new_w

    def edit_ksize_h_fcn_(self):
        new_h = int(self.ksize_edit_h.value())
        self.anchor_edit_y.setMaximum(new_h-1)
        self.morph_info['h'] = new_h

    def edit_shape_fcn_(self):
        self.morph_info['shape'] = self.shape_edit.currentIndex()

    def edit_type_fcn_(self):
        self.morph_info['type'] = self.type_edit.currentIndex()

    def edit_anchor_x(self):
        new_ax = self.anchor_edit_x.value()
        self.morph_info['ax'] = new_ax

    def edit_anchor_y(self):
        new_ay = self.anchor_edit_y.value()
        self.morph_info['ay'] = new_ay

    def use_anchor_fcn_(self):
        self.morph_info['use_anchor'] = self.use_anchor.isChecked()
        if self.use_anchor.isChecked():
            self.anchor_edit_x.setEnabled(True)
            self.anchor_edit_y.setEnabled(True)
        else:
            self.anchor_edit_x.setEnabled(False)
            self.anchor_edit_y.setEnabled(False)

    def use_more_check_fcn_(self):
        if self.use_more_check.isChecked():
            self.shape_edit.setEnabled(False)
            self.ksize_edit_w.setEnabled(False)
            self.ksize_edit_h.setEnabled(False)
        else:
            self.shape_edit.setEnabled(True)
            self.ksize_edit_w.setEnabled(True)
            self.ksize_edit_h.setEnabled(True)

    def edit_more_h(self):
        new_h = self.more_edit_h.value()
        self.anchor_edit_y.setMaximum(new_h - 1)

    def edit_more_w(self):
        new_w = self.more_edit_w.value()
        self.anchor_edit_x.setMaximum(new_w - 1)

    def more_start_fcn_(self):
        more_ksize_h = self.more_edit_h.value()
        more_ksize_w = self.more_edit_w.value()
        self.more_win = MoreStrucElementWin(
            height=more_ksize_h,
            width=more_ksize_w
        )
        self.more_win.show()
        self.preview_btn.setEnabled(True)
        self.confirm_btn.setEnabled(True)
        self.use_more_check.setEnabled(True)

    def emit_fcn_(self, is_confirm):
        if type(self.more_win) != int:
            self.morph_info['struct_element'] = self.more_win.struct_img.astype(np.uint8)
            self.morph_info['use_more'] = self.use_more_check.isChecked()
        self.morph_info['is_confirm'] = is_confirm
        self.morph_signal_.emit(self.morph_info)
        # print(self.morph_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MorphologyWin()
    win.show()
    sys.exit(app.exec_())
    # src_img = cv2.imread("img5.jpg")
    # src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
    # gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
    # _, bw_img = cv2.threshold(
    #     src=gray_img,
    #     maxval=255,
    #     type=cv2.THRESH_OTSU,
    #     thresh=cv2.THRESH_BINARY
    # )
    #
    # kernel = cv2.getStructuringElement(
    #     shape=2,
    #     ksize=(6, 23)
    # )
    #
    # morph_img = cv2.morphologyEx(
    #     src=src_img,
    #     op=6,
    #     kernel=kernel,
    #     anchor=(-1, -1)
    # )
    #
    # plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.imshow(src_img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(morph_img)
    # plt.show()
