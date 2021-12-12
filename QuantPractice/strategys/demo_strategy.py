import pandas as pd
import QuantPractice.strategys.define as define
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('哈哈哈')

    df = define.xunfei.get_bar('20211001', '20211205').close
    df.plot()
    plt.show()
