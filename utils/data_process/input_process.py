from email.mime import base
from sklearn.preprocessing import *
import numpy as np
import pandas as pd

def DateIndexMap(df, date):
    for i in df[df['Date']==date].index:
        return i

def IndexDateMap(df, index):
    return df["Date"][index]


class batch_scalar:
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


class full_wav_scalar():
    
    def __init__(self, full_wav, start_p, end_p, scalar_mehod=None):
        self.full_wav = np.array(full_wav)
        self.step = end_p-start_p
        self.scalar_method = scalar_mehod

    def apply_wav(self):
        res = np.empty(shape=(0,1))
        run_num = int(len(self.full_wav)/(self.step))

        for i in range(run_num):
            
            start = 0+i*self.step
            end = self.step+i*self.step
            
            batch_wav = self.full_wav[start:end]

            scalar_dict = {
            "min_max":batch_scalar.min_max_scalar(batch_wav),
            "std":batch_scalar.std_scalar(batch_wav),
            "ret":batch_scalar.ret(batch_wav),
            "log_diff":batch_scalar.log_diff(batch_wav)
        }
            # print(type(scalar_dict['{}'.format(self.scalar_method)]))
            res = np.append(res, scalar_dict['{}'.format(self.scalar_method)])

        return res