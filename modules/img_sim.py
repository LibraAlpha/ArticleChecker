import hashlib
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
import cv2


def calculate_ssim(image1, image2):

    if image1 is None or image2 is None:
        print("无法读取图像")
        return

    # 检查图像尺寸是否小于7x7像素
    min_dim = min(image1.shape[:2])
    if min_dim < 7:
        # 将图像调整为至少7x7像素
        scale_factor = max(7 / min_dim, 1.0)
        image1 = cv2.resize(image1, None, fx=scale_factor, fy=scale_factor)
        image2 = cv2.resize(image2, None, fx=scale_factor, fy=scale_factor)

    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    ssim_score = compare_ssim(gray1, gray2)

    return ssim_score


def calculate_md5_with_path(image_path):
    md5_hash = hashlib.md5()

    with open(image_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    md5_value = md5_hash.hexdigest()
    return md5_value


def calculate_md5_with_file(image_file):
    md5_hash = hashlib.md5(image_file).hexdigest()
    return md5_hash


if __name__ == '__main__':
    image_path1 = "D:/img/a.jpg"
    image_path2 = "D:/img/b.jpg"
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)
    print(calculate_md5_with_path(image_path1), calculate_md5_with_path(image_path2))
    # print(calculate_ssim(image1, image2))
