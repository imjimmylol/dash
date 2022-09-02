import numpy as np
from dtaidistance import dtw
from tqdm import tqdm
import pandas as pd
import warnings
warnings.simplefilter('ignore', np.RankWarning)

# Preprocess of Algo Calculation 

def arr2polycoef(arr):
    '''for polyd
    Input: an standardized time series data
    Return numpy array: numpy polynomial regression coefficient of the input time sereis
    
    a_0 + a_1*x + a_2*x**2 + .... + a_n*x**n, where n is the lenght of input series
    '''
    x = np.array([i for i in range(len(arr))])
    res = np.polyfit(x, arr, len(arr))
    return  res

def rms(x):
    
    return np.sqrt(np.mean(x**2))

def poly2on(poly_coeff):
    '''for polyd
    Input numpy array: an array containg the fitted polynomial coefficents
    Return numpy array: transform polynomial based on O.N bases
    '''
    x = np.array([i for i in range(len(poly_coeff))])
    orth_coef = np.polynomial.legendre.poly2leg(poly_coeff[::-1])
    leg_norms = np.array([rms(np.polynomial.Legendre(v)(x)) for v in np.eye(len(poly_coeff))])
    return orth_coef*leg_norms
    

def get_fbna(__min, __max):
    '''for plot
    Return a tuple : the golden partion of stock data
    '''
    dif = __max-__min
    l1 = __max - 0.236*dif
    l2 = __max - 0.382*dif
    l3 = __max - 0.618*dif
    return (__max, l1, l2, l3, __min)


def get_slope(arr):
    '''for mosd
    Return a numpy array 
    '''
    arr_series = pd.Series(arr)
    res = arr_series.diff(1).dropna()
    return np.array(res[1:])

def trans_m(d1, d2, trh=0.1):
    '''for mosd
    Return int: the pattern of array
    '''
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
    '''for mosd
    Return numpy array: the pattern of the series
    '''
    arr_series = pd.Series(arr)
    arr_d1_series, arr_d2_series = arr_series.diff(1), arr_series.diff(2)
    d_df = pd.DataFrame(zip(arr_d1_series, arr_d2_series ), columns=["d1",'d2']).dropna()
    res = list(map(trans_m, d_df['d1'], d_df['d2']))
    return np.array(res)
    
 
def get_conti_t(arr):
    '''for mosd
    Return numpy array: the weight of a continous pattern 
    '''
    arr = np.append(arr, False)
    sub = []
    sub.append(arr[0])
    length = 1 
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



# Input two array and return the distance of the array 
# Note that the array must be a standardized array
def shape_d(arr1, arr2):
    '''shape distance
    Return : int
    '''
    m1, m2 = get_m(arr1), get_m(arr2)
    a1, a2 = get_slope(arr1), get_slope(arr2)
    t_weight = norm_conti_t(get_conti_t(m1-m2))

    return sum(t_weight*abs(m1-m2)*abs(a1-a2))
    
def mink_d(arr1, arr2, p = 2):
    '''minks distance
    Return: int
    '''
    arr1,arr2 = np.array(arr1), np.array(arr2)
    return (((arr1 - arr2) ** p).sum() ** (1 / p))

def corr_d(arr1, arr2):
    '''correlation coefficient distance
    Return: int
    '''
    arr1,arr2 = np.array(arr1).flatten(), np.array(arr2).flatten()
    return np.corrcoef(arr1, arr2)[0][1]

def dtw_d(arr1, arr2):
    '''Dynamic time wraping distance
    Return: int
    '''    
    return dtw.distance(arr1, arr2)

def poly_d(arr1, arr2):
    '''Polynimial distance (based on minks)
    Return: int
    '''
    onpoly1, onpoly2 = poly2on(arr2polycoef(arr1)), poly2on(arr2polycoef(arr2))
    return np.sqrt(sum((onpoly1 - onpoly2)**2))

def polycos_d(arr1, arr2):
    '''Polynimial distance (based on cos similarity)
    Return: int
    '''
    onpoly1, onpoly2 = poly2on(arr2polycoef(arr1)), poly2on(arr2polycoef(arr2))
    num = float(np.dot(onpoly1, onpoly2))
    denom = np.linalg.norm(onpoly1) * np.linalg.norm(onpoly2)
    # return 0.5 + 0.5 * (num / denom) if denom != 0 else 0
    return num/denom
   


