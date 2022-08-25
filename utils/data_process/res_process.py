import numpy as np


def range_2_li(li):
    l, u = int(li.split(':')[0]), int(li.split(':')[1])
    return [i for i in range(l, u)]


def range_2_num(text):
    text = text[0]
    l, u = int(text.split(':')[0]), int(text.split(':')[1])
    return l, u


def li_check_intersect(li1, li2, overlap_protion):
    # 重疊超過一定比例就刪除
    overlap_num = int(len(li1) / overlap_protion)
    intersection = (set(li1) & set(li2))
    if len(intersection) > overlap_num:
        return True
    elif len(intersection) <= overlap_num:
        return False

def res_d_set(d1, d2, rank_d1=50, rank_d2 = 50):
    """
    優先度高的字典放前面(d1)
    把自己要不同演算法做出來的字典取交集，預設取前50名
    res_d_set(d1, d2, rank_d1, rank_d2)
    res_d_set(d2, d3, rank_d1, rank_d2)
    """
    x, y = list(d1.keys()) ,list(d2.keys())
    return set(x[1:rank_d1]).intersection(set(y[1:rank_d2]))

class clean_duplicate_li():
    """
    輸入一個有重複區間的list，返回不重疊的部分
    """
    def __init__(self, li, overlap_protion=5):
        self.li = li
        self.overlap_protion = overlap_protion

    def ret_uq_range(self):
        res_list = self.li
        uq_li = []
        while len(res_list) > 0:
            current_uq = range_2_li(res_list[0])
            pop_index = []
            try:
                for i in range(len(res_list)):
                    intersect = li_check_intersect(current_uq, range_2_li(res_list[i]), overlap_protion=self.overlap_protion)
                    if intersect:
                        pop_index.append(i)
                    else:
                        pass
                res_list_np = np.array(res_list)
                res_list_np_rm = np.delete(res_list_np, tuple(pop_index))

                res_list = res_list_np_rm.tolist()

                uq_li.append(res_list[0])

            except IndexError:
                return uq_li
