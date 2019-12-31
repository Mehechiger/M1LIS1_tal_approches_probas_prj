import numpy as np
import pandas as pd
import os
from scipy.stats import levene
from s0_load_scr import load_scr

metrics = ["da", "bleu", "terp"]
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
cents = {"da": "median", "bleu": "trimmed", "terp": "median"}
input_ = "../scores/"
output = "../analysis/"

if not os.path.isdir(output):
    os.makedirs(output)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))
    statistic, pvalue = levene(
        *[df[df.direction == direction].score for direction in directions], center=cents[metric])
    res.append({"metric": metric, "levene_statistic": statistic,
                "levene_pvalue": pvalue})

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))

        slc = df[df.lang_pair == lang_pair].score
        statistic, pvalue = levene(
            *[df[df.direction == direction][df.lang_pair == lang_pair].score for direction in directions], center=cents[metric])
        res.append({"metric": metric, "lang_pair": lang_pair,
                    "levene_statistic": statistic, "levene_pvalue": pvalue})

res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "levene_statistic", "levene_pvalue"]]
res.to_csv("%sa2_levene_test.csv" % output)
