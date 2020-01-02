import pandas as pd
import os
from collections import defaultdict
from scipy.stats import ttest_ind, t
from s0_load_scr import load_scr

input_ = "../scores/"
output = "../analysis/"

metrics = set(d.split(".")[0] for d in os.listdir(input_) if d[-4:] == ".scr")
directions = ["forward", "reverse"]
lang_pairs = ["en_ru", "ru_en", "fi_en", "cs_en", "ro_en", "de_en", "tr_en"]
equal_vars = defaultdict(lambda: False,
                         {"da": True,
                          ("en_ru", "da"): True,
                          ("fi_en", "da"): True,
                          ("cs_en", "terp"): True,
                          ("ro_en", "terp"): True,
                          ("ro_en", "da"): True,
                          ("de_en", "terp"): True,
                          ("de_en", "da"): True,
                          ("tr_en", "da"): True,
                          ("tr_en", "terp"): True
                          }
                         )
confidence = 0.95

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

    mean0 = df[df.direction == directions[0]].score.mean()
    mean1 = df[df.direction == directions[1]].score.mean()
    std0 = df[df.direction == directions[0]].score.std()
    std1 = df[df.direction == directions[1]].score.std()
    a0 = df[df.direction == directions[0]].score.shape[0]
    a1 = df[df.direction == directions[1]].score.shape[0]
    se = df.score.sem()

    CI = t.interval(confidence, a0+a1-1, mean0-mean1, se)
    cohensd = (mean0-mean1)/(((a0-1)*std0**2+(a1-1)*std1**2)/(a0+a1))**0.5

    res.append({"metric": metric,
                "ttest_statistics": statistic,
                "ttest_pvalue": pvalue,
                "%d%%_ci" % (confidence*100): CI,
                "cohen's_d": cohensd
                })

res = pd.DataFrame(res)
res = res[["metric",
           "ttest_statistics",
           "ttest_pvalue",
           "%d%%_ci" % (confidence*100),
           "cohen's_d"
           ]]
res.to_csv("%sdirection_level_a3_ttest_confidence_cohensd.csv" % output)


res = []

for lang_pair in lang_pairs:
    for metric in metrics:
        df = load_scr("%s%s..seg.scr" % (input_, metric))
        statistic, pvalue = ttest_ind(*[df[df.direction == direction][df.lang_pair == lang_pair].score
                                        for direction in directions
                                        ],
                                      equal_var=equal_vars[(lang_pair, metric)]
                                      )

        mean0 = df[df.lang_pair == lang_pair][df.direction ==
                                              directions[0]].score.mean()
        mean1 = df[df.lang_pair == lang_pair][df.direction ==
                                              directions[1]].score.mean()
        std0 = df[df.lang_pair == lang_pair][df.direction ==
                                             directions[0]].score.std()
        std1 = df[df.lang_pair == lang_pair][df.direction ==
                                             directions[1]].score.std()
        a0 = df[df.lang_pair == lang_pair][df.direction ==
                                           directions[0]].shape[0]
        a1 = df[df.lang_pair == lang_pair][df.direction ==
                                           directions[1]].shape[0]
        se = df[df.lang_pair == lang_pair].score.sem()
        CI = t.interval(confidence, a0+a1-1, mean0-mean1, se)
        cohensd = (mean0-mean1)/(((a0-1)*std0**2+(a1-1)*std1**2)/(a0+a1))**0.5

        res.append({"metric": metric,
                    "lang_pair": lang_pair,
                    "ttest_statistics": statistic,
                    "ttest_pvalue": pvalue,
                    "%d%%_ci" % (confidence*100): CI,
                    "cohen's_d": cohensd
                    })

res = pd.DataFrame(res)
res = res[["lang_pair",
           "metric",
           "ttest_statistics",
           "ttest_pvalue",
           "%d%%_ci" % (confidence*100),
           "cohen's_d"]]
res.to_csv("%slangpair_level_a3_ttest_confidence_cohensd.csv" % output)
