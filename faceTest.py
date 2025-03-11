import cv2

# 读取图像
image = cv2.imread('ghy.jpg')

# 获取左上角像素
b, g, r = image[0, 0]  # OpenCV 默认是 BGR

print(f"BGR 格式: {b}, {g}, {r}")
