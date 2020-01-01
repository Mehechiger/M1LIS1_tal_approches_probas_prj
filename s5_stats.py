import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from s0_load_scr import load_scr

input_ = "../scores/"
output = "../analysis/"
output_plots = "../plots/"

metrics = set(d.split(".")[0] for d in os.listdir(input_) if d[-4:] == ".scr")
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]

if not os.path.isdir(output):
    os.makedirs(output)
if not os.path.isdir("%shist/" % output_plots):
    os.makedirs("%shist/" % output_plots)


res = pd.DataFrame(columns=["lang_pair", "metric", "direction",
                            "mean", "diff_mean", "median", "diff_median", "std",
                            "mean_norm", "diff_mean_norm", "median_norm", "diff_median_norm", "std_norm"
                            ])

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))
    df_norm = df.copy()
    df_norm.score = (df_norm.score-df_norm.score.min()) / \
        (df_norm.score.max()-df_norm.score.min())

    plot = sns.FacetGrid(df_norm, hue="direction", margin_titles=True)
    plot.map(sns.distplot, 'score')
    plot.add_legend()
    plot.set_xlabels('%s score (normalized)' % metric)
    plot.savefig("%shist/%s.jpg" % (output_plots, metric))

    plot = sns.FacetGrid(df_norm, col='lang_pair', col_wrap=3,
                         hue="direction", margin_titles=True)
    plot.map(sns.distplot, 'score')
    plot.add_legend()
    plot.set_xlabels('%s score (normalized)' % metric)
    plot.savefig("%shist/%s_langpair_wide.jpg" % (output_plots, metric))

    for direction in directions:
        slc = df[df.direction == direction].score
        #slc_norm = (slc-slc.min())/(slc.max()-slc.min())
        slc_norm = df_norm[df_norm.direction == direction].score

        res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                             "direction": direction,
                                             "mean": slc.mean(),
                                             "median": slc.median(),
                                             "std": slc.std(),
                                             "mean_norm": slc_norm.mean(),
                                             "median_norm": slc_norm.median(),
                                             "std_norm": slc_norm.std()
                                             })

    slc = df.score
    slc0 = df[df.direction == directions[0]].score
    slc0_norm = (slc0-slc.min())/(slc.max()-slc.min())
    slc1 = df[df.direction == directions[1]].score
    slc1_norm = (slc1-slc.min())/(slc.max()-slc.min())
    res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                         "diff_mean": slc0.mean()-slc1.mean(),
                                         "diff_median": slc0.median()-slc1.median(),
                                         "diff_mean_norm": slc0_norm.mean()-slc1_norm.mean(),
                                         "diff_median_norm": slc0_norm.median()-slc1_norm.median()
                                         })


for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score
            slc_norm = (slc-slc.min())/(slc.max()-slc.min())

            res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                                 "direction": direction,
                                                 "lang_pair": lang_pair,
                                                 "mean": slc.mean(),
                                                 "median": slc.median(),
                                                 "std": slc.std(),
                                                 "mean_norm": slc_norm.mean(),
                                                 "median_norm": slc_norm.median(),
                                                 "std_norm": slc_norm.std()
                                                 })

        slc = df[df.lang_pair == lang_pair].score
        slc0 = df[df.lang_pair ==
                  lang_pair][df.direction == directions[0]].score
        slc0_norm = (slc0-slc.min())/(slc.max()-slc.min())
        slc1 = df[df.lang_pair ==
                  lang_pair][df.direction == directions[1]].score
        slc1_norm = (slc1-slc.min())/(slc.max()-slc.min())
        res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                             "lang_pair": lang_pair,
                                             "diff_mean": slc0.mean()-slc1.mean(),
                                             "diff_median": slc0.median()-slc1.median(),
                                             "diff_mean_norm": slc0_norm.mean()-slc1_norm.mean(),
                                             "diff_median_norm": slc0_norm.median()-slc1_norm.median()
                                             })


res.to_csv("%sa0_stats.csv" % output)
