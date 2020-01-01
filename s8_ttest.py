import pandas as pd
import os
from collections import defaultdict
from scipy.stats import ttest_ind
from s0_load_scr import load_scr

input_ = "../scores/"
output = "../analysis/"

metrics = set(d.split(".")[0] for d in os.listdir(input_) if d[-4:] == ".scr")
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
equal_vars = defaultdict(lambda: False,
                         {"da": True,
                          ("en_ru", "da"): True,
                          ("ru_en", "bleu"): True,
                          ("fi_en", "da"): True,
                          ("cs_en", "terp"): True,
                          ("ro_en", "terp"): True,
                          ("de_en", "bleu"): True,
                          ("tr_en", "bleu"): True,
                          ("tr_en", "terp"): True
                          }
                         )

if not os.path.isdir(output):
    os.makedirs(output)

res = []

for metric in metrics:
    df = load_scr("%s%s..seg.scr" % (input_, metric))

    statistic, pvalue = ttest_ind(*[df[df.direction == direction].score
                                    for direction in directions
                                    ],
                                  equal_var=equal_vars[metric]
                                  )

    res.append({"metric": metric,
                "ttest_statistics": statistic,
                "ttest_pvalue": pvalue
                })

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))
        statistic, pvalue = ttest_ind(*[df[df.direction == direction][df.lang_pair == lang_pair].score
                                        for direction in directions
                                        ],
                                      equal_var=equal_vars[(lang_pair, metric)]
                                      )

        res.append({"metric": metric,
                    "lang_pair": lang_pair,
                    "ttest_statistics": statistic,
                    "ttest_pvalue": pvalue
                    })

res = pd.DataFrame(res)
res = res[["lang_pair", "metric", "ttest_statistics", "ttest_pvalue"]]
res.to_csv("%sa3_ttest.csv" % output)
