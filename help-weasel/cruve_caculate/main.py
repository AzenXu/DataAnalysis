import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# np.set_printoptions(threshold=np.nan)
import pandas as pd
import matplotlib


def data_wash(img):
    # print(img)

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

                # 左右4个点内，y相同的点的数量
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

                # 上下4个点内，x相同的点的数量
                x_positions = np.where(white_points_x == x)[0]
                # 用position们去y_list中找y们
                y_count = 0
                for j in range(len(x_positions)):
                    x_index = x_positions[j]
                    tmp_y = white_points_y[x_index]
                    if abs(tmp_y - y) < 4:
                        y_count += 1
                if y_count <= 4:
                    fly_points_ver.append((x, y))

            return fly_points_ver

        # print(find_fly_points_ver())

        def remove_fly_points(fly_points) -> np.ndarray:
            for point in fly_points:
                point_x, point_y = point
                no_machine_img[point_y][point_x] = np.nan
            return no_machine_img

        # print(remove_fly_points(find_fly_points_hor()))

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

    # print(y_min_point['x'], y_max_point['x'])

    # 判断两个点，谁的x值距离图片中心点x最近，选出最近的那个点
    center_x = washed_img.shape[1] * 0.5
    # print(center_x)
    if abs(y_min_point['x'] - center_x) < abs(y_max_point['x'] - center_x):
        pre_wanted_point = y_min_point
    else:
        pre_wanted_point = y_max_point

    # print(pre_wanted_point)

    # pre_wanted_point为材料外侧点，需要找到与它x相同的，对应的内侧点
    same_x_position = np.where(item_collection_x == pre_wanted_point['x'])
    same_y_value = item_collection_y[same_x_position]
    if same_y_value[0] == pre_wanted_point['y']:
        wanted_y = same_y_value[-1]
    else:
        wanted_y = same_y_value[0]

    # print(wanted_y)

    # plt.imshow(washed_img)
    # plt.show()
    return wanted_y


def get_position_df(simple_index, pic_index, img_url):
    wanted_y = get_point_position(data_wash(mpimg.imread(img_url)))
    pic_index_real = pic_index.strip('_').split('.')[0]
    return pd.DataFrame({
        '试样': [int(simple_index)],
        '图片': [int(pic_index_real)],
        'y值': [wanted_y]
    })


if __name__ == '__main__':
    df = pd.DataFrame(columns=['试样', '图片', 'y值'])
    import os

    base_dir = '/Users/azen/Documents/data/'
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
                print(wanted)
                df = df.append(wanted, ignore_index=True)
                simple_pic_deal_index += 1

            simple_deal_index += 1
            print(df)
    df = df.sort_values(by=['试样', '图片'], ascending=[True, True]).reset_index()
    del df['index']
    df.to_csv('sample_result.csv')
