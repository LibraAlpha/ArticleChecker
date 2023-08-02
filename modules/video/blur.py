import cv2


def gaussian_blur(image, kernel_size, sigma):
    # 使用高斯核对图像进行模糊处理
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


# 读取图像
image = cv2.imread('D:/20230721-171903.jpg')

# 设置高斯核大小和标准差
kernel_size = 0
sigma = 30

# 进行高斯模糊
blurred_image = gaussian_blur(image, kernel_size, sigma)

width, height = 1280, 640
resized_image = cv2.resize(blurred_image, (width, height))

# 显示原始图像和模糊后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
