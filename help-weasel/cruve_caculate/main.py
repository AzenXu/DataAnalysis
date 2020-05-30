import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def test_img():
    img = mpimg.imread('./ori_imgs/1.jpeg') # (1040, 1392, 3)
    print(img.shape)

    new_img = img[:, 300:1100, :].copy()  # 裁剪图片到中心区域
    new_img_bake = np.where(new_img > 50, 255, 0)

    # print(new_img_bake)
    plt.imshow(new_img_bake)
    plt.show()

    positions = np.where(new_img_bake == [255, 255, 255])
    print(positions)


if __name__ == '__main__':
    test_img()
