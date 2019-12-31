import pandas as pd
import os
from scipy.stats import ttest_ind
from s0_load_scr import load_scr

input_ = "../scores/"
output = "../analysis/"

metrics = set(d.split(".")[0] for d in os.listdir(input_) if d[-4:] == ".scr")
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
equal_vars = {"da": True, "bleu": False, "terp": False, ("en_ru", "da"): True, ("en_ru", "bleu"): False, ("en_ru", "terp"): False, ("ru_en", "da"): False, ("ru_en", "bleu"): True, ("ru_en", "terp"): False, ("fi_en", "da"): True, ("fi_en", "bleu"): False, ("fi_en", "terp"): False, (
    "cs_en", "da"): False, ("cs_en", "bleu"): False, ("cs_en", "terp"): True, ("ro_en", "da"): False, ("ro_en", "bleu"): False, ("ro_en", "terp"): True, ("de_en", "da"): False, ("de_en", "bleu"): True, ("de_en", "terp"): False, ("tr_en", "da"): False, ("tr_en", "bleu"): True, ("tr_en", "terp"): True}

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
                                                                      lang_pair].score for direction in directions], equal_var=equal_vars[(lang_pair, metric)])

        res.append({"metric": metric, "lang_pair": lang_pair,
                    "ttest_statistics": statistic, "ttest_pvalue": pvalue})

res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "ttest_statistics", "ttest_pvalue"]]
res.to_csv("%sa3_ttest.csv" % output)
