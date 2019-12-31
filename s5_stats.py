import numpy as np
import pandas as pd
import os
from s0_load_scr import load_scr

metrics = ["da", "bleu", "terp"]
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
input_ = "../scores/"
output = "../analysis/"

if not os.path.isdir(output):
    os.makedirs(output)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))

    for direction in directions:
        slc = df[df.direction == direction].score

        res.append({"metric": metric, "direction": direction, "mean": slc.mean(
        ), "median": slc.median(), "std": slc.std()})

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))

        for direction in directions:
            slc = df[df.lang_pair == lang_pair][df.direction == direction].score

            res.append({"metric": metric, "direction": direction, "lang_pair": lang_pair,
                        "mean": slc.mean(), "median": slc.median(), "std": slc.std()})


res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "direction", "mean", "median", "std"]]
res.to_csv("%sa0_stats.csv" % output)
