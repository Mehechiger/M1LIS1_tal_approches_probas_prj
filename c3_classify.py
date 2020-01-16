import sys
import gc
import os
import json
import random
import pandas as pd
from itertools import combinations
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


def load_langpair(input_, lang_pairs):
    with open(input_, "r") as f:
        data = json.load(f)
        return {direction: {type_: [sent
                                    for lang_pair, langpair_dict in data[direction].items()
                                    for sent in langpair_dict[type_]
                                    if lang_pair in lang_pairs
                                    ]
                            for type_ in types
                            }
                for direction in directions
                }


def shuffle_datapair(datapair):
    assert len(datapair) == 2, "data not paired!"
    assert all(type(data) == list
               for data in datapair.values()
               ), "wrong data format!"
    assert len(set(len(data)
                   for data in datapair.values()
                   )) == 1, "data length not equal!"

    rand = random.randint(0, 10000)
    res = {}
    for type_, type_list in datapair.items():
        random.seed(rand)
        random.shuffle(type_list)
        res[type_] = type_list
    return res


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
train_dev_test_ratio = (3, 1, 1)

# load data from parsed data file
data_orig = load_direction_level(input_)
"""
data_orig = load_langpair(input_, ["en_ru", "ru_en"])
l = len(data_orig["reverse"]["src"])
data_orig["forward"]["src"] = data_orig["forward"]["src"][:l]
data_orig["forward"]["ref"] = data_orig["forward"]["ref"][:l]
"""
"""
"""


#features = ["ttr", "mean_word_rank", "cohesive_markers", "function_words", "puncs", "pronouns", "mean_dep_tree_depth", "pos_2_grams", "pos_3_grams", "chr_2_grams", "chr_3_grams", "positional_token_frequency"]
features = ["ttr", "puncs", "pronouns", "mean_dep_tree_depth", "pos_2_grams",
            "pos_3_grams", "chr_2_grams", "chr_3_grams", "positional_token_frequency"]

dc = Direction_classifier()

for chunk_size_coeff in range(40):
    chunk_size = 50*chunk_size_coeff

    for repeat in range(50):
        # shuffle data
        data = {direction: shuffle_datapair(direction_dict)
                for direction, direction_dict in data_orig.items()
                }

        # chunk data
        data = {direction: chunk_datapair(direction_dict, chunk_size)
                for direction, direction_dict in data.items()
                }

        # make train, dev and test
        train, dev, test = make_train_dev_test(data,
                                               train_dev_test_ratio,
                                               directions
                                               )
        print(len(train), len(dev), len(test))

        # regain RAM
        del data
        gc.collect()

        if os.path.exists("%stest_dc.json" % output):
            res = pd.read_json("%stest_dc.json" % output)
            shuffle = res.shuffle.max()
        else:
            res = pd.DataFrame(columns=["accuracy",
                                        "n_vec_dim",
                                        "n_updates",
                                        "n_passes",
                                        "n_passes_argmax",
                                        "feature",
                                        "chunk_size",
                                        "train_size",
                                        "dev_size",
                                        "test_size",
                                        "shuffle"
                                        ])
            shuffle = 0

        shuffle += 1
        dc.del_learned(True)

        dc.set_datasets(train, dev)

        # for i in range(1, len(features)):
        for i in range(1, 2):
            # for features_comb in combinations(features, i):
            for features_comb in [features, ]:
                dc.set_features(features_comb)
                dc.del_learned()
                dc.learn()
                acc = dc.evaluate(test)
                print(acc)
                print()
                res.loc[res.shape[0]+1] = pd.Series({"accuracy": acc,
                                                     "n_vec_dim": len(dc.get_w()),
                                                     "n_updates": dc.get_n_updates(),
                                                     "n_passes": dc.get_n_passes(),
                                                     "n_passes_argmax": dc.get_n_passes_argmax(),
                                                     "feature": "/".join(features_comb),
                                                     "chunk_size": chunk_size,
                                                     "train_size": len(train),
                                                     "dev_size": len(dev),
                                                     "test_size": len(test),
                                                     "shuffle": shuffle
                                                     })

        res.to_json("%stest_dc.json" % output)
