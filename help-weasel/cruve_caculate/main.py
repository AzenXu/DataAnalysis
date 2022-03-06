import matplotlib.image as mpimg
import numpy as np
import pandas as pd


def data_wash(img):

    def remove_machine():
        # 0. 三维数组二维化
        # test = [[[0,0,0], [255,255,255], [50,50,50]],
        #         [[0, 0, 0], [255, 255, 255], [50, 50, 50]],
        #         [[0, 0, 0], [255, 255, 255], [50, 50, 50]]
        #         ]

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

        # 找对应的点坐标 - 左右各留一些点的冗余
        right = position_real[position_index[0]][0] - 120
        left = position_real[position_index[0] - 1][0] + 100

        # 1.2 裁剪img[:, n:m]
        needed_img = img_baked[:, left:right]
        return needed_img

    def remove_flying_content(no_machine_img):
        """
        干掉「飞点」
        # 1.判断飞点
        1. 拿到白点们的坐标List
        2. 逐y值，找横向飞点：
            1. 判断x+1,x+2,x+3,x+4,x-1,x-2,x-3,x-4有几个在list中
            2. 如果数量<5，则认为是「飞点」
            3. 把(x, y)放入横向飞点list中
        3. 逐x值，纵向飞点：
            1. 判断y+1,y+2,y+3,y+4,y-1,y-2,y-3,y-4有几个在list中
            2. 如果数量<5，则认为是「飞点」
            3. 把(x, y)放入纵向飞点list中
        # 2.即是横向飞点，又是纵向飞点的点，是真正的飞点。
        # 拿到真正飞点坐标list，逐个把其值置换为NaN
        """
        white_points_y, white_points_x = np.where(no_machine_img == 1)

        def find_fly_points_hor() -> list:
            fly_points_hor = []
            for i in range(len(white_points_y)):
                y = white_points_y[i]
                x = white_points_x[i]

                # 左右各4个点内，y相同的点的数量
                count = 0
                # --- 处理边界值 ---
                left = -4
                right = 5
                if i < 4:
                    left = 0
                if i > len(white_points_y) - 5:
                    right = len(white_points_y) - i
                # --- 正式逻辑 ---
                for inner_i in range(left, right):
                    inner_y = white_points_y[i + inner_i]
                    if inner_y == y:
                        count += 1
                if count < 4:
                    fly_points_hor.append((x, y))

            return fly_points_hor

        def find_fly_points_ver() -> list:
            fly_points_ver = []
            for i in range(len(white_points_x)):
                x = white_points_x[i]
                y = white_points_y[i]

                # 上下4个点内，x相同的点的数量 - 由于一些异形样，需调整为上下10
                x_positions = np.where(white_points_x == x)[0]
                # 用position们去y_list中找y们
                y_count = 0
                for j in range(len(x_positions)):
                    x_index = x_positions[j]
                    tmp_y = white_points_y[x_index]
                    if abs(tmp_y - y) < 10:
                        y_count += 1
                if y_count <= 10:
                    fly_points_ver.append((x, y))

            return fly_points_ver

        def remove_fly_points(fly_points) -> np.ndarray:
            for point in fly_points:
                point_x, point_y = point
                no_machine_img[point_y][point_x] = np.nan
            return no_machine_img

        remove_fly_points(find_fly_points_ver())
        no_flying_points = remove_fly_points(find_fly_points_hor())

        return no_flying_points

    washed_img = remove_flying_content(remove_machine())
    return washed_img


