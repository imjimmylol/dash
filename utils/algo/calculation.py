from turtle import shape
import numpy as np
from dtaidistance import dtw
from tqdm import tqdm
import pandas as pd
import warnings
warnings.simplefilter('ignore', np.RankWarning)

def arr2poly_coef(arr):
    x = np.array([i for i in range(len(arr))])
    res = np.polyfit(x, arr, len(arr))
    return  res

def rms(x):
    return np.sqrt(np.mean(x**2))

def poly2on(poly_coeff):
    x = np.array([i for i in range(len(poly_coeff))])
    orth_coef = np.polynomial.legendre.poly2leg(poly_coeff[::-1])
    leg_norms = np.array([rms(np.polynomial.Legendre(v)(x)) for v in np.eye(len(poly_coeff))])
    return orth_coef*leg_norms


def poly_d(arr1, arr2):
    onpoly1, onpoly2 = poly2on(arr2poly_coef(arr1)), poly2on(arr2poly_coef(arr2))
    return np.sqrt(sum((onpoly1 - onpoly2)**2))


def get_slope(arr):
    arr_series = pd.Series(arr)
    res = arr_series.diff(1).dropna()
    return np.array(res[1:])

def trans_m(d1, d2, trh=0.1):
    if d1<-trh:
        if d2<0:
            return -3
        elif d2==0:
            return -2
        elif d2>0:
            return -1
    elif d1>=-trh and d1<=trh:
        return 0
    elif d1>trh:
        if d2>0:
            return 3
        elif d2==0:
            return 2
        elif d2<0:
            return 1

def get_m(arr, trh=0.1):
    arr_series = pd.Series(arr)
    arr_d1_series, arr_d2_series = arr_series.diff(1), arr_series.diff(2)
    d_df = pd.DataFrame(zip(arr_d1_series, arr_d2_series ), columns=["d1",'d2']).dropna()
    res = list(map(trans_m, d_df['d1'], d_df['d2']))
    return np.array(res)
    
 
def get_conti_t(arr):
    arr = np.append(arr, False)
    sub = []
    sub.append(arr[0])
    length = 1 # logest substring --> long
    iter_t = 1
    res = np.array([0])
    for i in arr[1:]:
        iter_t+=1
        if iter_t < len(arr):
            if i - sub[-1]==0:
                sub.append(i)
                if len(sub) > length:
                    length = len(sub)
            else:
                res = np.append(res, np.repeat(len(sub)/len(arr), len(sub)))
                sub = []
                sub.append(i)
        else:
            res = np.append(res, np.repeat(len(sub)/len(arr), len(sub)))
            pass
    return np.delete(res, 0)

def norm_conti_t(arr):
    return arr/sum(arr)

def shape_d(arr1, arr2):
    '''
    arr 需經標準化
    '''
    m1, m2 = get_m(arr1), get_m(arr2)
    a1, a2 = get_slope(arr1), get_slope(arr2)
    t_weight = norm_conti_t(get_conti_t(m1-m2))

    return sum(t_weight*abs(m1-m2)*abs(a1-a2))
    


def mink_d(arr1, arr2, p = 2):
    arr1,arr2 = np.array(arr1), np.array(arr2)
    return (((arr1 - arr2) ** p).sum() ** (1 / p))
def corr(arr1, arr2):
    arr1,arr2 = np.array(arr1).flatten(), np.array(arr2).flatten()
    return np.corrcoef(arr1, arr2)[0][1]
def dtw_d(arr1, arr2):
    return dtw.distance(arr1, arr2)




def get_fbna(_min, _max):
    dif = _max-_min
    l1 = _max - 0.236*dif
    l2 = _max - 0.382*dif
    l3 = _max - 0.618*dif
    return (_max, l1, l2, l3, _min)
