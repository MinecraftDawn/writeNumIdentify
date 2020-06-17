import cv2 as cv
import numpy as np
from skimage.measure import block_reduce


def readImg(name: str):
    img = cv.imread(name, cv.IMREAD_GRAYSCALE)

    # 原始圖膨脹
    kernel = np.ones((3, 3))
    img = cv.erode(img, kernel, iterations = 5)
    cv.imwrite("FirstErod.png", img)

    for x1 in range(img.shape[0]):
        if np.count_nonzero(img[x1, :] < 50) != 0:
            break
    for x2 in range(img.shape[0] - 1, x1, -1):
        if np.count_nonzero(img[x2, :] < 50) != 0:
            break
    for y1 in range(img.shape[1]):
        if np.count_nonzero(img[:, y1] < 50) != 0:
            break
    for y2 in range(img.shape[1] - 1, y1, -1):
        if np.count_nonzero(img[:, y2] < 50) != 0:
            break

    deltaX = x2 - x1
    deltaY = y2 - y1
    edge = max(deltaX, deltaY)


    # 設定一個大小為100的邊框，並將資料填補到中間
    ones = np.ones((edge + 100, edge + 100)) * 255

    # ones[(edge-deltaX)//2:(edge+deltaX)//2,
    # (edge-deltaY)//2:(edge+deltaY)//2] = img[x1:x2, y1:y2]

    ones[2 + (edge - deltaX):2 + deltaX + (edge - deltaX),
    2 + (edge - deltaY):2 + deltaY + (edge - deltaY)] = img[x1:x2, y1:y2]
    cv.imwrite("Shrink.png", ones)

    print(edge)

    # # 模糊處理 平均濾波
    # for _ in range(3):
    #     ones = cv.blur(ones, (5,5))
    # cv.imwrite("blur.png", ones)


    # min pooling
    while ones.shape[0] >= 200:
        ones = block_reduce(ones, (2, 2), np.mean)

    # 去除黑邊
    ones[:, -1] = np.ones((1, ones.shape[0])) *255
    ones[-1, :] = np.ones((1,ones.shape[1])) * 255
    print(ones[:, -1].shape, ones[-1,:].shape)
    cv.imwrite("MeanPool.png", ones)

    # 膨脹
    kernel = np.ones((5, 5))
    ones = cv.erode(ones, kernel, 1)

    # resize
    ones = cv.resize(ones, (28, 28))

    for endX in range(ones.shape[0] - 1, 0, -1):
        if np.count_nonzero(ones[endX, :] < 50) != 0:
            break

    for endY in range(ones.shape[1] - 1, 0, -1):
        if np.count_nonzero(ones[:, endY] < 50) != 0:
            break

    cv.imwrite("Resize.png", ones)

    # 將圖片位移到中間
    ones = np.concatenate((ones[:, :endX + (27 - endX) // 2], ones[:, endX + (27 - endX) // 2:]), axis=1)
    ones = np.concatenate((ones[endY + (27 - endY) // 2:, :], ones[:endY + (27 - endY) // 2, :]), axis=0)
    print(endX, endY)

    cv.imwrite("Center.png", ones)

    print(ones)

    # 反白
    ones = 255 - ones

    cv.imwrite("HighLight.png", ones)

    # 收縮
    kernel = np.ones((2, 2))
    ones = cv.dilate(ones, kernel, 1)
    cv.imwrite("Dilate.png", ones)

    # 模糊處理 平均濾波
    ones = cv.blur(ones, (2, 2))
    cv.imwrite("Blur.png", ones)

    ones /= 255

    return ones
