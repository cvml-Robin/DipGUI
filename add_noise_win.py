from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from utils import check_input_, window_global_style_str
from functools import partial


class AddNoiseWin(QMainWindow):
    add_noise_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(AddNoiseWin, self).__init__(parent=None)
        self.setFixedSize(400, 300)
        self.setWindowTitle("Add Noise")
        self.glob_style = window_global_style_str()
        self.tab_widget = QTabWidget(self)

        self.noise_gauss = QWidget(self.tab_widget)
        self.noise_sp = QWidget(self.tab_widget)
        self.noise_poisson = QWidget(self.tab_widget)
        self.tab_widget.addTab(self.noise_gauss, "Gauss")
        self.tab_widget.addTab(self.noise_sp, "Salt & Pepper")
        self.tab_widget.addTab(self.noise_poisson, "Poisson")

        self.tab_widget.setGeometry(QRect(10, 10, 580, 580))

        self.edit_sigma_text = QLabel(self.noise_gauss)
        self.edit_intensity_text = QLabel(self.noise_sp)

        self.edit_sigma = QLineEdit(self.noise_gauss)
        self.edit_intensity = QLineEdit(self.noise_sp)

        self.edit_sigma_text.setGeometry(QRect(10, 10, 200, 50))
        self.edit_intensity_text.setGeometry(QRect(10, 10, 200, 50))

        self.edit_sigma.setGeometry(QRect(230, 10, 150, 50))
        self.edit_intensity.setGeometry(QRect(230, 10, 150, 50))

        self.edit_sigma_text.setText("Sigma")
        self.edit_intensity_text.setText("Intensity")

        self.edit_sigma.setText("0.0001")
        self.edit_intensity.setText("0.0001")

        self.preview_btn = QPushButton(self.tab_widget)
        self.confirm_btn = QPushButton(self.tab_widget)
        self.preview_btn.setGeometry(QRect(10, 190, 150, 60))
        self.confirm_btn.setGeometry(QRect(380-160, 190, 150, 60))
        self.preview_btn.setText("Preview")
        self.confirm_btn.setText("Confirm")

        self.show()
        # self.tab_widget.setStyleSheet(self.glob_style)
        self.setStyleSheet(self.glob_style)

        self.edit_sigma.editingFinished.connect(self.edit_sigma_fcn_)
        self.edit_intensity.editingFinished.connect(self.edit_intensity_fcn_)

        self.preview_btn.clicked.connect(partial(self.emit_fcn_, False))
        self.confirm_btn.clicked.connect(partial(self.emit_fcn_, True))

        self.noise_info = dict(
            type='gauss',
            sigma=0.0001,
            intensity=0.0001,
            is_confirm=False
        )

    def edit_sigma_fcn_(self):
        now_val = check_input_(
            tool=self.edit_sigma,
            max_val=1.0000,
            min_val=0.0001,
            default_val=0.0001,
            digit=4,
            f_d=float
        )
        self.noise_info['sigma'] = now_val

    def edit_intensity_fcn_(self):
        now_val = check_input_(
            tool=self.edit_intensity,
            max_val=1.0000,
            min_val=0.0001,
            default_val=0.0001,
            digit=4,
            f_d=float
        )
        self.noise_info['intensity'] = now_val

    def emit_fcn_(self, is_confirm):
        self.noise_info['is_confirm'] = is_confirm
        if self.tab_widget.currentIndex() == 0:
            self.noise_info['type'] = 'gauss'
        elif self.tab_widget.currentIndex() == 1:
            self.noise_info['type'] = 'sp'
        else:
            self.noise_info['type'] = 'poisson'

        self.add_noise_signal_.emit(self.noise_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AddNoiseWin()
    win.show()
    sys.exit(app.exec_())

