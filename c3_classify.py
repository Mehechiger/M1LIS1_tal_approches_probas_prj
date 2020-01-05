import sys
import gc
import json
import random
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


def load_langpair_level(input_):
    """
    ???
    """
    with open(input_, "r") as f:
        return {lang_pair: {direction: direction_dict[lang_pair]
                            for direction, direction_dict in json.load(f).items()
                            }
                for lang_pair in lang_pairs
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


def make_train_dev_test(data, train_dev_test_ratio):
    data = [(direction_dict["src"][i], direction_dict["ref"][i], direction)
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

directions = ["reverse", "forward"]
lang_pairs = ["ru_en", "en_ru", "ro_en", "fi_en", "de_en", "cs_en", "tr_en"]
types = ["ref", "src"]
chunk_size = 100
train_dev_test_ratio = (3, 1, 1)

# load data from parsed data file
data_orig = load_direction_level(input_)

# shuffle data
data = {direction: shuffle_datapair(direction_dict)
        for direction, direction_dict in data_orig.items()
        }


# chunk data
data = {direction: chunk_datapair(direction_dict, chunk_size)
        for direction, direction_dict in data.items()
        }

# make train, dev and test
train, dev, test = make_train_dev_test(data, train_dev_test_ratio)

# regain RAM
del data
gc.collect()


dc = Direction_classifier(train, dev)
for f in ["ttr", "mean_word_rank", "cohesive_markers", "function_words", "puncs", "pronouns", "mean_dep_tree_depth", "pos_2_grams", "pos_2_grams", "chr_3_grams", "chr_3_grams"]:
    dc.set_features([f, ])
    dc.classify(test[0][0])
    print()
