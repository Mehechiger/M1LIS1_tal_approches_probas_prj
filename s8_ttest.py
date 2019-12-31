import pandas as pd
import os
from scipy.stats import ttest_ind
from s0_load_scr import load_scr

metrics = ["da", "bleu", "terp"]
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
equal_vars = {"da": True, "bleu": False, "terp": False}
input_ = "../scores/"
output = "../analysis/"

if not os.path.isdir(output):
    os.makedirs(output)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))

    statistic, pvalue = ttest_ind(
        *[df[df.direction == direction].score for direction in directions], equal_var=equal_vars[metric])

    res.append({"metric": metric, "ttest_statistics": statistic,
                "ttest_pvalue": pvalue})

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))
        statistic, pvalue = ttest_ind(*[df[df.direction == direction][df.lang_pair ==
                                                                      lang_pair].score for direction in directions], equal_var=equal_vars[metric])

        res.append({"metric": metric, "lang_pair": lang_pair,
                    "ttest_statistics": statistic, "ttest_pvalue": pvalue})

res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "ttest_statistics", "ttest_pvalue"]]
res.to_csv("%sa3_ttest.csv" % output)
