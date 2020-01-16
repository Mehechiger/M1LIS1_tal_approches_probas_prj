import sys
import gc
import os
import json
import random
import pandas as pd
from collections import defaultdict
from c2_Direction_classifier import Direction_classifier


def load_direction_level(input_):
    with open(input_, "r") as f:
        data = json.load(f)
        return {direction: {type_: [sent
                                    for langpair_dict in data[direction].values()
                                    for sent in langpair_dict[type_]
                                    ]
                            for type_ in types
                            }
                for direction in directions
                }


def chunk_datapair(datapair, chunk_size):
    assert len(datapair) == 2, "data not paired!"
    assert all(type(data) == list
               for data in datapair.values()
               ), "wrong data format!"
    assert len(set(len(data)
                   for data in datapair.values()
                   )) == 1, "data length not equal!"

    chunks_pair = {type_: [] for type_ in datapair}
    count = chunk_size
    ind = -1
    for i in range(len(datapair["src"])):
        if count >= chunk_size:
            count = 0
            ind += 1
            for type_ in chunks_pair:
                chunks_pair[type_].append([])
        for type_ in chunks_pair:
            chunks_pair[type_][ind].append(datapair[type_][i])
        count += min(len(datapair["src"][i]), len(datapair["ref"][i]))
    return {type_: chunks_pair[type_] for type_ in datapair}


def make_train_dev_test(data, train_dev_test_ratio, label_dict):
    data = [(direction_dict["src"][i], direction_dict["ref"][i], label_dict[direction])
            for direction, direction_dict in data.items()
            for i in range(len(direction_dict["src"]))
            ]
    lens = [ratio*len(data)/sum(train_dev_test_ratio)
            for ratio in train_dev_test_ratio
            ]

    # shuffle chunks of data
    random.shuffle(data)
    datasets = [[]]
    i = 0
    count = 0
    for it in data:
        if count >= lens[i]:
            count = 0
            i += 1
            datasets.append([])
        datasets[i].append(it)
        count += 1
    return datasets


path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%s/data/data_parsed.json" % path
output = "%s/data/" % path

directions = {"reverse": -1, "forward": 1}
lang_pairs = ["ru_en", "en_ru", "ro_en", "fi_en", "de_en", "cs_en", "tr_en"]
types = ["ref", "src"]
train_dev_test_ratio = (1, 0, 0)

# load data from parsed data file
data = load_direction_level(input_)

dc = Direction_classifier()

chunk_size = 9999999

# chunk data
data = {direction: chunk_datapair(direction_dict, chunk_size)
        for direction, direction_dict in data.items()
        }

# make train, dev and test
train = make_train_dev_test(data,
                            train_dev_test_ratio,
                            directions
                            )
print(len(train))


src, ref, pred = list(zip(*train[0]))
o = []
t = []
for i in range(len(pred)):
    if pred[i] == 1:
        o.extend(src[i])
        t.extend(ref[i])
    else:
        o.extend(ref[i])
        t.extend(src[i])

features = ["puncs", "pos_2_grams", "pos_3_grams",
            "chr_2_grams", "chr_3_grams", "positional_token_frequency"]
for feature in features:
    res = {}
    dc.set_features([feature, ])
    ft = feature
    feature = feature.replace("2", "n")
    feature = feature.replace("3", "n")
    res["original"] = eval("dc.%s" % feature)(o, "")
    res["translated"] = eval("dc.%s" % feature)(t, "")
    res = pd.DataFrame(res)
    res.to_csv("%sfeature_all_%s.csv" % (output, ft))


"""
"""

data = load_direction_level(input_)

dc = Direction_classifier()

chunk_size = 0

data = {direction: chunk_datapair(direction_dict, chunk_size)
        for direction, direction_dict in data.items()
        }

train = make_train_dev_test(data,
                            train_dev_test_ratio,
                            directions
                            )
print(len(train))

src, ref, pred = list(zip(*train[0]))
o = []
t = []
for i in range(len(pred)):
    if pred[i] == 1:
        o.extend(src[i])
        t.extend(ref[i])
    else:
        o.extend(ref[i])
        t.extend(src[i])

features3 = ["ttr", "pronouns", "mean_dep_tree_depth"]
for feature in features3:
    res = {}
    dc.set_features([feature, ])
    reso = []
    rest = []
    for oo in o:
        tmp = [v for v in eval("dc.%s" % feature)([oo, ], "").values()]
        reso.append(tmp[0] if tmp else 0)
    res["original"] = reso
    for tt in t:
        tmp = [v for v in eval("dc.%s" % feature)([tt, ], "").values()]
        rest.append(tmp[0] if tmp else 0)
    res["translated"] = rest
    res = pd.DataFrame(res).fillna(0)
    res.to_csv("%sfeature_sentwise_%s.csv" % (output, feature))
