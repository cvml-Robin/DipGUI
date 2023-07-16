import cv2
import numpy as np
import matplotlib.pyplot as plt


def img_to_norm(img):
    max_val = img.max()
    nor_max_val = 1.0
    if max_val > 255:
        nor_max_val = 65535
    elif max_val > 1:
        nor_max_val = 255
    return img / nor_max_val


def normalize_img(img):
    max_val = np.max(img)
    min_val = np.min(img)
    return (img - min_val) / (max_val - min_val)


def position_prod(h=7, w=7, theta=0.0, sigma1=1.0, sigma2=1.0):
    theta = np.deg2rad(theta)
    x = np.linspace(1, w, w) - (w + 1) / 2
    y = np.linspace(1, h, h) - (h + 1) / 2
    mx, my = np.meshgrid(x, y)
    mx = np.reshape(mx, (1, h * w))
    my = np.reshape(my, (1, h * w))
    rot_mat = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    pos_mat = np.concatenate((mx, my), axis=0)
    sig_mat = np.array([[sigma1 ** 2, 0], [0, sigma2 ** 2]])
    rot_sig_mat = np.matmul(np.matmul(rot_mat.T, sig_mat), rot_mat)
    pos_prod = np.array(np.matmul(np.matrix(rot_sig_mat).I, pos_mat)) * pos_mat
    pos_prod = np.sum(pos_prod, axis=0)
    return pos_prod


def gaussian_kernel(sigma1=0.0, sigma2=0.0, ksize=7, theta=0.0, beta=1.0):
    pos_prod = position_prod(h=ksize, w=ksize, theta=theta, sigma2=sigma2, sigma1=sigma1)
    gauss_kernel_mat = np.exp(-np.power(pos_prod, beta)/2)
    gauss_kernel_mat = gauss_kernel_mat / np.sum(gauss_kernel_mat)
    return gauss_kernel_mat.reshape((ksize, ksize))


def plateau_kernel(sigma1=0.0, sigma2=0.0, ksize=7, theta=0.0, beta=1.0):
    pos_prod = position_prod(h=ksize, w=ksize, theta=theta, sigma2=sigma2, sigma1=sigma1)
    gauss_kernel_mat = 1 / (1 + pos_prod ** beta)
    gauss_kernel_mat = gauss_kernel_mat / np.sum(gauss_kernel_mat)
    return gauss_kernel_mat.reshape((ksize, ksize))


def motion_kernel(length=10, theta=0.0):
    vec0 = np.ones((1, length))
    kernel0 = np.zeros((length, length))
    kernel0[int(length/2), :] = np.ones((1, length))
    rot_mat = cv2.getRotationMatrix2D(
        scale=1,
        angle=theta,
        center=(length/2, length/2)
    )
    kernel = cv2.warpAffine(
        src=kernel0,
        M=rot_mat,
        dsize=(length, length),
        flags=cv2.INTER_CUBIC
    ).clip(0, 1)
    kernel = kernel / np.sum(kernel)
    return kernel


def add_noise_gauss(src_img=None, sigma=0.01):
    src_img = img_to_norm(src_img)
    noise_mat = np.random.normal(0, sigma ** 2, size=src_img.shape)
    noise_img = (src_img + noise_mat).clip(0, 1)
    return noise_img


def add_noise_salt_pepper(src_img=None, intensity=0.1):
    src_img = img_to_norm(src_img)
    if len(src_img.shape) > 2:
        sp_pos = np.random.uniform(0, 1, src_img[:, :, 0].shape)
    else:
        sp_pos = np.random.uniform(0, 1, src_img.shape)
    sp_zero = np.where(sp_pos < intensity/2, True, False)
    sp_one = np.where(np.abs(sp_pos - intensity*3/4) < intensity/4, True, False)
    src_copy = src_img.copy()
    if len(src_img.shape) > 2:
        src_copy[sp_zero, :] = 0
        src_copy[sp_one, :] = 1
    else:
        src_copy[sp_zero] = 0
        src_copy[sp_one] = 1
    return src_copy


def add_noise_poisson(src_img=None):
    src_img = img_to_norm(src_img)
    val = len(np.unique(src_img))
    vals = 2 ** np.ceil(np.log2(val))
    noise_img = np.random.poisson(lam=src_img * vals) / vals
    return noise_img.clip(0, 1)


if __name__ == '__main__':
    # kernel_gauss = gaussian_kernel(
    #     ksize=100,
    #     sigma1=10,
    #     sigma2=2,
    #     theta=20,
    #     beta=0.3
    # )
    #
    # kernel_plateau = gaussian_kernel(
    #     ksize=100,
    #     sigma1=10,
    #     sigma2=2,
    #     theta=20
    # )
    #
    # kernel_motion = motion_kernel(
    #     length=21,
    #     theta=-30
    # )
    # print(kernel_motion.shape)
    # plt.figure()
    # plt.imshow(kernel_motion, 'gray')
    # plt.show()

    src_img = cv2.imread("../img5.jpg")
    src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
    # src_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)

    # noise_img = add_noise_gauss(src_img=src_img, sigma=0.5)
    # noise_img = add_noise_salt_pepper(src_img=src_img, intensity=0.01)
    # noise_img = add_noise_poisson(src_img)
    #
    # plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.imshow(src_img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(noise_img, 'gray')
    # plt.show()

