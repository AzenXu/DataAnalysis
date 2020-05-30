def test():
    print('hey~ baby~')
    pass


def test_basic_grammar():
    def true_false_in():
        print(True and False)
        print(True or False)
        print(not True)
        print('a' in ['a', 'b', 'c'])
        print('a' in 'abc')
        print('a' not in r'abc')

    # 成员运算符 - 指针指的是不是同一个对象
    def member_opt():
        print('a' is 'a')
        a = ['a']
        a_equal = a
        print(a is a_equal)

        import copy
        a_copy = copy.copy(a)  # 浅拷贝 - list中的子对象不会拷贝，只是指针
        print(a_copy is a)
        a_deep_copy = copy.deepcopy(a)  # 深拷贝 - list中的子对象也拷贝
        print(a_deep_copy is a)
        print(a_deep_copy is not a_copy)

    def collections():
        import copy
        a_list = [1, 2, '666', [3, 8]]
        a_tuple = (1, 2, '666', [3, 8])
        a_set = set('aaacccc444311')  # 集合 - 去重 & 无序
        a_frozenset = frozenset(copy.deepcopy(a_set))
        a_dict = {'name': '王也', 'age': 21}
        print(a_dict['name'])
        a_dict['name'] = '身无分文王道长'
        print(a_dict['name'])

    # 不定长参数 - 元组
    def tuple_args_test():
        def tuple_args(a, b, *c):
            print(a, b, c, len(c), type(c))

        tuple_args(1, 2, 3, 4, 'a', 'b')

    # 不定长参数 - 字典
    def dict_args_test():
        def dict_args(a, **b):
            print(a, b, len(b), type(b))

        dict_args(a=1, name='王也', age=21, nick_name='身无分文')

    def lambda_test():
        sum_func = lambda a=1, b=2: a + b
        print(sum_func, sum_func())

    tuple_args_test()
    dict_args_test()
    lambda_test()


'''
Numpy: 
提供多维数组对象
各种派生对象(掩码数组、矩阵)
用于数组快速操作的各种API(数学、逻辑、形状操作、排序、选择、输入输出、离散傅立叶变换、基本线性代数，基本统计运算和随机模拟.etc)

核心：ndarray对象 - 封装了python原生n维数组
特点：
1. ndarray长度固定，改大小会重新创建个新数组
2. 元素数据类型相同 - 内存中大小相同
3. 针对矩阵乘法，做了C代码预编译，提升了计算速度 - 矢量化 - 减少了难以阅读的for循环

property:
@ndarray.ndim - 数组的轴(dimensions)个数
@ndarray.shape - 对于有 n 行和 m 列的矩阵，shape 将是 (n,m)
@ndarray.size - 总元素数量 - shape的乘积
@ndarray.dtype - 一个元素的类型
@ndarray.itemsize - 一个item的字节数
@ndarray.data - 该缓冲区包含数组的实际元素。通常，我们不需要使用此属性，因为我们将使用索引访问数组中的元素
'''


def numpy_array_init():
    import numpy
    a = numpy.arange(15).reshape(3, 5)
    print(a, '\n', a.shape, '\n', a.ndim, '\n', a.dtype.name, '\n', a.size, '\n', type(a), '\n')

    def basic_init():
        b = numpy.array([1, 2, 3])
        # b_wrong_init = numpy.array(1, 2, 3)

        # 将序列类型转为数组
        c = numpy.array([('a', 'b'), ('c', 'd'), ['e', 'f']])
        print(c)

    def init_with_no_value_but_structure():
        array = numpy.zeros((3, 4), int)
        print(array)
        array_2 = numpy.ones((3, 4), float)
        print(array_2)
        array_3 = numpy.empty((10, 10))  # 内容随机, 有内存决定
        print(array_3)

    def init_with_step():
        array = numpy.arange(0, 10, 2)
        print(array)
        # 针对可能有浮点数运算的步长，最好用linspace
        array_float = numpy.linspace(0, 1, 10)
        print(array_float)
        array_float_cube = array_float.reshape((5, 2))
        print(array_float_cube)

    # basic_init()
    # init_with_no_value_but_structure()
    init_with_step()
    pass


def numpy_array_calculate():
    # array运算都是做元素运算的
    import numpy

    a = numpy.array([20, 30, 40, 50])
    b = numpy.ones(4, int)
    c = a - b
    d = numpy.arange(4)
    print(c, d, d ** 2, numpy.sin(d), d < 2)

    # 矩阵乘法默认按元素计算，而不是矩阵相乘
    aa = numpy.array([[1, 1], [0, 1]])
    bb = numpy.array([[2, 0], [3, 4]])
    print(aa * bb, '\n', aa @ bb)

    # array内元素操作 - 求和、最小、最大、平均
    # 全集运算
    print(aa.sum(), aa.min(), aa.max(), aa.mean())
    # 按轴运算 - 0 -> 按列，1 -> 按行
    print(aa.sum(axis=0), aa.sum(axis=1))
    pass


def numpy_index_slice_loop():
    import numpy
    # 一维数组- 索引、切片、迭代同list
    # 多维数组

    def f(x, y):
        return 10 * x + y

    a = numpy.fromfunction(f, (5, 4), dtype=int)
    # [轴1切片, 轴2切片, 轴3切片]
    # 缺省值 - 轴完整切片 - a[-1] <=> a[-1, :, :] <=> a[-1,...]
    # print(a, a[0, 1], a[0:5, 0], a[:, 1], a[1:3, 1:3], a[-1], a[-1, ...], a[..., 0])
    #
    # bool型索引
    GDP_Percent = numpy.array([7.90, 7.80, 7.30, 6.90, 6.70])
    Year = numpy.array([2012, 2013, 2014, 2015, 2016])
    print(Year[GDP_Percent > 7])

    def loop():
        # 迭代 - 默认迭代第一个轴
        for row in a:
            print(row)

        # 迭代 - 用flat属性(数组的所有元素迭代器)完成所有元素迭代
        for element in a.flat:
            print(element)

    pass


def numpy_array_shape_change():
    import numpy

    a = numpy.floor(10 * numpy.random.random((3, 4)))
    print(a, a.shape)

    # 产生修改后的新数组 - 不改变原始数据
    # reshape(6, -1) - -1会自动计算为正确的数 -> 2
    print(a.ravel(), a.reshape(6, 2), a.reshape(6, -1), a.T)

    # 两数组堆叠
    b_1 = numpy.zeros((2, 2), int)
    b_2 = numpy.ones((2, 2), int)

    print(b_1, b_2, numpy.vstack((b_1, b_2)), numpy.hstack((b_1, b_2)))


    pass


def numpy_interesting_functions():
    import numpy
    a = numpy.arange(27).reshape((3,3,3))
    print(a)
    b = numpy.where(a > 5, 1, 0)
    print(b, type(b))
    print(a)

    pass


if __name__ == '__main__':
    # test()
    # test_basic_grammar()
    # numpy_array_init()
    # numpy_array_calculate()
    # numpy_index_slice_loop()
    # numpy_array_shape_change()
    numpy_interesting_functions()
