import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# np.set_printoptions(threshold=np.nan)
import pandas as pd


def data_wash(img):
    # print(img)
    print(img)
    # 0. 三维数组二维化
    # test = [[[0,0,0], [255,255,255], [50,50,50]],
    #         [[0, 0, 0], [255, 255, 255], [50, 50, 50]],
    #         [[0, 0, 0], [255, 255, 255], [50, 50, 50]]
    #         ]
    def remove_machine():
        # 1. 清洗左右两侧夹机
        img_baked = np.where(img > 50, 1, np.nan)
        # 1.1 找到左右裁剪
        # 拿到最后一行点
        img_row_one = img_baked[-1]
        # 拿到白点的x值，去重
        position_real = np.unique(np.where(img_row_one == 1))
        # 实现list的shift()操作
        position_tmp = np.insert(position_real, 0, 0)[:-1]
        # 取差值最大的下标
        position_minus = position_real - position_tmp
        position_index = np.where(position_minus == position_minus.max())
        print(position_index)
        # 找对应的点坐标 - 左右各留20点冗余
        right = position_real[position_index[0]][0] - 20
        left = position_real[position_index[0] - 1][0] + 20
        #
        print(left, right)
        # 1.2 裁剪img[:, n:m, :]
        needed_img = img_baked[:, left:right]
        return needed_img
    centre_img = remove_machine()
    plt.subplot()
    plt.imshow(centre_img)
    plt.show()

    # point = img[0][0].mean()
    # print(point, type(point))

    pass


def get_top_position(img) -> int:
    # print(img.shape)

    new_img = img[:, 500:1100, :].copy()  # 裁剪图片到中心区域
    new_img_bake = np.where(new_img > 0, 1, np.nan)
    positions = np.where(new_img_bake == [255, 255, 255])

    # print(new_img_bake)
    # plt.imshow(new_img_bake)
    # plt.show()

    # df = pd.DataFrame(positions[1], index=positions[0])
    # print(df.head(300))
    # print(positions[0][0])
    return positions[0][0]


if __name__ == '__main__':
    data_wash(mpimg.imread('./ori_imgs/4.jpg'))
    # print(get_top_position(mpimg.imread('./ori_imgs/2.jpeg')))
