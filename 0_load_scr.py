from collections import defaultdict
import numpy as np


def load_scr(scr):
    score = defaultdict(lambda: defaultdict(list))
    with open(scr, "r") as f:
        for line in f.readlines():
            l = line.split()
            score[l[0]][l[1]].append(float(l[3]))
    return score


def gen_sms(score):
    sm_doc = {direction: {lang_pair: np.mean(langpair_list) for lang_pair, langpair_list in direction_dict.items(
    )} for direction, direction_dict in score.items()}

    sm_sys = {direction: np.mean([it for langpair_list in direction_dict.values(
    ) for it in langpair_list]) for direction, direction_dict in score.items()}

    return sm_doc, sm_sys
