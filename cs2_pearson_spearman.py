import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import sys


path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sdata/test_dc_V17_all+one_50x.json" % path
output = "%sanalysis/" % path
output_plots = "%splots/" % path
to_test = {"ttr/puncs/pronouns/mean_dep_tree_depth/pos_2_grams/pos_3_grams/chr_2_grams/chr_3_grams/positional_token_frequency": "all"}


if not os.path.isdir(output):
    os.makedirs(output)
if not os.path.isdir("%s" % output_plots):
    os.makedirs("%s" % output_plots)

data = pd.read_json(input_)


res = pd.DataFrame(columns=["feature",
                            "pearson_coeff",
                            "spearman_coeff"
                            ])

for feature in set(data.feature):
    if feature not in to_test:
        continue

    slice_ = data[data.feature == feature]

    plot = sns.jointplot(x="chunk_size", y="accuracy", data=slice_, kind="kde")
    plt.title(to_test[feature])
    plot.savefig("%spearson_spearman.jpg" % output_plots)

    acc = slice_.accuracy
    chunk_size = slice_.chunk_size
    res.loc[res.shape[0]+1] = pd.Series({"feature": feature,
                                         "pearson_coeff": chunk_size.corr(acc, method="pearson"),
                                         "spearman_coeff": chunk_size.corr(acc, method="spearman")
                                         })

res.to_csv("%sca1_pearson_spearman.csv" % output)
