import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from scipy.stats import anderson
from s0_load_scr import load_scr

metrics = ["da", "bleu", "terp"]
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
input_ = "../scores/"
output_direction = "../analysis/a1_is_norm_direction_level/"
output_langpair = "../analysis/a1_is_norm_langpair_level/"

if not os.path.isdir(output_direction):
    os.makedirs(output_direction)
if not os.path.isdir(output_langpair):
    os.makedirs(output_langpair)

res_metric = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))

    for direction in directions:
        slc = df[df.direction == direction].score
        plt.title('%s %s hist' % (metric, direction))
        plt.xlabel('%s score' % metric)
        plt.ylabel('count')
        slc.hist(bins=50)
        plt.savefig("%s%s_%s_hist.jpg" % (output_direction, metric, direction))
        plt.clf()

        statistic, critical_values, significance_level = anderson(slc)
        res_metric.append({"metric": metric, "direction": direction, "anderson_statistic": statistic,
                           "anderson_critical_values": critical_values, "anderson_significance_level": significance_level})

res_metric = pd.DataFrame(res_metric)
res_metric = res_metric[["metric", "direction", "anderson_statistic",
                         "anderson_critical_values", "anderson_significance_level"]]
res_metric.to_csv("%sis_norm.csv" % output_direction)


for lang_pair in lang_pairs:
    res_langpair = []

    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score
            plt.title('%s %s %s hist' % (lang_pair, metric, direction))
            plt.xlabel('%s %s score' % (lang_pair, metric))
            plt.ylabel('count')
            slc.hist(bins=50)
            plt.savefig("%s%s_%s_%s_hist.jpg" %
                        (output_langpair, lang_pair, metric, direction))
            plt.clf()

            statistic, critical_values, significance_level = anderson(slc)
            res_langpair.append({"metric": metric, "direction": direction, "lang_pair": lang_pair, "anderson_statistic": statistic,
                                 "anderson_critical_values": critical_values, "anderson_significance_level": significance_level})

    res_langpair = pd.DataFrame(res_langpair)
    res_langpair = res_langpair[["lang_pair", "metric", "direction",
                                 "anderson_statistic", "anderson_critical_values", "anderson_significance_level"]]
    res_langpair.to_csv("%s%s_is_norm.csv" %
                        (output_langpair, lang_pair))
