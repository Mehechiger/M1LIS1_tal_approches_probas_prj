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

input_ = "%sdata/test_dc_all_200x.json" % path
output = "%sanalysis/" % path
output_plots = "%splots/" % path


if not os.path.isdir(output):
    os.makedirs(output)
if not os.path.isdir("%s" % output_plots):
    os.makedirs("%s" % output_plots)

data = pd.read_json(input_)

plot = sns.relplot(x='chunk_size', y='accuracy',
                   hue='feature', kind='line', data=data)
plot.savefig("%sfeatures_acc.jpg" % output_plots)


res = pd.DataFrame(columns=["feature",
                            "chunk_size",
                            "mean",
                            "median",
                            "std"
                            ])

for feature in set(data.feature):
    acc = data[data.feature == feature].accuracy
    res.loc[res.shape[0]+1] = pd.Series({"feature": feature,
                                         "mean": acc.mean(),
                                         "median": acc.median(),
                                         "std": acc.std()
                                         })

for chunk_size in set(data.chunk_size):
    acc = data[data.chunk_size == chunk_size].accuracy
    res.loc[res.shape[0]+1] = pd.Series({"chunk_size": chunk_size,
                                         "mean": acc.mean(),
                                         "median": acc.median(),
                                         "std": acc.std()
                                         })

for feature in set(data.feature):
    for chunk_size in set(data.chunk_size):
        acc = data[data.feature ==
                   feature][data.chunk_size == chunk_size].accuracy
        res.loc[res.shape[0]+1] = pd.Series({"feature": feature,
                                             "chunk_size": chunk_size,
                                             "mean": acc.mean(),
                                             "median": acc.median(),
                                             "std": acc.std()
                                             })


res.to_csv("%sca0_stats.csv" % output)
