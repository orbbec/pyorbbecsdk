import cv2
import numpy as np
import os


def check_stripe_pattern(image, orientation='horizontal'):
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 计算灰度图像的傅里叶变换
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    # 计算幅度谱
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    # 检查是否存在条纹模式
    mean = 0
    if orientation == 'horizontal':
        mean = np.mean(magnitude_spectrum, axis=0).var()
    elif orientation == 'vertical':
        mean = np.mean(magnitude_spectrum, axis=1).var()
    print("stripe pattern: ", mean)


def check_color(image, lower_bound, upper_bound):
    # 将图像从BGR转换为HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 定义在HSV空间中紫色和绿色的范围
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    # 计算图像中特定颜色的像素占总像素的比例
    ratio = cv2.countNonZero(mask) / (image.size / 3)
    print("color ratio: ", ratio)
    return ratio > 0.6


def check_over_exposure(image):
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 计算图像中过曝的像素占总像素的比例
    ratio = np.sum(gray > 200) / gray.size
    print("exposure ratio: ", ratio)
    return ratio > 0.6


def check_image(image):
    # 定义紫色和绿色的范围
    purple_lower = np.array([120, 50, 50])
    purple_upper = np.array([160, 255, 255])
    green_lower = np.array([35, 50, 50])
    green_upper = np.array([85, 255, 255])
    # 检查图像
    check_color(image, purple_lower, purple_upper)
    check_color(image, green_lower, green_upper)
    check_stripe_pattern(image, 'horizontal')
    check_stripe_pattern(image, 'vertical')
    check_over_exposure(image)


def main():
    bad_image_dir = '/home/toosimple/Pictures/bad_images/'
    for image_name in os.listdir(bad_image_dir):
        image = cv2.imread(bad_image_dir + image_name)
        print("check image: ", image_name)
        check_image(image)


if __name__ == '__main__':
    main()
