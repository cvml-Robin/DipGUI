from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import sys
import functools as f_tool
from image_process.utils import motion_kernel, gaussian_kernel, plateau_kernel


class SpatialFilterWin(QMainWindow):
    spatial_filter_signal_ = pyqtSignal(dict)

    def __init__(self):
        super(SpatialFilterWin, self).__init__(parent=None)
        self.glob_style = "font-size:15pt;font-weight:bold;font-family:Calibri"
        self.setStyleSheet(self.glob_style)
        self.back_gray_val = 190
        self.style_sheet = 'background:rgb(%d, %d, %d)' % (
            self.back_gray_val,
            self.back_gray_val,
            self.back_gray_val
        )
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Spatial Filter")
        self.tab_bar = QTabWidget(self)
        self.tab_bar.setGeometry(QRect(20, 20, 960, 560))
        tab_gauss = QWidget(self.tab_bar)
        tab_plateau = QWidget(self.tab_bar)
        tab_average = QWidget(self.tab_bar)
        tab_motion = QWidget(self.tab_bar)
        tab_gauss.setStyleSheet(self.style_sheet)
        tab_plateau.setStyleSheet(self.style_sheet)
        tab_average.setStyleSheet(self.style_sheet)
        tab_motion.setStyleSheet(self.style_sheet)

        self.tab_bar.addTab(tab_gauss, "Gaussian")
        self.tab_bar.addTab(tab_plateau, "Plateau")
        self.tab_bar.addTab(tab_average, "Average")
        self.tab_bar.addTab(tab_motion, "Motion")

        self.gauss_sigma1_edit = QLineEdit(tab_gauss)
        self.gauss_sigma2_edit = QLineEdit(tab_gauss)
        self.gauss_theta_edit = QLineEdit(tab_gauss)
        self.gauss_ksize_edit = QLineEdit(tab_gauss)

        self.plateau_sigma1_edit = QLineEdit(tab_plateau)
        self.plateau_sigma2_edit = QLineEdit(tab_plateau)
        self.plateau_theta_edit = QLineEdit(tab_plateau)
        self.plateau_ksize_edit = QLineEdit(tab_plateau)

        self.average_ksize_edit = QLineEdit(tab_average)

        self.motion_length_edit = QLineEdit(tab_motion)
        self.motion_theta_edit = QLineEdit(tab_motion)

        self.gauss_sigma1_edit.setGeometry(QRect(220, 20, 150, 70))
        self.gauss_sigma2_edit.setGeometry(QRect(220, 100, 150, 70))
        self.gauss_theta_edit.setGeometry(QRect(220, 180, 150, 70))
        self.gauss_ksize_edit.setGeometry(QRect(220, 260, 150, 70))

        self.plateau_sigma1_edit.setGeometry(QRect(220, 20, 150, 70))
        self.plateau_sigma2_edit.setGeometry(QRect(220, 100, 150, 70))
        self.plateau_theta_edit.setGeometry(QRect(220, 180, 150, 70))
        self.plateau_ksize_edit.setGeometry(QRect(220, 260, 150, 70))

        self.average_ksize_edit.setGeometry(QRect(220, 20, 150, 70))

        self.motion_length_edit.setGeometry(QRect(220, 20, 150, 70))
        self.motion_theta_edit.setGeometry(QRect(220, 100, 150, 70))

        self.gauss_sigma1_edit.setText("1.0")
        self.gauss_sigma2_edit.setText("1.0")
        self.gauss_theta_edit.setText("0.0")
        self.gauss_ksize_edit.setText("5")

        self.plateau_sigma1_edit.setText("1.0")
        self.plateau_sigma2_edit.setText("1.0")
        self.plateau_theta_edit.setText("0.0")
        self.plateau_ksize_edit.setText("5")

        self.average_ksize_edit.setText("5")

        self.motion_length_edit.setText("5")
        self.motion_theta_edit.setText("0.0")

        self.gauss_sigma1_edit.setStyleSheet("background:white")
        self.gauss_sigma2_edit.setStyleSheet("background:white")
        self.gauss_theta_edit.setStyleSheet("background:white")
        self.gauss_ksize_edit.setStyleSheet("background:white")

        self.plateau_sigma1_edit.setStyleSheet("background:white")
        self.plateau_sigma2_edit.setStyleSheet("background:white")
        self.plateau_theta_edit.setStyleSheet("background:white")
        self.plateau_ksize_edit.setStyleSheet("background:white")

        self.average_ksize_edit.setStyleSheet("background:white")

        self.motion_length_edit.setStyleSheet("background:white")
        self.motion_theta_edit.setStyleSheet("background:white")

        self.gauss_sigma1_text = QLabel(tab_gauss)
        self.gauss_sigma2_text = QLabel(tab_gauss)
        self.gauss_theta_text = QLabel(tab_gauss)
        self.gauss_ksize_text = QLabel(tab_gauss)
        self.plateau_sigma1_text = QLabel(tab_plateau)
        self.plateau_sigma2_text = QLabel(tab_plateau)
        self.plateau_theta_text = QLabel(tab_plateau)
        self.plateau_ksize_text = QLabel(tab_plateau)
        self.average_ksize_text = QLabel(tab_average)
        self.motion_length_text = QLabel(tab_motion)
        self.motion_theta_text = QLabel(tab_motion)

        self.gauss_sigma1_text.setGeometry(QRect(20, 20, 120, 50))
        self.gauss_sigma2_text.setGeometry(QRect(20, 100, 120, 50))
        self.gauss_theta_text.setGeometry(QRect(20, 180, 120, 50))
        self.gauss_ksize_text.setGeometry(QRect(20, 260, 120, 50))

        self.plateau_sigma1_text.setGeometry(QRect(20, 20, 120, 50))
        self.plateau_sigma2_text.setGeometry(QRect(20, 100, 120, 50))
        self.plateau_theta_text.setGeometry(QRect(20, 180, 120, 50))
        self.plateau_ksize_text.setGeometry(QRect(20, 260, 120, 50))

        self.average_ksize_text.setGeometry(QRect(20, 20, 120, 50))

        self.motion_length_text.setGeometry(QRect(20, 20, 120, 50))
        self.motion_theta_text.setGeometry(QRect(20, 100, 120, 50))

        self.gauss_sigma1_text.setText("Sigma1:")
        self.gauss_sigma2_text.setText("Sigma2:")
        self.gauss_theta_text.setText("Theta:")
        self.gauss_ksize_text.setText("Ksize:")

        self.plateau_sigma1_text.setText("Sigma1:")
        self.plateau_sigma2_text.setText("Sigma2:")
        self.plateau_theta_text.setText("Theta:")
        self.plateau_ksize_text.setText("Ksize:")

        self.average_ksize_text.setText("Ksize:")

        self.motion_length_text.setText("Length:")
        self.motion_theta_text.setText("Theta:")

        self.gauss_sigma1_text.setAlignment(Qt.AlignCenter)
        self.gauss_sigma2_text.setAlignment(Qt.AlignCenter)
        self.gauss_theta_text.setAlignment(Qt.AlignCenter)
        self.gauss_ksize_text.setAlignment(Qt.AlignCenter)

        self.plateau_sigma1_text.setAlignment(Qt.AlignCenter)
        self.plateau_sigma2_text.setAlignment(Qt.AlignCenter)
        self.plateau_theta_text.setAlignment(Qt.AlignCenter)
        self.plateau_ksize_text.setAlignment(Qt.AlignCenter)

        self.preview_btn = QPushButton(self.tab_bar)
        self.confirm_btn = QPushButton(self.tab_bar)
        self.preview_btn.setGeometry(QRect(20, 430, 180, 70))
        self.confirm_btn.setGeometry(QRect(300-90, 430, 180, 70))
        self.preview_btn.setText("Preview")
        self.confirm_btn.setText("Confirm")

        self.confirm_btn.clicked.connect(
            f_tool.partial(self.confirm_fcn_, True)
        )

        self.preview_btn.clicked.connect(
            f_tool.partial(self.confirm_fcn_, False)
        )

        self.gauss_info = dict(
            ksize=5,
            sigma1=1.0,
            sigma2=1.0,
            theta=0.0
        )

        self.plateau_info = dict(
            ksize=5,
            sigma1=1.0,
            sigma2=1.0,
            theta=0.0
        )

        self.average_info = dict(
            ksize=5
        )

        self.motion_info = dict(
            length=10,
            theta=0.0
        )

        self.emit_info = self.gauss_info

        self.gauss_sigma1_edit.editingFinished.connect(self.edit_gauss_sigma1_fcn_)
        self.gauss_sigma2_edit.editingFinished.connect(self.edit_gauss_sigma2_fcn_)
        self.gauss_theta_edit.editingFinished.connect(self.edit_gauss_theta_fcn_)
        self.gauss_ksize_edit.editingFinished.connect(self.edit_gauss_ksize_fcn_)

        self.plateau_sigma1_edit.editingFinished.connect(self.edit_plateau_sigma1_fcn_)
        self.plateau_sigma2_edit.editingFinished.connect(self.edit_plateau_sigma2_fcn_)
        self.plateau_theta_edit.editingFinished.connect(self.edit_plateau_theta_fcn_)
        self.plateau_ksize_edit.editingFinished.connect(self.edit_plateau_ksize_fcn_)

        self.average_ksize_edit.editingFinished.connect(self.edit_average_ksize_fcn_)

        self.motion_length_edit.editingFinished.connect(self.edit_motion_length_fcn_)
        self.motion_theta_edit.editingFinished.connect(self.edit_motion_theta_fcn_)

        self.psf_label = QLabel(self.tab_bar)
        self.psf_label.setGeometry(QRect(430, 50, 450, 450))
        self.psf_label.setStyleSheet("background:black")

        self.show()

    def input_check(self, tool_name, default_val, min_val, max_val, dtype):
        now_tool = self.__getattribute__(tool_name)
        try:
            now_val = float(now_tool.text())
        except:
            now_val = default_val
        now_val = np.round(np.minimum(np.maximum(now_val, min_val), max_val), dtype)
        if dtype == 0:
            now_tool.setText(str(int(now_val)))
        else:
            now_tool.setText(str(now_val))
        return now_val

    def edit_gauss_sigma1_fcn_(self):
        now_val = self.input_check("gauss_sigma1_edit", 1.0, 0.0, 1e12, 1)
        self.gauss_info['sigma1'] = now_val

    def edit_gauss_sigma2_fcn_(self):
        now_val = self.input_check("gauss_sigma2_edit", 1.0, 0.0, 1e12, 1)
        self.gauss_info['sigma2'] = now_val

    def edit_gauss_theta_fcn_(self):
        now_val = self.input_check("gauss_theta_edit", 0, 0.0, 360.0, 1)
        self.gauss_info['theta'] = now_val

    def edit_gauss_ksize_fcn_(self):
        now_val = self.input_check("gauss_ksize_edit", 3, 3, 100, 0)
        self.gauss_info['ksize'] = int(now_val)

    def edit_plateau_sigma1_fcn_(self):
        now_val = self.input_check("plateau_sigma1_edit", 1, 0.0, 1e12, 1)
        self.plateau_info['sigma1'] = now_val

    def edit_plateau_sigma2_fcn_(self):
        now_val = self.input_check("plateau_sigma2_edit", 1.0, 0.0, 1e12, 1)
        self.plateau_info['sigma2'] = now_val

    def edit_plateau_theta_fcn_(self):
        now_val = self.input_check("plateau_theta_edit", 0.0, 0.0, 360.0, 1)
        self.plateau_info['theta'] = now_val

    def edit_plateau_ksize_fcn_(self):
        now_val = self.input_check("plateau_ksize_edit", 3, 3, 100, 0)
        self.plateau_info['ksize'] = int(now_val)

    def edit_average_ksize_fcn_(self):
        now_val = self.input_check("average_ksize_edit", 3, 3, 100, 0)
        self.average_info['ksize'] = int(now_val)

    def edit_motion_length_fcn_(self):
        now_val = self.input_check("motion_length_edit", 1, 1, 100, 0)
        self.motion_info['length'] = int(now_val)

    def edit_motion_theta_fcn_(self):
        now_val = self.input_check("motion_theta_edit", 0.0, -360.0, 360.0, 1)
        self.motion_info['theta'] = now_val

    def confirm_fcn_(self, is_confirm):
        now_tab_id = self.tab_bar.currentIndex()
        if now_tab_id == 0:
            now_info = self.gauss_info
            now_kernel = gaussian_kernel(
                sigma1=now_info['sigma1'],
                sigma2=now_info['sigma2'],
                theta=now_info['theta'],
                ksize=now_info['ksize']
            )
        elif now_tab_id == 1:
            now_info = self.plateau_info
            now_kernel = plateau_kernel(
                sigma1=now_info['sigma1'],
                sigma2=now_info['sigma2'],
                theta=now_info['theta'],
                ksize=now_info['ksize']
            )
        elif now_tab_id == 2:
            ksize = self.average_info['ksize']
            now_kernel = np.ones((ksize, ksize)) / (ksize ** 2)
        else:
            now_info = self.motion_info
            now_kernel = motion_kernel(
                length=now_info['length'],
                theta=now_info['theta']
            )
        if now_tab_id != 2:
            now_max = np.max(now_kernel)
            now_min = np.min(now_kernel)
            show_kernel = (now_kernel - now_min) / (now_max - now_min)
            show_kernel = (show_kernel * 255).astype(np.uint8)
        else:
            show_kernel = (now_kernel * 255).astype(np.uint8)
        self.psf_label.clear()
        self.psf_label.setPixmap(
            QPixmap(
                QImage(
                    show_kernel.data,
                    show_kernel.shape[1],
                    show_kernel.shape[0],
                    show_kernel.shape[1],
                    QImage.Format.Format_Grayscale8
                )
            )
        )
        self.psf_label.setScaledContents(True)
        self.spatial_filter_signal_.emit(
            dict(
                kernel=now_kernel,
                confirmed=is_confirm
            )
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SpatialFilterWin()
    win.show()
    sys.exit(app.exec_())
