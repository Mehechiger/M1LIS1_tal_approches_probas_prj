import matplotlib.pyplot as plt
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


res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))

    for direction in directions:
        slc = df[df.direction == direction].score

        plt.hist(slc, bins=50, label=direction, alpha=0.4)

        res.append({"metric": metric,
                    "direction": direction,
                    "mean": slc.mean(),
                    "median": slc.median(),
                    "std": slc.std()
                    })

    res.append({"metric": metric,
                "diff_mean": df[df.direction == directions[0]].score.mean()-df[df.direction == directions[1]].score.mean(),
                "diff_median": df[df.direction == directions[0]].score.median()-df[df.direction == directions[1]].score.median()
                })

    plt.title('%s hist' % metric)
    plt.xlabel('%s score' % metric)
    plt.ylabel('count')
    plt.legend()
    plt.savefig("%shist/all_%s.jpg" % (output_plots, metric))
    plt.clf()

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))
    df.score = (df.score-df.score.min())/(df.score.max()-df.score.min())

    for direction in directions:
        slc = df[df.direction == direction].score

        plt.hist(slc, bins=50, label=direction, alpha=0.2)

        res.append({"metric": metric,
                    "direction": direction,
                    "norm_mean": slc.mean(),
                    "norm_median": slc.median(),
                    "norm_std": slc.std()
                    })

    res.append({"metric": metric,
                "diff_norm_mean": df[df.direction == directions[0]].score.mean()-df[df.direction == directions[1]].score.mean(),
                "diff_norm_median": df[df.direction == directions[0]].score.median()-df[df.direction == directions[1]].score.median()
                })

plt.title('all hist')
plt.xlabel('all scores')
plt.ylabel('count')
plt.legend()
plt.savefig("%shist/all_all.jpg" % output_plots)
plt.clf()

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score

            plt.hist(slc, bins=50, label=direction, alpha=0.4)

            res.append({"metric": metric,
                        "direction": direction,
                        "lang_pair": lang_pair,
                        "mean": slc.mean(),
                        "median": slc.median(),
                        "std": slc.std()
                        })

        res.append({"metric": metric,
                    "lang_pair": lang_pair,
                    "diff_mean": df[df.direction == directions[0]].score.mean()-df[df.direction == directions[1]].score.mean(),
                    "diff_median": df[df.direction == directions[0]].score.median()-df[df.direction == directions[1]].score.median()
                    })

        plt.title('%s %s hist' % (lang_pair, metric))
        plt.xlabel('%s %s score' % (lang_pair, metric))
        plt.ylabel('count')
        plt.legend()
        plt.savefig("%shist/%s_%s.jpg" % (output_plots, lang_pair, metric))
        plt.clf()

    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))
        df.score = (df.score-df.score.min())/(df.score.max()-df.score.min())

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score

            plt.hist(slc, bins=50, label=direction, alpha=0.2)

            res.append({"metric": metric,
                        "direction": direction,
                        "lang_pair": lang_pair,
                        "norm_mean": slc.mean(),
                        "norm_median": slc.median(),
                        "norm_std": slc.std()
                        })

        res.append({"metric": metric,
                    "lang_pair": lang_pair,
                    "diff_norm_mean": df[df.direction == directions[0]].score.mean()-df[df.direction == directions[1]].score.mean(),
                    "diff_norm_median": df[df.direction == directions[0]].score.median()-df[df.direction == directions[1]].score.median()
                    })

    plt.title('%s all hist' % lang_pair)
    plt.xlabel('%s all score' % lang_pair)
    plt.ylabel('count')
    plt.legend()
    plt.savefig("%shist/%s_all.jpg" % (output_plots, lang_pair))
    plt.clf()


res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "direction",
           "mean", "diff_mean", "median", "diff_median", "std",
           "norm_mean", "diff_norm_mean", "norm_median", "diff_norm_median"
           ]]
res.to_csv("%sa0_stats.csv" % output)
