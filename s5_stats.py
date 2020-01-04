import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import sys
from s0_load_scr import load_scr


def vertical_mean_line(x, vars_, **kwargs):
    """
    source: https://stackoverflow.com/a/44961245
    """
    plt.axvline(x.mean(), linestyle="--", color=kwargs['color'])
    txkw = dict(size=7, color=kwargs['color'], rotation=90)
    tx = "mean: {:.2f}, std: {:.2f}".format(x.mean(), x.std())
    plt.text(x.mean()+0.005, 0.052, tx, **txkw)


path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sscores/" % path
output = "%sanalysis/" % path
output_plots = "%splots/" % path

metrics = set(d.split(".")[0] for d in os.listdir(input_) if d[-4:] == ".scr")
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]


if not os.path.isdir(output):
    os.makedirs(output)
if not os.path.isdir("%s" % output_plots):
    os.makedirs("%s" % output_plots)


res = pd.DataFrame(columns=["metric", "direction", "sample_size",
                            "mean", "median", "std",
                            "mean_norm", "median_norm", "std_norm"
                            ])

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))
    df_norm = df.copy()
    if metric[:3] == "ter":
        df_norm.score = -df_norm.score
    df_norm.score = (df_norm.score-df_norm.score.min()) / \
        (df_norm.score.max()-df_norm.score.min())

    plot = sns.FacetGrid(df_norm,
                         hue="direction",
                         hue_order=directions,
                         margin_titles=True,
                         height=3.2,
                         aspect=3)
    plot.map(sns.distplot, 'score', bins=50)
    plot.map(vertical_mean_line, 'score', vars_=directions)
    plot.add_legend()
    plot.set(xlim=(0, 1))
    plot.set_xlabels('%s score (normalized)' % metric)
    plot.savefig("%sdirection_level_%s.jpg" % (output_plots, metric))

    plot = sns.FacetGrid(df_norm,
                         col='lang_pair',
                         col_order=lang_pairs,
                         col_wrap=2,
                         hue="direction",
                         hue_order=directions,
                         margin_titles=True,
                         height=3.2,
                         aspect=3)
    plot.map(sns.distplot, 'score', bins=50)
    plot.map(vertical_mean_line, 'score', vars_=directions)
    plot.add_legend()
    plot.set(xlim=(0, 1))
    plot.set_xlabels('%s score (normalized)' % metric)
    plot.savefig("%slangpair_level_%s.jpg" % (output_plots, metric))

    for direction in directions:
        slc = df[df.direction == direction].score
        slc_norm = df_norm[df_norm.direction == direction].score

        res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                             "direction": direction,
                                             "sample_size": slc.shape[0],
                                             "mean": slc.mean(),
                                             "median": slc.median(),
                                             "std": slc.std(),
                                             "mean_norm": slc_norm.mean(),
                                             "median_norm": slc_norm.median(),
                                             "std_norm": slc_norm.std()
                                             })

    slc = df.score
    slc0 = df[df.direction == directions[0]].score
    slc0_norm = df_norm[df_norm.direction == directions[0]].score
    slc1 = df[df.direction == directions[1]].score
    slc1_norm = df_norm[df_norm.direction == directions[1]].score
    res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                         "direction": "(difference)",
                                         "mean": slc0.mean()-slc1.mean(),
                                         "median": slc0.median()-slc1.median(),
                                         "mean_norm": slc0_norm.mean()-slc1_norm.mean(),
                                         "median_norm": slc0_norm.median()-slc1_norm.median()
                                         })

res.to_csv("%sdirection_level_a0_stats.csv" % output)

res = pd.DataFrame(columns=["lang_pair", "metric", "direction", "sample_size",
                            "mean", "median", "std",
                            "mean_norm", "median_norm", "std_norm"
                            ])

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))
        df_norm = df.copy()
        if metric[:3] == "ter":
            df_norm.score = -df_norm.score
        df_norm.score = (df_norm.score-df_norm.score.min()) / \
            (df_norm.score.max()-df_norm.score.min())

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score
            slc_norm = df_norm[df_norm.lang_pair ==
                               lang_pair][df_norm.direction == direction].score

            res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                                 "direction": direction,
                                                 "lang_pair": lang_pair,
                                                 "sample_size": slc.shape[0],
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
        slc0_norm = df_norm[df_norm.lang_pair ==
                            lang_pair][df_norm.direction == directions[0]].score
        slc1 = df[df.lang_pair ==
                  lang_pair][df.direction == directions[1]].score
        slc1_norm = df_norm[df_norm.lang_pair ==
                            lang_pair][df_norm.direction == directions[1]].score
        res.loc[res.shape[0]+1] = pd.Series({"metric": metric,
                                             "direction": "(difference)",
                                             "lang_pair": lang_pair,
                                             "diff_mean": slc0.mean()-slc1.mean(),
                                             "diff_median": slc0.median()-slc1.median(),
                                             "diff_mean_norm": slc0_norm.mean()-slc1_norm.mean(),
                                             "diff_median_norm": slc0_norm.median()-slc1_norm.median()
                                             })

res.to_csv("%slangpair_level_a0_stats.csv" % output)
