from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from utils import check_input_, window_global_style_str
from functools import partial


class SegmentKmeansWin(QMainWindow):
    segment_kmeans_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(SegmentKmeansWin, self).__init__(parent=None)
        self.setFixedSize(500, 500)
        self.setWindowTitle("K-Means Parameter Settings")
        self.glob_style = window_global_style_str(
            font_size=14
        )

        self.edit_k_text = QLabel(self)
        self.edit_best_label_text = QLabel(self)
        self.edit_k = QSpinBox(self)
        self.edit_best_label = QSpinBox(self)

        self.edit_k_text.setGeometry(QRect(10, 20, 200, 50))
        self.edit_best_label_text.setGeometry(QRect(10, 100, 200, 50))
        self.edit_k.setGeometry(QRect(230, 20, 150, 50))
        self.edit_best_label.setGeometry(QRect(230, 100, 150, 50))

        self.edit_k_text.setText("Number Of Classes")
        self.edit_best_label_text.setText("Target Id")
        self.edit_k.setMaximum(20)
        self.edit_k.setMinimum(3)
        self.edit_best_label.setMaximum(3)
        self.edit_best_label.setMinimum(0)

        self.preview_btn = QPushButton(self)
        self.confirm_btn = QPushButton(self)

        self.preview_btn.setGeometry(QRect(20, 200, 150, 60))
        self.confirm_btn.setGeometry(QRect(220, 200, 150, 60))

        self.preview_btn.setText("Preview")
        self.confirm_btn.setText("Confirm")

        self.setStyleSheet(self.glob_style)
        self.show()

        self.edit_k.valueChanged.connect(self.edit_k_fcn_)
        self.edit_best_label.valueChanged.connect(self.edit_label_fcn_)

        self.preview_btn.clicked.connect(partial(self.emit_fcn_, False))
        self.confirm_btn.clicked.connect(partial(self.emit_fcn_, True))

        self.kmeans_info = dict(
            k=3,
            label=0,
            is_confirm=False
        )

    def edit_k_fcn_(self):
        self.kmeans_info['k'] = self.edit_k.value()
        self.edit_best_label.setMaximum(self.edit_k.value())

    def edit_label_fcn_(self):
        self.kmeans_info['label'] = self.edit_best_label.value()

    def emit_fcn_(self, is_confirm):
        self.kmeans_info['is_confirm'] = is_confirm
        self.segment_kmeans_signal_.emit(self.kmeans_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SegmentKmeansWin()
    win.show()
    sys.exit(app.exec_())
