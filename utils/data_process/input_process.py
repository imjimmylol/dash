from email.mime import base
from sklearn.preprocessing import *
import numpy as np
import pandas as pd

def DateIndexMap(df, date):
    for i in df[df['Date']==date].index:
        return i

def IndexDateMap(df, index):
    return df["Date"][index]


class BatchScaler:
    """
    輸入1個arr回傳1個等長arr
    - min_max std_scalar 會返回等長序列
    - ret 與 log diff 會回傳序列-1個值
    """
    def __init__(self):
        pass

    @staticmethod
    def min_max_scalar(arr):
        process_func = MinMaxScaler()
        arr_reshape = arr.reshape(-1,1)
        res = process_func.fit_transform(arr_reshape)
        return res.flatten()

    @staticmethod
    def std_scalar(arr):
        arr_reshape = arr.reshape(-1,1)
        process_func = StandardScaler()
        res = process_func.fit_transform(arr_reshape)
        return res.flatten()

    @staticmethod
    def ret(arr):
        arr = pd.Series(arr)
        return np.array((arr[1:])/((arr.shift(1))[1:]))

    @staticmethod
    def log_diff(arr):
        arr_log = np.log(arr)
        arr_diff = pd.Series(arr_log).diff(1).dropna()
        return np.array(arr_diff)

class FullWavScaler:
    def __init__(self, start_p, end_p, scalar_func=None):
        self.step = end_p-start_p
        self.scalar_func = scalar_func

    def apply_wav(self, full_wav):
        res = np.empty(shape=(0,1))
        run_num = int(len(full_wav)/(self.step))

        for i in range(run_num):
            start = 0+i*self.step
            end = self.step+i*self.step
            
            batch_wav = full_wav[start:end]
            
            res = np.append(res, self.scalar_func(batch_wav))

        return res