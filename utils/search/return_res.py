from re import search
from utils.search import do_search
from utils.data_process import input_process, res_process
import numpy as np


def get_sim_res(df, s, e, algo = None, rank = 1):
    '''
    algo = ["shape_d", "mink_d", "corr_d", "dtw_d", "poly_d", "polycos_d"]
    rank is the top three similar interval
    '''


    # proccess data

    input_proccess = input_process.full_wav_scalar(full_wav=np.array(df['Close']), start_p=s, end_p=e, scalar_mehod="min_max")
    full_wav_std = input_proccess.apply_wav()
    baseline_wav_std = full_wav_std[s:e]

    # do search

    res_d = {}
    search = do_search.search(baseline_wav=baseline_wav_std, full_wav=full_wav_std)
    res_d['{}'.format(algo)] = search.run_search_test(algo_option=algo)

    # sort dict
    if algo=="corr_d" or algo=="polycos_d":
    # if algo=="corr_d":
        # print(algo)
        res_d_sorted = dict(sorted(res_d[algo].items(), key=lambda item: item[1], reverse=True))
    else:
        print(algo)
        res_d_sorted = dict(sorted(res_d[algo].items(), key=lambda item: item[1]))

    # result list
    clear_res_engine = res_process.clean_duplicate_li(list(res_d_sorted.keys())[:100])

    res = clear_res_engine.ret_uq_range()

    return res[:rank]