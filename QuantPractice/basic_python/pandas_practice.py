from pandas import Series


def pandas_practice():
    import numpy as np
    import pandas as pd

    def series_test():
        se = pd.Series(range(0, 2))
        print(se, type(se), type(se.values))
        # 0 0
        # 1 1
        # <class 'pandas.core.series.Series'>
        # <class 'numpy.ndarray'>
        print(pd.Series(np.arange(0, 2))[0])  # 0
        se: Series = pd.Series(range(0, 2))
        print(se[se > 0])  # 1    1

        print(pd.Series({'name': '王也', 'nickname': '身无分文'}))
        #  name    王也
        #  nickname    身无分文

        person = pd.Series({'name': '王也', 'nickname': '身无分文'})
        person.name = 'Person Info'
        person.index.name = 'Items'
        # Items
        # name          王也
        # nickname    身无分文
        # Name: Person Info, dtype: object

        print(pd.Series(['不摇莲', '机智一批', '不听闲话'],
                        index=['No.1', 'No.2', 'No.3']))
        # No.1     不摇莲
        # No.2    机智一批
        # No.3    不听闲话

        print(pd.Series(range(0, 3))[0:1])
        # 0    0

        person = pd.Series({'name': 'Trump',
                            'slogan': 'Fake News!',
                            'favorite': 'money'
                            })
        # Label切片
        print(person['name':'favorite'])
        # name             Trump
        # slogan      Fake News!
        # favorite         money
        # dtype: object

        # Label多选
        print(person[['name', 'favorite']])
        # name        Trump
        # favorite    money
        # dtype: object

    series_test()


if __name__ == '__main__':
    print('Pandas will never be a slave!!!👹')
    pandas_practice()
