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
        # print(position_index)
        # 找对应的点坐标 - 左右各留20点冗余
        right = position_real[position_index[0]][0] - 100
        left = position_real[position_index[0] - 1][0] + 30
        #
        # print(left, right)
        # 1.2 裁剪img[:, n:m]
        needed_img = img_baked[:, left:right]
        return needed_img

    def remove_tiny_content(no_machine_img):
        return no_machine_img

    centre_img = remove_tiny_content(remove_machine())
    return centre_img


def get_point_position(washed_img) -> dict:
    # 1. 判断弯曲方向
    # 拿到max_y - 点的集合maxP & min_y - 点的集合minP
    print('--- washed_img ---')
    # print(washed_img)
    # 找到试样的所有点坐标
    item_collection_y = np.where(washed_img == 1)[0]
    item_collection_x = np.where(washed_img == 1)[1]

    # print(item_collection_y.tolist())
    # print(item_collection_x.tolist())

    # 取y值最大、最小的点坐标对应的x
    y_min_point = {'x': item_collection_x[0], 'y': item_collection_y[0]}
    y_max_point = {'x': item_collection_x[-1], 'y': item_collection_y[-1]}

    print(y_min_point['x'], y_max_point['x'])

    # 判断两个点，谁的x值距离图片中心点x最近，选出最近的那个点
    center_x = washed_img.shape[1] * 0.5
    print(center_x)
    if abs(y_min_point['x'] - center_x) < abs(y_max_point['x'] - center_x):
        pre_wanted_point = y_min_point
    else:
        pre_wanted_point = y_max_point

    print(pre_wanted_point)

    # pre_wanted_point为材料外侧点，需要找到与它x相同的，对应的内侧点
    same_x_position = np.where(item_collection_x == pre_wanted_point['x'])
    same_y_value = item_collection_y[same_x_position]
    if same_y_value[0] == pre_wanted_point['y']:
        wanted_y = same_y_value[-1]
    else:
        wanted_y = same_y_value[0]

    print(wanted_y)

    plt.imshow(washed_img)
    plt.show()
    return wanted_y


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
    get_point_position(data_wash(mpimg.imread('./ori_imgs/6.jpg')))
    # print(get_top_position(mpimg.imread('./ori_imgs/2.jpeg')))
