def plot_test():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    import matplotlib
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像时符号'-'显示为方块的问题

    def pandas_appendix_plot():
        np.random.seed(6)
        df = pd.DataFrame((np.random.randn(5, 4).round(1) * 10 + 100).astype('int'),
                          index=['张无忌', '令狐冲', '乔峰', '金轮法王', '韦小宝'],
                          columns=['内力', '力道', '拳掌', '轻功'])
        #        内力   力道   拳掌   轻功
        # 张无忌    97  107  102   91
        # 令狐冲    75  109  111   85
        # 乔峰    116   96  126  106
        # 金轮法王   97  112  101  101
        # 韦小宝   101   98  106  108
        df.plot(figsize=(8, 6),
                title='人物属性表',
                style=['--', '-'],
                ylim=[df.内力.min() * 0.8, df.内力.max() * 1.2],  # 动态设置y最大/最小值
                secondary_y='内力'
                )
        # df.hist(
        #     figsize=(9, 4),  # 绘图大小
        #     bins=10,  # 直方图颗粒度大小
        # )

        # 用散点图寻找内力和力道的相关性
        # df.plot(
        #     kind='scatter',
        #     x='内力',
        #     y='力道'
        # )

        plt.show()
        pass

    # pandas_appendix_plot()

    def mat_plot_test():
        # plt.plot(range(8, 80, 10))

        # plt.plot(range(0, 10),
        #          range(0, 10),
        #          'g--',
        #          label='Beauty',  # 配置图例，需要调plt.legend()才会展示
        #          )
        # plt.legend()  # 展示图例
        # plt.ylabel('y')
        # plt.xlabel('不是x')
        # plt.ylim(0, 10)
        # plt.show()

        # data = np.arange(0, 3, 0.2)
        # plt.plot(data, data, 'r--',
        #          data, data ** 2, 'b',
        #          data, data ** 3, 'm .'
        #          )

        from matplotlib import style
        style.use('ggplot')
        # plt.figure(figsize=(8, 6))  # 生成绘图上下文
        # plt.plot(np.arange(0, 3, 0.2))
        # plt.plot(np.arange(0, 3, 0.2) ** 2)
        # plt.plot(np.arange(0, 3, 0.2) ** 3)
        # plt.show()

        # plt.scatter(x=[1, 2, 3, 4, 5],
        #             y=[6, 6, 3, 6, 6])

        # fig1, ax = plt.subplots()
        # plt.plot([1, 2, 3], 'g')
        # plt.ylabel('y1')
        #
        # ax.twinx()
        # plt.plot([10, 9, 8], 'r')
        # plt.ylabel('y2')

        plt.subplot(221)
        # equivalent but more general
        ax1 = plt.subplot(2, 2, 1)
        # add a subplot with no frame
        ax2 = plt.subplot(222, frameon=False)
        # add a polar subplot
        plt.subplot(223, projection='polar')
        # add a red subplot that shares the x-axis with ax1
        plt.subplot(224, sharex=ax1, facecolor='red')
        # delete ax2 from the figure
        plt.delaxes(ax2)
        # add ax2 to the figure again
        plt.subplot(ax2)

        plt.show()

        pass

    mat_plot_test()


if __name__ == '__main__':
    plot_test()
    print('Give you some color see see')