def get_point_position(washed_img) -> dict:
    # 1. 判断弯曲方向
    # 拿到max_y - 点的集合maxP & min_y - 点的集合minP
    # print('--- washed_img ---')
    # print(washed_img)
    # 找到试样的所有点坐标
    item_collection_y = np.where(washed_img == 1)[0]
    item_collection_x = np.where(washed_img == 1)[1]

    # print(item_collection_y.tolist())
    # print(item_collection_x.tolist())

    # 取y值最大、最小的点坐标对应的x
    y_min_point = {'x': item_collection_x[0], 'y': item_collection_y[0]}
    y_max_point = {'x': item_collection_x[-1], 'y': item_collection_y[-1]}

    # 判断两个点，谁的x值距离图片中心点x最近，选出最近的那个点
    center_x = washed_img.shape[1] * 0.5
    # print(center_x)
    if abs(y_min_point['x'] - center_x) < abs(y_max_point['x'] - center_x):
        pre_wanted_point = y_min_point
    else:
        pre_wanted_point = y_max_point

    # pre_wanted_point为材料外侧点，需要找到与它x相同的，对应的内侧点
    def get_inner_point():
        same_x_position = np.where(item_collection_x == pre_wanted_point['x'])
        same_y_value = item_collection_y[same_x_position]
        if same_y_value[0] == pre_wanted_point['y']:
            wanted_y = same_y_value[-1]
        else:
            wanted_y = same_y_value[0]

        return wanted_y

    # 获取顶部往下25像素的两个点坐标
    def get_middle_25_points():
        top_inner_point = {'x': pre_wanted_point['x'], 'y': get_inner_point()}
        wanted_downer_25_y = top_inner_point['y'] + 25
        wanted_left_x = 0
        wanted_right_x = 0
        # 判断该位置是否存在点
        wanted_point_indexes = np.where(item_collection_y == wanted_downer_25_y)
        if len(wanted_point_indexes[0]) >= 3:
            # 在对应index取x点坐标，找出离顶点x坐标最近的两个
            start_index = wanted_point_indexes[0][0]
            end_index = wanted_point_indexes[0][-1]
            wanted_xs = item_collection_x[start_index:end_index]
            wanted_xs_test_abs = abs(wanted_xs - pre_wanted_point['x'])
            wanted_x_index_1 = np.where(wanted_xs_test_abs == wanted_xs_test_abs.min())[0][0]
            wanted_x_1 = wanted_xs[wanted_x_index_1]

            wanted_x_1_left = wanted_xs[0]
            if wanted_x_index_1 > 0:
                wanted_x_1_left = wanted_xs[wanted_x_index_1 - 1]

            wanted_x_1_right = wanted_xs[wanted_x_index_1]
            if len(wanted_xs) > wanted_x_index_1 + 1:
                wanted_x_1_right = wanted_xs[wanted_x_index_1 + 1]

            wanted_x_index_2 = wanted_x_index_1 + 1
            wanted_left_x_index = wanted_x_index_1
            wanted_right_x_index = wanted_x_index_2
            # 如果距左侧点更远，则左侧点为需要的第二个点
            if abs(wanted_x_1 - wanted_x_1_left) > abs(wanted_x_1 - wanted_x_1_right):
                wanted_x_index_2 = wanted_x_index_1 - 1
                wanted_left_x_index = wanted_x_index_2
                wanted_right_x_index = wanted_x_index_1

            wanted_left_x = wanted_xs[wanted_left_x_index]
            wanted_right_x = wanted_xs[wanted_right_x_index]

        return {'left_x': wanted_left_x, 'right_x': wanted_right_x, 'y': wanted_downer_25_y,
                'top_x': top_inner_point['x'], 'top_y': top_inner_point['y']}

    # 20201128:逻辑调整为，获取顶部下方25像素的两个点坐标
    # wanted_y = get_inner_point()
    wanted_data_dic = get_middle_25_points()

    # plt.imshow(washed_img)
    # plt.show()
    return wanted_data_dic


def get_position_df(simple_index, pic_index, img_url):
    wanted_data = get_point_position(data_wash(mpimg.imread(img_url)))
    pic_index_real = pic_index.strip('_').split('.')[0]
    return pd.DataFrame({
        '试样': [simple_index],
        '图片': [pic_index_real],
        'left_x': [wanted_data['left_x']],
        'right_x': [wanted_data['right_x']],
        'y': [wanted_data['y']],
        'top_x': [wanted_data['top_x']],
        'top_y': [wanted_data['top_y']]
    })


def deployed_logical():
    df = pd.DataFrame(columns=['试样', '图片'])
    import os

    # base_dir = '/Users/azen/Documents/to_chang/upper/'
    base_dir = '/Users/azen/Documents/to_chang/v20201129/chang/chang/water/'
    simples_dir = os.listdir(base_dir)

    simple_deal_index = 0
    for simple_dir in simples_dir:
        simple_dir_abs = base_dir + simple_dir + '/'
        if os.path.isdir(simple_dir_abs):
            simple_index = simple_dir
            # 读试样下的文件
            simple_pics = os.listdir(simple_dir_abs)

            simple_pic_deal_index = 0
            for simple_pic_index in simple_pics:
                if simple_pic_index == '.DS_Store':
                    continue

                print('正在处理第 %d 个试样，总计 %d 个试样，当前图片 %d，当前试样总计图片 %d'
                      % (simple_deal_index, len(simples_dir), simple_pic_deal_index, len(simple_pics)))

                simple_pic_url = simple_dir_abs + simple_pic_index
                print('开始处理：' + simple_pic_url)
                wanted = get_position_df(simple_index, simple_pic_index, simple_pic_url)
                # print(wanted)
                df = df.append(wanted, ignore_index=True)
                simple_pic_deal_index += 1

            simple_deal_index += 1
            df.to_csv('sample_result.csv')
    df = df.sort_values(by=['试样', '图片'], ascending=[True, True]).reset_index()
    del df['index']
    df.to_csv('sample_result.csv')


def test_logical():
    wanted = get_position_df('1-31', '_0', './ori_imgs/_56.jpg')
    print(wanted)


def block_print():
    import sys
    import os
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    import sys
    sys.stdout = sys.__stdout__


if __name__ == '__main__':
    test_logical()
    # block_print()
    # deployed_logical()

    # enable_print()
