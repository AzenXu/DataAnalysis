import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd


def get_top_position(img) -> int:
    # print(img.shape)

    new_img = img[:, 500:1100, :].copy()  # 裁剪图片到中心区域
    new_img_bake = np.where(new_img > 50, 255, 0)
    positions = np.where(new_img_bake == [255, 255, 255])

    # print(new_img_bake)
    # plt.imshow(new_img_bake)
    # plt.show()


    # df = pd.DataFrame(positions[1], index=positions[0])
    # print(df.head(300))
    # print(positions[0][0])
    return positions[0][0]


if __name__ == '__main__':

    print(get_top_position(mpimg.imread('./ori_imgs/2.jpeg')))
