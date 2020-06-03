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

    # series_test()

    def data_frame_test():
        def data_frame_init():
            df_obj = pd.DataFrame(np.random.randn(3, 3).round(2),
                                  columns=['语文', '数学', '哲学'],
                                  index=['王也', '诸葛青', '宝儿'])
            #        语文    数学    哲学
            # 王也   1.60 -0.45  0.68
            # 诸葛青 -1.02  1.24  0.13
            # 宝儿  -0.67  0.21  0.98
            # print(df_obj.loc[['王也', '宝儿']])
            # print(df_obj.loc['王也':'宝儿'])
            # print(df_obj.loc[['王也', '宝儿'], ['哲学']])
            # print(df_obj.iloc[[0, 2], [-1]])
            # print(df_obj.ix[0:2], ['哲学'])  # 方法作废

            wanted = ((df_obj.哲学 > 0) * 1) + ((df_obj.数学 > 0) * 1) + ((df_obj.语文 > 0) * 1) >= 2
            # print(df_obj[wanted])

            df_obj['体育'] = pd.Series(range(0, 3), index=['王也', '宝儿',
                                                         '诸葛青'])  # range(0, 3)  # pd.Series(range(0, 3)) #range(0, 3) #np.arange(0,3)
            # print(df_obj)
            del df_obj['体育']
            # print(df_obj)
            df_obj['刀法'] = pd.DataFrame(np.random.randn(3).round(2), index=['王也', '宝儿', '诸葛青'])
            # print(df_obj)

            df_obj = pd.DataFrame({
                '语文': pd.Series(np.ones(3)),
                '数学': pd.Series(np.random.randn(2).round(2)),
            })
            #     语文    数学
            # 0  1.0  0.13
            # 1  1.0 -0.78
            # 2  1.0  NaN
            # print(df_obj.语文, type(df_obj.语文))
            # 0    1.0
            # 1    1.0
            # 2    1.0
            # Name: 语文, dtype: float64 <class 'pandas.core.series.Series'>
            # print(df_obj.values)
            print(df_obj.isnull())

            dates = pd.date_range('2020-06-01', periods=10, freq='M')
            # print(dates)

        # data_frame_init()

        def data_frame_plus():
            period = pd.date_range('20200601', periods=10000, freq='D')
            df = pd.DataFrame(np.random.randn(10000, 4),
                              columns=['V1', 'V2', 'V3', 'V4'],
                              index=period)
            df['type'] = np.random.choice(['A', 'B', 'C', 'D'], size=10000)

            grouped = df.groupby('type')
            # <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7fe66783fed0>
            print(grouped.size())
            print(type(grouped.get_group('A')))

            df['type-B'] = np.random.choice(['男', '女'], size=10000)
            grouped = df.groupby(['type', 'type-B'])
            print(grouped.agg([np.max, np.min]))
            pass

        # data_frame_plus()

        def data_frame_stack():
            df1 = pd.DataFrame(np.zeros((2, 2)), columns=['columnA', 'columnB'], index=['indexA', 'indexB'])
            df2 = pd.DataFrame(np.ones((2, 2)), columns=['columnA', 'columnC'], index=['indexA', 'indexC'])

            print(pd.concat((df1, df2)))
            #         columnA  columnB  columnC
            # indexA      0.0      0.0      NaN
            # indexB      0.0      0.0      NaN
            # indexA      1.0      NaN      1.0
            # indexC      1.0      NaN      1.0
            print(pd.concat((df1, df2), axis=1))
            #         columnA  columnB  columnA  columnC
            # indexA      0.0      0.0      1.0      1.0
            # indexB      0.0      0.0      NaN      NaN
            # indexC      NaN      NaN      1.0      1.0
            print(df1.join(df2, rsuffix='_df2'))
            #         columnA  columnB  columnA_df2  columnC
            # indexA      0.0      0.0          1.0      1.0
            # indexB      0.0      0.0          NaN      NaN
            print(df1.join(df2, rsuffix='_df2', how='outer'))
            #         columnA  columnB  columnA_df2  columnC
            # indexA      0.0      0.0          1.0      1.0
            # indexB      0.0      0.0          NaN      NaN
            # indexC      NaN      NaN          1.0      1.0

            df1['type_1'] = pd.Series(['股票', '基金'], index=['indexA', 'indexB'])
            df2['type_2'] = pd.Series(['股票', '期货'], index=['indexA', 'indexC'])

            print(pd.merge(df1, df2, left_on='type_1', right_on='type_2', how='outer'))
            #    columnA_x  columnB type_1  columnA_y  columnC type_2
            # 0        0.0      0.0     股票        1.0      1.0     股票
            # 1        0.0      0.0     基金        NaN      NaN    NaN
            # 2        NaN      NaN    NaN        1.0      1.0     期货

            print(pd.merge(df1, df2, left_index=True, right_index=True, how='left'))
            #         columnA_x  columnB type_1  columnA_y  columnC type_2
            # indexA        0.0      0.0     股票        1.0      1.0     股票
            # indexB        0.0      0.0     基金        NaN      NaN    NaN

        # data_frame_stack()

        def multi_index():
            # Series多重索引
            se = pd.Series(np.random.randn(5).round(2),
                           index=[['科大', '科大', '茅台', '茅台', '茅台'],
                                  ['Q1', 'Q2', 'Q1', 'Q2', 'Q3']])
            print(se)
            # 科大  Q1    1.35
            #     Q2    1.83
            # 茅台  Q1    1.22
            #     Q2    0.74
            #     Q3   -0.23
            print(se.unstack())
            #       Q1    Q2    Q3
            # 科大  1.35  1.83   NaN
            # 茅台  1.22  0.74 -0.23

            # DataFrame多重索引
            df = pd.DataFrame(np.random.randn(3, 2).round(2),
                              index=[['科大', '科大', '茅台'],
                                     ['Q1', 'Q2', 'Q3']],
                              columns=['股价', 'PE']
                              )

            print(df)
            #         股价    PE
            # 科大 Q1 -0.19 -1.96
            #    Q2  1.16  0.84
            # 茅台 Q3 -2.20  0.05

            print(df.unstack())
            #       股价               PE
            #       Q1    Q2   Q3    Q1    Q2    Q3
            # 科大 -0.19  1.16  NaN -1.96  0.84   NaN
            # 茅台   NaN   NaN -2.2   NaN   NaN  0.05

            print(df.sum(level=0))
            #       股价    PE
            # 科大  5.11  0.59
            # 茅台 -0.06 -1.69

        multi_index()

    data_frame_test()


if __name__ == '__main__':
    print('Pandas will never be a slave!!!👹')
    pandas_practice()
