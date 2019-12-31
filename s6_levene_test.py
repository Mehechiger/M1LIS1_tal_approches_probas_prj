import numpy as np
import pandas as pd
import os
from scipy.stats import levene
from s0_load_scr import load_scr

metrics = ["da", "bleu", "terp"]
input_ = "/Users/mehec/nlp/approbas/prj/scores/"
output = "/Users/mehec/nlp/approbas/prj/analysis/"

if not os.path.isdir(output):
    os.makedirs(output)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))
    directions = set(df.direction)
    lang_pairs = set(df.lang_pair)
    cent = "trimmed" if metric == "bleu" else "median"
    statistic, pvalue = levene(
        *[df[df.direction == direction].score for direction in directions], center=cent)
    res.append({"metric": metric, "levene_statistic": statistic,
                "levene_pvalue": pvalue})

    for lang_pair in lang_pairs:
        slc = df[df.lang_pair == lang_pair].score
        statistic, pvalue = levene(
            *[df[df.direction == direction][df.lang_pair == lang_pair].score for direction in directions], center=cent)
        res.append({"metric": metric, "lang_pair": lang_pair,
                    "levene_statistic": statistic, "levene_pvalue": pvalue})

pd.DataFrame(res).to_csv("%slevene_test.csv" % output)
