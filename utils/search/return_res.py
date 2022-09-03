from re import search
from utils.search.do_search import Search
from utils.data_process import input_process, res_process
import numpy as np


def GetSimRes(df, s, e, algo = None, rank = 1, scalar_func = input_process.BatchScaler.min_max_scalar):
    '''
    Input: 
        df -> pd dataframe 
        s,e -> int, the index of pd dataframe (if input date, needed DateIndexMap for conversion)
        algo -> function, the distance functions in algo
        rank -> int, the first n similarity result you want to obtain
        scalar_func -> function, the standardization method

    Option:
        algo = ["shape_d", "mink_d", "corr_d", "dtw_d", "poly_d", "polycos_d"]
        scalar_func = min_max_scalar, std_scalar, ret, log_diff
    '''
    # proccess data
    input_proccess =  input_process.FullWavScaler(full_wav=np.array(df['Close']), start_p=s, end_p=e, scalar_func=scalar_func)

    full_wav_std = input_proccess.apply_wav()
    baseline_wav_std = full_wav_std[s:e]

    # do search

    res_d = {}
    search = do_search.search(baseline_wav=baseline_wav_std, full_wav=full_wav_std)
    res_d['{}'.format(algo)] = search.run_search_test(algo_option=algo)

    # sort dict
    if algo=="corr_d" or algo=="polycos_d":
        res_d_sorted = dict(sorted(res_d[algo].items(), key=lambda item: item[1], reverse=True))
    else:
        res_d_sorted = dict(sorted(res_d[algo].items(), key=lambda item: item[1]))

    # result list
    clear_res_engine = res_process.clean_duplicate_li(list(res_d_sorted.keys())[:100])

    res = clear_res_engine.ret_uq_range()

    return res[:rank]