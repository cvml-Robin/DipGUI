from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
import rotate_win
import spatial_filter_win
from resize_win import ResizeWin
from edge_win import EdgeWin
from image_process.utils import normalize_img, add_noise_poisson, add_noise_salt_pepper, add_noise_gauss
from segment_thresh_adaptive_win import AdaptiveThreshWin
from segment_color import SegmentColorSpace
from segment_kmeans_win import SegmentKmeansWin
from image_info_win import ImageInfoWin
from morphology_win import MorphologyWin
from non_linear_trans_win import NonLinearTransformWin
from add_noise_win import AddNoiseWin
from functools import partial


class DipMainWin(QMainWindow):
    def __init__(self):
        super(DipMainWin, self).__init__(None)
        self.desktop = QApplication.desktop()
        self.setStyleSheet("font-size:12pt;font-weight:bold;font-family:Calibri")
        self.setWindowTitle("Digital Image Process By kyanko")
        self.desk_rect = self.desktop.screenGeometry()
        self.desk_height = self.desk_rect.height()
        self.desk_width = self.desk_rect.width()

        self.win_height = int(self.desk_height * 3 / 4)
        self.win_width = int(self.desk_width * 3 / 4)

        self.setFixedSize(self.win_width, self.win_height)

        self.menu_bar = self.menuBar()
        self.menu_file = self.menu_bar.addMenu("File")
        # self.menu_bar.setStyleSheet("font-size:12pt;font-weight:bold;font-family:Calibri")
        self.menu_file_open_image = self.menu_file.addAction("Open")
        self.menu_file_open_image.setShortcut('Ctrl+O')

        self.menu_file_save_image = self.menu_file.addAction("Save")
        self.menu_file_save_image.setShortcut('Ctrl+S')

        self.menu_file_info = self.menu_file.addAction("Info")

        self.menu_file_open_image.triggered.connect(self.open_image_)
        self.menu_file_save_image.triggered.connect(self.save_image_)
        self.menu_file_info.triggered.connect(self.check_file_info_)

        self.menu_edit = self.menu_bar.addMenu("Edit")
        self.menu_edit_undo = self.menu_edit.addAction("Undo")
        self.menu_edit_redo = self.menu_edit.addAction("Redo")
        self.menu_edit_undo.setShortcut("Ctrl+Z")
        self.menu_edit_redo.setShortcut("Ctrl+Y")
        self.menu_edit_undo.triggered.connect(self.edit_undo_fcn_)
        self.menu_edit_redo.triggered.connect(self.edit_redo_fcn_)

        self.menu_interp = self.menu_bar.addAction("Resize")
        self.menu_interp.triggered.connect(self.resize_fcn_)

        self.menu_filter = self.menu_bar.addMenu("Filter")
        self.menu_filter_space = self.menu_filter.addMenu("Space")
        self.menu_filter_space_blur = self.menu_filter_space.addAction("Blur")
        self.menu_filter_space_median = self.menu_filter_space.addAction("Median")
        self.menu_filter_space_blur.triggered.connect(self.spatial_blur_win_show_)
        self.menu_filter_space_median.triggered.connect(self.median_blur_fcn_)

        self.menu_filter_space_sharpen = self.menu_filter_space.addAction("Sharpen")
        self.menu_filter_space_noise = self.menu_filter_space.addAction("Add Noise")

        self.menu_filter_space_noise.triggered.connect(self.add_noise_win_show_)

        self.menu_transform = self.menu_bar.addMenu("Transform")
        self.menu_transform_geo = self.menu_transform.addMenu("Geometric")
        self.menu_transform_geo_rotate = self.menu_transform_geo.addAction("Rotate")
        self.menu_transform_color = self.menu_transform.addMenu("Color Space")

        self.menu_transform_color_gray = self.menu_transform_color.addAction("Gray")
        self.menu_transform_color_hsv = self.menu_transform_color.addAction("HSV")
        self.menu_transform_color_hsl = self.menu_transform_color.addAction("HSL")
        self.menu_transform_color_lab = self.menu_transform_color.addAction("LAB")
        self.menu_transform_color_ycbcr = self.menu_transform_color.addAction("YCbCr")

        self.menu_transform_nonlinear = self.menu_transform.addAction("Non Linear")
        self.menu_transform_nonlinear.triggered.connect(self.trans_non_linear_win_)

        self.menu_transform_color_gray.triggered.connect(
            partial(self.transform_color_space, "gray")
        )

        self.menu_transform_color_hsv.triggered.connect(
            partial(self.transform_color_space, "hsv")
        )

        self.menu_transform_color_hsl.triggered.connect(
            partial(self.transform_color_space, "hsl")
        )

        self.menu_transform_color_lab.triggered.connect(
            partial(self.transform_color_space, "lab")
        )

        self.menu_transform_color_ycbcr.triggered.connect(
            partial(self.transform_color_space, "ycbcr")
        )

        self.menu_transform_geo_rotate.triggered.connect(self.rotate_win_show_)

        self.menu_segment = self.menu_bar.addMenu("Segment")
        self.menu_segment_thresh = self.menu_segment.addMenu("Thresh")
        self.menu_segment_thresh_otsu = self.menu_segment_thresh.addAction("OTSU")
        self.menu_segment_thresh_adaptive = self.menu_segment_thresh.addAction("Adaptive")
        self.menu_segment_thresh_otsu.triggered.connect(self.segment_thresh_otsu_fcn_)
        self.menu_segment_thresh_adaptive.triggered.connect(self.segment_thresh_adaptive_win_)

        self.menu_segment_color = self.menu_segment.addAction("Color Space")
        self.menu_segment_color.triggered.connect(self.segment_color_space_win_)

        self.menu_segment_kmeans = self.menu_segment.addAction("K-Means")
        self.menu_segment_kmeans.triggered.connect(self.segment_kmeans_win_)

        self.menu_edge = self.menu_bar.addAction("Edge")
        self.menu_edge.triggered.connect(self.edge_win_show_)

        self.menu_trans_fft = self.menu_transform.addAction("FFT")
        self.menu_trans_fft.triggered.connect(self.show_fft_)

        self.menu_morphology = self.menu_bar.addAction("Morphology")
        self.menu_morphology.triggered.connect(self.morphology_win_)

        self.src_img_label = QLabel(self)
        self.src_img_label.setGeometry(QRect(20, 50, 500, 500))
        self.src_img_label.setStyleSheet("background:black")

        self.prs_img_label = QLabel(self)
        self.prs_img_label.setGeometry(QRect(550, 50, 500, 500))
        self.prs_img_label.setStyleSheet("background:black")

        self.show()
        self.prs_img = []
        self.prs_id = -1
        self.src_img = 0
        self.now_img = 0
        self.src_width = 0
        self.src_height = 0
        self.src_file_path = ""
        self.src_file_name = ""
        self.src_fig = plt.figure()
        self.prs_fig = plt.figure()
        self.fft_fig = plt.figure()
        self.ele_fig = plt.figure()

        self.src_fig.canvas.manager.window.setWindowTitle("Source Image")
        self.prs_fig.canvas.manager.window.setWindowTitle("Current Output Image")
        self.fft_fig.canvas.manager.window.setWindowTitle("Image FFT")
        self.ele_fig.canvas.manager.window.setWindowTitle("Morphology Element")

        self.menu_file_save_image.setEnabled(False)
        self.menu_file_info.setEnabled(False)
        self.menu_edit.setEnabled(False)
        self.menu_interp.setEnabled(False)
        self.menu_transform.setEnabled(False)
        self.menu_segment.setEnabled(False)
        self.menu_filter.setEnabled(False)
        self.menu_edge.setEnabled(False)
        self.menu_morphology.setEnabled(False)

    def src_img_label_press_fcn_(self, e):
        if e.buttons() == Qt.LeftButton:
            self.src_fig.gca().imshow(self.src_img)
            self.src_fig.canvas.draw()
            self.src_fig.canvas.flush_events()
            self.src_fig.show()

    def prs_img_label_press_fcn_(self, e):
        if e.buttons() == Qt.LeftButton:

            self.prs_fig.gca().cla()
            self.prs_fig.gca().imshow(self.prs_img[self.prs_id])
            self.prs_fig.canvas.draw()
            self.prs_fig.canvas.flush_events()
            self.prs_fig.show()

    def open_image_(self):
        file_path, file_name = QFileDialog.getOpenFileNames(
            self, "选取文件", "./", "(*jpg *bmp *png)"
        )
        if len(file_path) != 0:
            self.src_file_path = file_path[0]
            self.src_file_name = file_name
            src_img = cv2.imread(file_path[0])
            src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
            h, w, _ = src_img.shape
            self.src_height = h
            self.src_width = w
            desk_hw_ratio = self.desk_height / self.desk_width
            hw_ratio = h / w
            if hw_ratio > desk_hw_ratio:
                label_h = (self.desk_height * 0.75) - 80
                label_w = int(label_h / hw_ratio)
                label_h = int(label_h)
            else:
                label_w = (self.desk_width * 0.75 - 20) / 2
                label_h = int(label_w * hw_ratio)
                label_w = int(label_w)
            self.win_width = label_w * 2 + 30
            self.win_height = label_h + 60
            self.setFixedSize(self.win_width, self.win_height)
            self.move(
                int(self.desk_width / 2 - self.win_width / 2),
                int(self.desk_height / 2 - self.win_height / 2)
            )
            self.src_img_label.setGeometry(QRect(10, 40, label_w, label_h))
            self.prs_img_label.setGeometry(QRect(10 + label_w + 10, 40, label_w, label_h))
            self.src_img = src_img
            self.src_img_label.setPixmap(
                QPixmap(
                    QImage(
                        src_img.data,
                        src_img.shape[1],
                        src_img.shape[0],
                        src_img.shape[1] * 3,
                        QImage.Format_RGB888
                    )
                )
            )
            self.src_img_label.setScaledContents(True)
            self.prs_img_label.clear()
            self.menu_file_save_image.setEnabled(True)
            self.menu_file_info.setEnabled(True)
            self.menu_edit.setEnabled(True)
            self.menu_interp.setEnabled(True)
            self.menu_transform.setEnabled(True)
            self.menu_segment.setEnabled(True)
            self.menu_filter.setEnabled(True)
            self.menu_edge.setEnabled(True)
            self.menu_morphology.setEnabled(True)
            self.src_img_label.mouseDoubleClickEvent = self.src_img_label_press_fcn_
            self.prs_img_label.mouseDoubleClickEvent = self.prs_img_label_press_fcn_
            self.prs_id = -1
            self.prs_img = []
            self.show_prs_image_(now_img=self.src_img, append_prs=True)
            # self.prs_img.append(self.src_img)
            # self.prs_id += 1

    def save_image_(self):
        save_file_path, save_file_type = QFileDialog.getSaveFileName(
            self,
            "Save Current Image",
            './',
            "jpg(*.jpg);;png(*.png);;bmp(*.bmp)"
        )
        if len(save_file_path) > 0:
            prs_img = self.prs_img[self.prs_id]
            cv2.imwrite(
                save_file_path,
                prs_img[:, :, [2, 1, 0]]
            )

    def check_file_info_(self):
        self.info_win = ImageInfoWin(
            src_img=self.src_img,
            file_path=self.src_file_path
        )
        self.info_win.show()

    def edit_undo_fcn_(self):
        now_id = self.prs_id
        self.prs_id = self.prs_id - 1
        self.prs_id = max(0, self.prs_id)
        if self.prs_id != now_id:
            self.show_prs_image_(self.prs_img[self.prs_id], append_prs=False)

    def edit_redo_fcn_(self):
        now_id = self.prs_id
        self.prs_id = self.prs_id + 1
        self.prs_id = min(len(self.prs_img)-1, self.prs_id)
        if now_id != self.prs_id:
            self.show_prs_image_(self.prs_img[self.prs_id], append_prs=False)

    def resize_fcn_(self):
        self.resize_win = ResizeWin()
        self.resize_win.show()
        self.resize_win.change_size_signal_.connect(self.resize_fcn_emit_)

    def resize_fcn_emit_(self, new_size):
        resize_img = cv2.resize(
            src=self.prs_img[self.prs_id],
            dsize=(new_size[1], new_size[0]),
            interpolation=new_size[2]
        )
        self.show_prs_image_(resize_img, new_size[3])
        QApplication.processEvents()

    def spatial_blur_win_show_(self):
        self.spatial_blur_win = spatial_filter_win.SpatialFilterWin()
        self.spatial_blur_win.show()
        self.spatial_blur_win.spatial_filter_signal_.connect(self.spatial_blur_fcn_)

    def spatial_blur_fcn_(self, blur_kernel):
        blur_img = cv2.filter2D(
            src=self.prs_img[self.prs_id],
            ddepth=-1,
            kernel=blur_kernel['kernel']
        )
        self.show_prs_image_(now_img=blur_img, append_prs=blur_kernel['confirmed'])

    def median_blur_fcn_(self):
        median_img = cv2.medianBlur(
            src=self.prs_img[self.prs_id],
            ksize=3
        )
        self.show_prs_image_(median_img, True)

    def add_noise_win_show_(self):
        self.add_noise_win = AddNoiseWin()
        self.add_noise_win.show()
        self.add_noise_win.add_noise_signal_.connect(self.add_noise_fcn_)

    def add_noise_fcn_(self, noise_info):
        if noise_info['type'] == 'gauss':
            noise_img = add_noise_gauss(
                src_img=self.prs_img[self.prs_id],
                sigma=noise_info['sigma']
            )
        elif noise_info['type'] == 'sp':
            noise_img = add_noise_salt_pepper(
                src_img=self.prs_img[self.prs_id],
                intensity=noise_info['intensity']
            )
        else:
            noise_img = add_noise_poisson(self.prs_img[self.prs_id])
        noise_img = (noise_img * 255).astype(np.uint8)
        self.show_prs_image_(
            now_img=noise_img,
            append_prs=noise_info['is_confirm']
        )

    def rotate_win_show_(self):
        self.rot_win = rotate_win.ImageRotateWin()
        self.rot_win.show()
        self.rot_win.change_deg_signal_.connect(self.rotate_img_fcn_)

    def rotate_img_fcn_(self, now_deg):
        src_img = self.prs_img[self.prs_id]
        rot_mat = cv2.getRotationMatrix2D(
            center=(src_img.shape[1] / 2, src_img.shape[0] / 2),
            angle=now_deg['angle'],
            scale=1
        )
        rot_img = cv2.warpAffine(
            src=src_img,
            M=rot_mat,
            dsize=(src_img.shape[1], src_img.shape[0]),
            flags=cv2.INTER_CUBIC
        )
        self.show_prs_image_(now_img=rot_img, append_prs=now_deg['is_confirm'])
        QApplication.processEvents()

    def edge_win_show_(self):
        self.edge_win = EdgeWin()
        self.edge_win.show()
        self.edge_win.edge_signal_.connect(self.edge_detection_fcn_)

    def edge_detection_fcn_(self, edge_info):
        edge_img = cv2.Canny(
            image=self.prs_img[self.prs_id],
            threshold1=edge_info[0],
            threshold2=edge_info[1],
            apertureSize=edge_info[2],
            L2gradient=True
        )
        edge_img = np.dstack((edge_img, edge_img, edge_img))
        self.show_prs_image_(edge_img, append_prs=edge_info[3])

    def show_fft_(self):
        gray_img = cv2.cvtColor(self.prs_img[self.prs_id], cv2.COLOR_RGB2GRAY)
        gray_img = (gray_img / 255)
        fft_img = np.fft.fft2(gray_img)
        fft_img = np.fft.fftshift(fft_img)
        amp_img = np.log10(np.abs(fft_img)+1)
        ang_img = np.angle(fft_img)
        real_img = np.real(fft_img)
        imag_img = np.imag(fft_img)

        real_img = np.log10(real_img - np.min(real_img) + 1)
        imag_img = np.log10(imag_img - np.min(imag_img) + 1)
        amp_img = normalize_img(amp_img)
        ang_img = normalize_img(ang_img)
        real_img = normalize_img(real_img)
        imag_img = normalize_img(imag_img)

        self.fft_fig.add_subplot(2, 2, 1)
        self.fft_fig.gca().imshow(amp_img, 'gray')
        plt.title("|F{I}|")
        plt.axis("off")

        self.fft_fig.add_subplot(2, 2, 2)
        self.fft_fig.gca().imshow(ang_img, 'gray')
        plt.title("Phase(F{I})")
        plt.axis("off")

        self.fft_fig.add_subplot(2, 2, 3)
        self.fft_fig.gca().imshow(real_img, 'gray')
        plt.title("Real(F{I})")
        plt.axis("off")

        self.fft_fig.add_subplot(2, 2, 4)
        self.fft_fig.gca().imshow(imag_img, 'gray')
        plt.title("Imag(F{I})")
        plt.axis("off")
        self.fft_fig.show()

    def segment_thresh_otsu_fcn_(self):
        gray_img = cv2.cvtColor(self.prs_img[self.prs_id], cv2.COLOR_RGB2GRAY)
        _, bw_img = cv2.threshold(
            src=gray_img,
            maxval=255,
            type=cv2.THRESH_OTSU,
            thresh=None
        )
        bw_img = np.dstack((bw_img, bw_img, bw_img))
        self.show_prs_image_(bw_img, append_prs=True)

    def segment_thresh_adaptive_win_(self):
        self.adaptive_thresh_win = AdaptiveThreshWin()
        self.adaptive_thresh_win.show()
        self.adaptive_thresh_win.adaptive_thresh_signal_.connect(
            self.segment_thresh_adaptive_fcn_
        )

    def segment_thresh_adaptive_fcn_(self, thresh_info):
        gray_img = cv2.cvtColor(self.prs_img[self.prs_id], cv2.COLOR_RGB2GRAY)
        bw_img = cv2.adaptiveThreshold(
            src=gray_img,
            blockSize=thresh_info['ksize'],
            C=thresh_info['C'],
            adaptiveMethod=thresh_info['method'],
            thresholdType=thresh_info['type'],
            maxValue=255
        )
        bw_img = np.dstack((bw_img, bw_img, bw_img))
        self.show_prs_image_(bw_img, thresh_info['is_confirm'])

    def segment_color_space_win_(self):
        self.color_space_win = SegmentColorSpace()
        self.color_space_win.show()
        self.color_space_win.preview_signal_.connect(self.segment_color_space_fcn_)

    def segment_color_space_fcn_(self, emit_info):
        src_img = self.prs_img[self.prs_id]
        color_img = src_img
        if emit_info['color_space'] == "hsv":
            color_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2HSV)
        elif emit_info['color_space'] == "hsl":
            color_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2HLS)
            color_img = color_img[:, :, [0, 2, 1]]
        elif emit_info['color_space'] == "lab":
            color_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2LAB)
        elif emit_info['color_space'] == "ybr":
            color_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2YCrCb)
            color_img = color_img[:, :, [0, 2, 1]]
        color_img = color_img.astype(np.float32)
        color1 = color_img[:, :, 0]
        color2 = color_img[:, :, 1]
        color3 = color_img[:, :, 2]
        now_th = emit_info['th']
        bool1 = (color1 >= now_th[0]) * (color1 <= now_th[1])
        bool2 = (color2 >= now_th[2]) * (color2 <= now_th[3])
        bool3 = (color3 >= now_th[4]) * (color3 <= now_th[5])
        mask = bool1 * bool2 * bool3
        mask = ~mask
        masked_img = src_img.copy()
        masked_img[mask, :] = 0
        masked_img = masked_img.astype(np.uint8)
        self.show_prs_image_(masked_img, emit_info['is_confirm'])

    def segment_kmeans_win_(self):
        self.seg_kmeans_win = SegmentKmeansWin()
        self.seg_kmeans_win.show()
        self.seg_kmeans_win.segment_kmeans_signal_.connect(self.segment_kmeans_fcn_)

    def segment_kmeans_fcn_(self, kmeans_info):
        k = kmeans_info['k']
        best_label = kmeans_info['label']
        temp_img = self.prs_img[self.prs_id]
        temp_gray = cv2.cvtColor(temp_img, cv2.COLOR_RGB2GRAY)
        gray_vec = np.reshape(
            (temp_gray/255).astype(np.float32),
            (temp_gray.shape[0] * temp_gray.shape[1], 1)
        )
        _, label_mat, _ = cv2.kmeans(
            data=gray_vec,
            K=k,
            bestLabels=None,
            criteria=(cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 10, 1),
            attempts=10,
            flags=cv2.KMEANS_RANDOM_CENTERS
        )
        label_mat = (label_mat.astype(np.float32)).reshape(
            (temp_gray.shape[0], temp_gray.shape[1])
        )
        if best_label == 0:
            k_img = (label_mat * 255 / (k - 1))
            sv_img = np.ones_like(temp_gray) * 255
            k_img = np.dstack((k_img, sv_img, sv_img)).astype(np.uint8)
            k_img = cv2.cvtColor(k_img, cv2.COLOR_HSV2RGB)
        else:
            k_img = np.where(label_mat == (best_label - 1), 255, 0).astype(np.uint8)
            k_img = np.dstack((k_img, k_img, k_img))
        self.show_prs_image_(
            now_img=k_img,
            append_prs=kmeans_info['is_confirm']
        )

    def transform_color_space(self, target_space="gray"):
        target_id = dict(
            gray=cv2.COLOR_RGB2GRAY,
            hsv=cv2.COLOR_RGB2HSV,
            hsl=cv2.COLOR_RGB2HLS,
            lab=cv2.COLOR_RGB2LAB,
            ycbcr=cv2.COLOR_RGB2YCrCb
        )
        trans_color_img = cv2.cvtColor(
            self.prs_img[self.prs_id],
            target_id[target_space]
        )
        if target_space == "gray":
            trans_color_img = np.dstack((trans_color_img, trans_color_img, trans_color_img))
        self.show_prs_image_(now_img=trans_color_img, append_prs=True)

    def trans_non_linear_win_(self):
        self.non_linear_win = NonLinearTransformWin()
        self.non_linear_win.show()
        self.non_linear_win.non_linear_trans_signal_.connect(self.trans_nonlinear_fcn_)

    def trans_nonlinear_fcn_(self, trans_info):
        coe0 = trans_info['coe']
        gamma0 = trans_info['gamma']
        const0 = trans_info['const']
        temp_float_img = (self.prs_img[self.prs_id] / 255)
        temp_float_img = coe0 * (temp_float_img ** gamma0) + const0
        temp_float_img = (np.clip(temp_float_img, 0, 1) * 255).astype(np.uint8)
        self.show_prs_image_(
            now_img=temp_float_img,
            append_prs=trans_info['is_confirm']
        )

    def morphology_win_(self):
        self.morph_win = MorphologyWin()
        self.morph_win.show()
        self.morph_win.morph_signal_.connect(self.do_morphology_image_)

    def do_morphology_image_(self, morph_info):
        process_bar = QProgressBar()
        process_bar.setWindowTitle("Processing")
        process_bar.setStyleSheet("font-size:14pt")
        process_bar.setGeometry(QRect(960 - 250, 540 - 15, 500, 30))
        process_bar.setMaximum(100)
        process_bar.show()
        process_bar.setValue(0)
        QApplication.processEvents()
        if morph_info['use_more']:
            struct_element = morph_info['struct_element']
        else:
            struct_element = cv2.getStructuringElement(
                ksize=(morph_info['h'], morph_info['w']),
                shape=morph_info['shape'],
            )
        process_bar.setValue(30)
        QApplication.processEvents()
        if morph_info['type'] == 7:
            temp_gray = cv2.cvtColor(self.prs_img[self.prs_id], cv2.COLOR_RGB2GRAY)
            morph_img = cv2.morphologyEx(
                src=temp_gray,
                kernel=struct_element,
                op=morph_info['type'],
                anchor=(morph_info['ay'], morph_info['ax'])
            )
            morph_img = np.dstack((morph_img, morph_img, morph_img))
        else:
            morph_img = cv2.morphologyEx(
                src=self.prs_img[self.prs_id],
                kernel=struct_element,
                op=morph_info['type'],
                anchor=(morph_info['ay'], morph_info['ax'])
            )
        process_bar.setValue(60)
        QApplication.processEvents()
        self.show_prs_image_(
            now_img=morph_img,
            append_prs=morph_info['is_confirm']
        )
        if morph_info['show_element']:
            self.ele_fig.gca().imshow(struct_element.astype(np.float32), 'gray')
            self.ele_fig.canvas.draw()
            self.ele_fig.canvas.flush_events()
            self.ele_fig.show()
        process_bar.setValue(100)
        QApplication.processEvents()
        process_bar.close()
        QApplication.processEvents()

    def show_prs_image_(self, now_img=None, append_prs=False):
        self.prs_img_label.setPixmap(
            QPixmap(
                QImage(
                    now_img.data,
                    now_img.shape[1],
                    now_img.shape[0],
                    now_img.shape[1] * 3,
                    QImage.Format_RGB888
                )
            )
        )
        self.prs_img_label.setScaledContents(True)
        if append_prs:
            if len(self.prs_img) > self.prs_id + 1:
                self.prs_img[self.prs_id+1] = now_img
            else:
                self.prs_img.append(now_img)
            self.prs_id += 1
            if self.prs_id + 1 < len(self.prs_img):
                self.prs_img = self.prs_img[0:(self.prs_id + 1)]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = DipMainWin()
    ui.show()
    sys.exit(app.exec_())
