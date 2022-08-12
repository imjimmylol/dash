from utils.algo.calculation import *
from tqdm import tqdm

class search():

    def __init__(self, baseline_wav, full_wav):

        self.baseline_wav = baseline_wav
        self.full_wav = full_wav

    def run_search_test(self, proccess_method=None, algo_option=None):
        res_d = {}
        for i in tqdm(range(len(self.full_wav)-len(self.baseline_wav))):
            res = None
            start = i
            step = len(self.baseline_wav)
    
            target_wav = self.full_wav[start:start+step]        

            if algo_option == "dtw_d":
                res = dtw_d(self.baseline_wav, target_wav)

            elif algo_option == "corr_d":
                res = corr(self.baseline_wav, target_wav)

            elif algo_option == "mink_d":
                res = mink_d(self.baseline_wav, target_wav)

            elif algo_option == "shape_d":
                res = shape_d(self.baseline_wav, target_wav)


            if res != None:

                if proccess_method=='ret' or proccess_method=='log_diff':
                    res_d["{}:{}".format(start-1, start+step-1)] = res

                else:
                    res_d["{}:{}".format(start, start + step)] = res


        return res_d
