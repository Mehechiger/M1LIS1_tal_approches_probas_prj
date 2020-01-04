import numpy as np
import pandas as pd
import os
import sys
from scipy.stats import anderson
from s0_load_scr import load_scr

path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]


input_ = "%sscores/" % path
output = "%sanalysis/" % path

metrics = set(d.split(".")[0] for d in os.listdir(input_) if d[-4:] == ".scr")
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]

if not os.path.isdir(output):
    os.makedirs(output)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))

    for direction in directions:
        slc = df[df.direction == direction].score

        statistic, critical_values, significance_level = anderson(slc)
        res.append({"metric": metric,
                    "direction": direction,
                    "anderson_statistic": statistic,
                    "anderson_critical_values": critical_values,
                    "anderson_significance_level": significance_level
                    })

res = pd.DataFrame(res)
res = res[["metric", "direction", "anderson_statistic",
           "anderson_critical_values", "anderson_significance_level"]]
res.to_csv("%sdirection_level_a1_anderson_test.csv" % output)


res = []

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score

            statistic, critical_values, significance_level = anderson(slc)
            res.append({"metric": metric,
                        "direction": direction,
                        "lang_pair": lang_pair,
                        "anderson_statistic": statistic,
                        "anderson_critical_values": critical_values,
                        "anderson_significance_level": significance_level
                        })


res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "direction", "anderson_statistic",
           "anderson_critical_values", "anderson_significance_level"]]
res.to_csv("%slangpair_level_a1_anderson_test.csv" % output)
