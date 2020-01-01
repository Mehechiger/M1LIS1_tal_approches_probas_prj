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

    plt.title('%s hist' % metric)
    plt.xlabel('%s score' % metric)
    plt.ylabel('count')
    plt.legend()
    plt.savefig("%shist/all_%s.jpg" % (output_plots, metric))
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

        plt.title('%s %s hist' % (lang_pair, metric))
        plt.xlabel('%s %s score' % (lang_pair, metric))
        plt.ylabel('count')
        plt.legend()
        plt.savefig("%shist/%s_%s.jpg" % (output_plots, lang_pair, metric))
        plt.clf()


res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "direction", "mean", "median", "std"]]
res.to_csv("%sa0_stats.csv" % output)
