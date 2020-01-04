import sys
#from collections import Counter, defaultdict
#from math import log
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
        res[type_] = random.shuffle(type_list)
    return res


def chunk_data(data, chunk_size):
    chunks = []
    count = chunk_size
    ind = -1
    for sent in data:
        if count >= chunk_size:
            count = 0
            ind += 1
            chunks[ind] = []
        chunks[ind].append(sent)
        count += len(sent)
    return chunks


def make_train_dev_test(data, train_dev_test_ratio):
    ratios = (ratio/sum(train_dev_test_ratio)
              for ratio in train_dev_test_ratio
              )


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

data_orig = load_direction_level(input_)
data = {direction: shuffle_datapair(direction_dict)
        for direction, direction_dict in data_orig.items()
        }
data = {direction: {type_: chunk_data(type_list, chunk_size)
                    for type_, type_list in direction_dict.items()
                    }
        for direction, direction_dict in data.items()
        }

dc = Direction_classifier(1, 1)
dc.set_features(["pronouns", ])
