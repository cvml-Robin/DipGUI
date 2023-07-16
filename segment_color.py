import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class SegmentColorSpace(QMainWindow):
    preview_signal_ = pyqtSignal(dict)
    segment_color_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(SegmentColorSpace, self).__init__(parent=None)
        self.setFixedSize(600, 600)
        self.setWindowTitle("Segment Color Space")
        self.glob_style = 'font-size:16pt;font-weight:bold;font-family:Calibri'
        self.glob_style = self.glob_style

        self.tab_widget = QTabWidget(self)
        self.tab_bar = QTabBar(self.tab_widget)
        self.tab_widget.setGeometry(QRect(10, 10, 580, 580))
        self.tab_bar.setGeometry(QRect(0, 0, 580, 580))

        self.tab_rgb = self.tab_bar.addTab("RGB")
        self.tab_hsv = self.tab_bar.addTab("HSV")
        self.tab_hsl = self.tab_bar.addTab("HSL")
        self.tab_lab = self.tab_bar.addTab("LAB")
        self.tab_ycbcr = self.tab_bar.addTab("YCbCr")

        self.color_slid1 = QSlider(Qt.Horizontal, self.tab_bar)
        self.color_slid2 = QSlider(Qt.Horizontal, self.tab_bar)
        self.color_slid3 = QSlider(Qt.Horizontal, self.tab_bar)
        self.color_slid4 = QSlider(Qt.Horizontal, self.tab_bar)
        self.color_slid5 = QSlider(Qt.Horizontal, self.tab_bar)
        self.color_slid6 = QSlider(Qt.Horizontal, self.tab_bar)
        self.color_slid1.setGeometry(QRect(60, 60, 300, 40))
        self.color_slid2.setGeometry(QRect(60, 120, 300, 40))

        self.color_slid3.setGeometry(QRect(60, 220, 300, 40))
        self.color_slid4.setGeometry(QRect(60, 280, 300, 40))

        self.color_slid5.setGeometry(QRect(60, 380, 300, 40))
        self.color_slid6.setGeometry(QRect(60, 440, 300, 40))
        self.color_slid1.setMinimum(0)
        self.color_slid1.setMaximum(255)
        self.color_slid2.setMinimum(0)
        self.color_slid2.setMaximum(255)
        self.color_slid3.setMinimum(0)
        self.color_slid3.setMaximum(255)
        self.color_slid4.setMinimum(0)
        self.color_slid4.setMaximum(255)
        self.color_slid5.setMinimum(0)
        self.color_slid5.setMaximum(255)
        self.color_slid6.setMinimum(0)
        self.color_slid6.setMaximum(255)
        self.color_slid2.setValue(255)
        self.color_slid4.setValue(255)
        self.color_slid6.setValue(255)

        self.slid_text1 = QLabel(self)
        self.slid_text2 = QLabel(self)
        self.slid_text3 = QLabel(self)
        self.slid_text4 = QLabel(self)
        self.slid_text5 = QLabel(self)
        self.slid_text6 = QLabel(self)
        self.slid_text1.setGeometry(QRect(430, 60, 50, 50))
        self.slid_text2.setGeometry(QRect(430, 120, 50, 50))
        self.slid_text3.setGeometry(QRect(430, 220, 50, 50))
        self.slid_text4.setGeometry(QRect(430, 280, 50, 50))
        self.slid_text5.setGeometry(QRect(430, 380, 50, 50))
        self.slid_text6.setGeometry(QRect(430, 440, 50, 50))
        self.slid_text1.setText("0")
        self.slid_text2.setText("255")
        self.slid_text3.setText("0")
        self.slid_text4.setText("255")
        self.slid_text5.setText("0")
        self.slid_text6.setText("255")
        self.slid_text1.setAlignment(Qt.AlignCenter)
        self.slid_text2.setAlignment(Qt.AlignCenter)
        self.slid_text3.setAlignment(Qt.AlignCenter)
        self.slid_text4.setAlignment(Qt.AlignCenter)
        self.slid_text5.setAlignment(Qt.AlignCenter)
        self.slid_text6.setAlignment(Qt.AlignCenter)

        self.confirm_btn = QPushButton(self)
        self.confirm_btn.setGeometry(QRect(150, 500, 200, 60))
        self.confirm_btn.setText("Confirm")

        self.show()
        self.setStyleSheet(self.glob_style)

        # self.color_slid1.sliderReleased.connect(self.color_slid1_fcn_)
        # self.color_slid2.sliderReleased.connect(self.color_slid2_fcn_)
        # self.color_slid3.sliderReleased.connect(self.color_slid3_fcn_)
        # self.color_slid4.sliderReleased.connect(self.color_slid4_fcn_)
        # self.color_slid5.sliderReleased.connect(self.color_slid5_fcn_)
        # self.color_slid6.sliderReleased.connect(self.color_slid6_fcn_)

        self.color_slid1.valueChanged.connect(self.color_slid1_fcn_)
        self.color_slid2.valueChanged.connect(self.color_slid2_fcn_)
        self.color_slid3.valueChanged.connect(self.color_slid3_fcn_)
        self.color_slid4.valueChanged.connect(self.color_slid4_fcn_)
        self.color_slid5.valueChanged.connect(self.color_slid5_fcn_)
        self.color_slid6.valueChanged.connect(self.color_slid6_fcn_)
        self.tab_bar.currentChanged.connect(self.change_tab_fcn_)
        self.confirm_btn.clicked.connect(self.confirm_fcn_)

        self.color_info = dict(
            rgb=[0, 255, 0, 255, 0, 255],
            hsv=[0, 255, 0, 255, 0, 255],
            hsl=[0, 255, 0, 255, 0, 255],
            lab=[0, 255, 0, 255, 0, 255],
            ybr=[0, 255, 0, 255, 0, 255]
        )

        self.color_id = ['rgb', 'hsv', 'hsl', 'lab', 'ybr']
        self.emit_info = dict(
            color_space='rgb',
            th=[0, 255, 0, 255, 0, 255],
            is_confirm=False
        )

    def color_slid1_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        now_info[0] = self.color_slid1.value()
        self.slid_text1.setText(str(self.color_slid1.value()))
        self.emit_info['color_space'] = self.color_id[now_id]
        self.emit_info['th'] = now_info
        self.emit_info['is_confirm'] = False
        self.preview_signal_.emit(self.emit_info)

    def color_slid2_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        now_info[1] = self.color_slid2.value()
        self.slid_text2.setText(str(self.color_slid2.value()))
        self.emit_info['color_space'] = self.color_id[now_id]
        self.emit_info['th'] = now_info
        self.emit_info['is_confirm'] = False
        self.preview_signal_.emit(self.emit_info)

    def color_slid3_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        now_info[2] = self.color_slid3.value()
        self.slid_text3.setText(str(self.color_slid3.value()))
        self.emit_info['color_space'] = self.color_id[now_id]
        self.emit_info['th'] = now_info
        self.emit_info['is_confirm'] = False
        self.preview_signal_.emit(self.emit_info)

    def color_slid4_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        now_info[3] = self.color_slid4.value()
        self.slid_text4.setText(str(self.color_slid4.value()))
        self.emit_info['color_space'] = self.color_id[now_id]
        self.emit_info['th'] = now_info
        self.emit_info['is_confirm'] = False
        self.preview_signal_.emit(self.emit_info)

    def color_slid5_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        now_info[4] = self.color_slid5.value()
        self.slid_text5.setText(str(self.color_slid5.value()))
        self.emit_info['color_space'] = self.color_id[now_id]
        self.emit_info['th'] = now_info
        self.emit_info['is_confirm'] = False
        self.preview_signal_.emit(self.emit_info)

    def color_slid6_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        now_info[5] = self.color_slid6.value()
        self.slid_text6.setText(str(self.color_slid6.value()))
        self.emit_info['color_space'] = self.color_id[now_id]
        self.emit_info['th'] = now_info
        self.emit_info['is_confirm'] = False
        self.preview_signal_.emit(self.emit_info)

    def change_tab_fcn_(self):
        now_id = self.tab_bar.currentIndex()
        now_info = self.color_info[self.color_id[now_id]]
        self.color_slid1.setValue(now_info[0])
        self.color_slid2.setValue(now_info[1])
        self.color_slid3.setValue(now_info[2])
        self.color_slid4.setValue(now_info[3])
        self.color_slid5.setValue(now_info[4])
        self.color_slid6.setValue(now_info[5])

    def confirm_fcn_(self):
        # now_id = self.tab_bar.currentIndex()
        # now_info = self.color_info[self.color_id[now_id]]
        # print(now_info)
        self.emit_info['is_confirm'] = True
        self.preview_signal_.emit(self.emit_info)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SegmentColorSpace()
    win.show()
    sys.exit(app.exec_())
