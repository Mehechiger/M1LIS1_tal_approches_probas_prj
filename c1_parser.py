import spacy
import json
from collections import defaultdict

input_ = "/Users/mehec/nlp/approbas/prj/data/data_regen.json"
output = "/Users/mehec/nlp/approbas/prj/data/"


en = spacy.load("en_core_web_sm")
de = spacy.load("de_core_news_sm")

with open(input_, "r") as f:
    data = json.load(f)

parsed = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: list())))
d_type = {"ref": "tgt_lang", "src": "src_lang"}

for direction, direction_dict in data.items():
    for lang_pair, langpair_list in direction_dict.items():
        for it in langpair_list:
            for type_ in d_type:
                sent = it[type_]
                lang = it[d_type[type_]]
                if lang == "en" or lang == "de":
                    doc = globals()[lang](sent)
                    parsed[direction][lang_pair][type_].append([{"text": token.text,
                                                                 "lemma": token.lemma_,
                                                                 "pos": token.pos_,
                                                                 "tag": token.tag_,
                                                                 "dep": token.dep_,
                                                                 "shape": token.shape_,
                                                                 "alpha": token.is_alpha,
                                                                 "stop": token.is_stop,
                                                                 "head": token.head.i if token.dep_ != "ROOT" else 0
                                                                 }
                                                                for token in doc
                                                                ])
                else:
                    pass

with open("%sdata_parsed.json" % output, "w") as f:
    json.dump(parsed, f)
