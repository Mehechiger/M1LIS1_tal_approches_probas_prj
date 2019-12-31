import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from scipy.stats import anderson
from s0_load_scr import load_scr

metrics = ["da", "bleu", "terp"]
input_ = "/Users/mehec/nlp/approbas/prj/scores/"
output = "/Users/mehec/nlp/approbas/prj/analysis/"
output_plot = "/Users/mehec/nlp/approbas/prj/analysis/plot/"

if not os.path.isdir(output):
    os.makedirs(output)
if not os.path.isdir(output_plot):
    os.makedirs(output_plot)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))
    directions = set(df.direction)
    lang_pairs = set(df.lang_pair)
    for direction in directions:
        slc = df[df.direction == direction].score
        slc.hist(bins=50).get_figure().savefig(
            "%s%s_%s_hist.jpg" % (output_plot, metric, direction))
        plt.clf()
        statistic, critical_values, significance_level = anderson(slc)
        res.append({"metric": metric, "direction": direction, "anderson_statistic": statistic,
                    "anderson_critical_values": critical_values, "anderson_significance_level": significance_level})

        for lang_pair in lang_pairs:
            slc = df[df.direction == direction][df.lang_pair == lang_pair].score
            slc.hist(bins=50).get_figure().savefig(
                "%s%s_%s_%s_hist.jpg" % (output_plot, metric, direction, lang_pair))
            plt.clf()
            statistic, critical_values, significance_level = anderson(slc)
            res.append({"metric": metric, "direction": direction, "lang_pair": lang_pair, "anderson_statistic": statistic,
                        "anderson_critical_values": critical_values, "anderson_significance_level": significance_level})

pd.DataFrame(res).to_csv("%sis_norm.csv" % output)
