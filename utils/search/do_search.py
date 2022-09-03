from email.mime import base
from tkinter.messagebox import NO
from turtle import st
from utils.algo.calculation import *
from utils.data_process import input_process, res_process
from tqdm import tqdm

class Search():
    '''
    Input:
        df -> pandas raw data frame
        scalar_func -> a BatchScaler function
        algo_func -> a algo caculation function
        ohlc_average -> bool, average the similarity result of OHLC of stock price

    Ouput: 
        res_d -> an dictionary with similarity result

    Option:
        algo_func = ["shape_d", "mink_d", "corr_d", "dtw_d", "poly_d", "polycos_d"]
        scalar_func = ["min_max_scalar", "std_scalar", "ret", "log_diff"]

    '''
    def __init__(
        self, df, start_d, end_d,
        scalar_func=input_process.BatchScaler.min_max_scalar, algo_func=mink_d, 
            ohlc_average=True):

        self.scalar_func = scalar_func
        self.algo_func = algo_func
        self.ohlc_average = ohlc_average
        self.df = df
        self.s, self.e = input_process.DateIndexMap(df, start_d), input_process.DateIndexMap(df, end_d)

        self.scalar_func_name = scalar_func.__name__
        self.algo_func_name = self.algo_func.__name__

    def standerdization(self):
        '''Standerdization
        '''
        if self.ohlc_average==True:
            o,h,l,c = np.array(self.df["Open"]), np.array(self.df["High"]), np.array(self.df["Low"]), np.array(self.df["Close"])

            # call proccess function
            proccess = input_process.FullWavScaler(start_p=self.s, end_p=self.e, scalar_func=self.scalar_func)

            # std ohlc
            full_wav_std_o, full_wav_std_h  = proccess.apply_wav(o), proccess.apply_wav(h)
            full_wav_std_l, full_wav_std_c = proccess.apply_wav(l), proccess.apply_wav(c)

            baseline_wav_std_o, baseline_wav_std_h = full_wav_std_o[self.s:self.e], full_wav_std_h[self.s:self.e]
            baseline_wav_std_l, baseline_wav_std_c = full_wav_std_l[self.s:self.e], full_wav_std_c[self.s:self.e]
        
        return [full_wav_std_o, full_wav_std_h, full_wav_std_l, full_wav_std_c,
                baseline_wav_std_o, baseline_wav_std_h, baseline_wav_std_l, baseline_wav_std_c]
   

    def search(self):
        '''Loop full wav with baseline wav
        '''
        std_wav = self.standerdization()
        res_d = {}
        for index in tqdm(range(len(std_wav[0])-len(std_wav[0+4]))):
            start = index
            step = len(std_wav[0+4])
            ohlc_res_li = []

            # Calculate O, H, L, C in each iter
            for iter in range(4):
                # std_wav[iter] is standereized fullwav when 0<=iter<=3 
                # std_wavp[iter+4] is standereized baselinewav when iter>3
                tmp_res = None
                target_wav = std_wav[iter][start:start+step]
                tmp_res = self.algo_func(std_wav[iter+4], target_wav)
                if tmp_res != None:
                    ohlc_res_li.append(tmp_res)

            res = sum(ohlc_res_li)/len(ohlc_res_li)

            if self.scalar_func_name=='ret' or self.scalar_func_name=='log_diff':
                res_d["{}:{}".format(start-1, start+step-1)] = res

            else:
                res_d["{}:{}".format(start, start + step)] = res
        return res_d


    def sort_res_d(self):
        '''Sort dict
        '''
        res_d = self.search()
        if self.algo_func_name=="corr_d" or self.algo_func_name=="polycos_d":
            res_d_sorted = dict(sorted(res_d.items(), key=lambda item: item[1], reverse=True))
        else:
            res_d_sorted = dict(sorted(res_d.items(), key=lambda item: item[1]))
        return res_d_sorted

    def get_res(self,rank=1):
        '''Clear result
        '''
        res_d_sorted = self.sort_res_d()
        clear_res_engine = res_process.CleanResult()
        res = clear_res_engine.clean_duplicate_li(li = list(res_d_sorted.keys())[:100])
        return res[:rank]




    # def run_search_test(self, proccess_method=None, algo_option=None):
    #     res_d = {}
    #     for i in tqdm(range(len(self.full_wav)-len(self.baseline_wav))):
    #         res = None
    #         start = i
    #         step = len(self.baseline_wav)
    
    #         target_wav = self.full_wav[start:start+step]        

    #         if algo_option == "dtw_d":
    #             res = dtw_d(self.baseline_wav, target_wav)

    #         elif algo_option == "corr_d":
    #             res = corr_d(self.baseline_wav, target_wav)

    #         elif algo_option == "mink_d":
    #             res = mink_d(self.baseline_wav, target_wav)

    #         elif algo_option == "shape_d":
    #             res = shape_d(self.baseline_wav, target_wav)

    #         elif algo_option == "poly_d":
    #             res = poly_d(self.baseline_wav, target_wav)

    #         elif algo_option == "polycos_d":
    #             res = polycos_d(self.baseline_wav, target_wav)

    #         if res != None:

    #             if proccess_method=='ret' or proccess_method=='log_diff':
    #                 res_d["{}:{}".format(start-1, start+step-1)] = res

    #             else:
    #                 res_d["{}:{}".format(start, start + step)] = res


    #     return res_d
