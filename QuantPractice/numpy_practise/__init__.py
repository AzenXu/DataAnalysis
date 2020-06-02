def test_python_number():
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn

    def normal_list_choice():
        list_a = [[1, 2, 3],
                  [4, 5, 6]]
        print(list_a[1][2])

    def numpy_test():
        a = np.array([0, 1, 2])
        # 类型
        print(type(a))  # <class 'numpy.ndarray'>
        # 修改
        a[0] = 10
        # 方法们
        print(np.ones(10).std())  # 标准差  0.0
        print(np.ones(10).cumsum())  # 累加  [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
        print(np.ones(10).cumprod())  # 累乘  [1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]

        print(np.ones(shape=(10, 1)).ndim)  # n dimension  # 2
        print(np.ones(10).shape)  # (10,)
        print(np.ones(2).dtype)  # data type  # float64

        print(np.ones(2).astype(np.int).dtype)  # int64

        a_slice = a[1:2]
        a_slice[0] = 666
        # print(a) # [ 10 666 2]

        a = np.array([i * 2 for i in range(10)])  # [ 0  2  4  6  8 10 12 14 16 18]
        b = np.arange(10)  # [0 1 2 3 4 5 6 7 8 9]
        c = 2
        d = np.array(range(2))

        print(np.arange(2) + np.ones(2))  # [1. 2.]
        print(np.ones(3) + 1)  # [2. 2. 2.]
        # print(np.ones(2) + np.ones(3))  # ValueError: operands could not be broadcast together with shapes (2,) (3,)

        print(np.sqrt(np.ones(2) * 4))  # [2. 2.]
        print(np.array([[0, 1], [10, 11]])[1, 1])  # 11
        print(np.ones(10).sum())  # 10.0

        print(np.ones(shape=(3, 6)).sum(axis=0), np.ones(shape=(3, 6)).sum(axis=1))  # [3. 3. 3. 3. 3. 3.] [6. 6. 6.]

        def condition_select():
            year_array = np.arange(2010, 2020)
            print(year_array[year_array > 2015])  # [2016 2017 2018 2019]
            print(year_array[(year_array > 2015) & (year_array < 2018)])  # [2016 2017]
            print(year_array[(year_array > 2015) | (year_array % 2 == 0)])  # [2010 2012 2014 2016 2017 2018 2019]

        condition_select()

        print(np.where(np.arange(4) >= 2, 1, 0))  # [0 0 1 1]
        print(np.where(np.array([[[1, 2, 3]]]) > 2))  # (array([0]), array([0]), array([2]))

        print(np.sign(np.array([10, 0, -10])))  # [ 1  0 -1]
        print(np.any(np.array([1, 0, -1]) > 0))  # True
        print(np.all(np.array([1, 0, -1]) > 0))  # False

        print(np.arange(4).reshape(2, 2))  # [[0 1] [2 3]]

        print(np.ones_like(np.arange(4).reshape(2, 2)))  # [[1 1] [1 1]]
        print(np.empty((2, 2), int))
        print(np.linspace(0, 2, 3))  # [0. 1. 2.]

        print(np.resize(np.arange(0, 2), (1, 5)))  # [[0 1 0 1 0]]

        print(np.ones((1, 2)).T)  # [[1.] [1.]]
        print(np.ones((1, 2)).transpose())  # [[1.] [1.]]
        print(np.ones((2, 2)).flatten())  # [1. 1. 1. 1.]
        print(np.arange(0, 4).reshape(2, 2).flatten(order='C'))  # [0 1 2 3]
        print(np.arange(0, 4).reshape(2, 2).flatten(order='F'))  # [0 2 1 3]

        print(np.zeros((2, 2)) + np.ones((2, 1)))  # [[1 1] [1 1]]

    def line_calculate():
        # 解线性方程
        arguments = np.array([[3, 1], [1, 2]])
        values = np.array([9, 8])
        point = np.linalg.solve(arguments, values)
        print(point)  # [2. 3.]

    def random_generate():
        print(np.random.randn())

        print(np.random.randn(2, 2).round(2))
        # [[-1.06  0.49]
        #  [ 0.02  0.07]]

        print(np.random.rand(2, 2).round(2))
        # [[0.25 0.32]
        #  [0.86 0.45]]

        # np.random.seed(6)
        print(np.random.randn(2))

        print(np.random.randint(-2, 2, size=(2, 2)))
        # [[-2 -2]
        #  [ 0  1]]

        print(np.random.choice(['诸葛青', '柳妍妍', '宝儿姐', '不摇碧莲', '王道长'], size=(1, 2), p=[0.5, 0.2, 0.1, 0.1, 0.1]))
        # [['诸葛青' '诸葛青']]

    def fit_test():
        x = np.arange(1, 11)
        y = 3 * x + 2

        reg = np.polyfit(x, y, 1)
        print(reg)  # [3. 2.]

        x = np.arange(1, 11)
        y = 3 * x ** 2 + x + 10
        print(np.polyfit(x, y, 2))  # [ 3.  1. 10.]

        y = np.polyval([3, 1, 10], x=1)
        print(y)  # 14

        x_array = np.sort(np.random.randn(800))
        y_array = np.random.randn(800)
        reg1 = np.polyfit(x_array, y_array, 1)
        reg2 = np.polyfit(x_array, y_array, 2)
        reg3 = np.polyfit(x_array, y_array, 3)

        y_fit_linear = np.polyval(reg1, x_array)
        y_fit_quadratic = np.polyval(reg2, x_array)
        y_fit_cubic = np.polyval(reg3, x_array)

        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.plot(x_array, y_array, 'r.', label='data')
        plt.plot(x_array, y_fit_linear, 'g-', label='linear')
        plt.plot(x_array, y_fit_quadratic, 'b-', label='quadratic')
        plt.plot(x_array, y_fit_cubic, 'y-', label='cubic')
        plt.legend()
        plt.show()

    # numpy_test()
    # normal_list_choice()
    # line_calculate()
    # random_generate()
    fit_test()


if __name__ == '__main__':
    test_python_number()
