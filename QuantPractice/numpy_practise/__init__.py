def test_python_number():
    def normal_list_choice():
        list_a = [[1, 2, 3],
                  [4, 5, 6]]
        print(list_a[1][2])

    def numpy_test():
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn

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

    numpy_test()

    # normal_list_choice()


if __name__ == '__main__':
    test_python_number()
