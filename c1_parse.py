import sys
import spacy
import stanfordnlp
import json
from collections import defaultdict

path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sdata/data_regen.json" % path
output = "%sdata/" % path
stanfordnlp_models_dir = "%sstanfordnlp" % path


en = spacy.load("en_core_web_sm")
de = spacy.load("de_core_news_sm")
for lang in ["ro", "ru", "tr", "cs", "fi"]:
    globals()[lang] = stanfordnlp.Pipeline(lang=lang,
                                           models_dir=stanfordnlp_models_dir,
                                           processors='tokenize,pos,lemma,depparse'
                                           )


with open(input_, "r") as f:
    data = json.load(f)

parsed = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: list())))

for direction, direction_dict in data.items():
    for lang_pair, langpair_list in direction_dict.items():
        langs = [("src", lang_pair.split("_")[0]),
                 ("ref", lang_pair.split("_")[1])
                 ]
        for it in langpair_list:
            for type_, lang in langs:
                sent = it[type_]
                if lang == "en" or lang == "de":
                    doc = globals()[lang](sent)
                    parsed[direction][lang_pair][type_].append([{"text": token.text,
                                                                 "lemma": token.lemma_,
                                                                 "pos": token.pos_,
                                                                 "tag": token.tag_,
                                                                 "dep": token.dep_,
                                                                 "head": token.head.i if token.dep_ != "ROOT" else -1
                                                                 }
                                                                for token in doc
                                                                ])
                else:
                    doc = globals()[lang](sent)
                    tmp = [{"text": token.text,
                            "lemma": token.lemma,
                            "pos": token.upos,
                            "tag": token.xpos,
                            "dep": token.dependency_relation,
                            "head": token.governor-1
                            }
                           for token in doc.sentences[0].words
                           ]
                    len_ = len(doc.sentences)
                    if len_ > 1:
                        head = [ind
                                for ind, it in enumerate(tmp)
                                if it["head"] == -1
                                ][0]
                        for i in range(1, len_):
                            len_prevs = len(tmp)
                            tmp.extend([{"text": token.text,
                                         "lemma": token.lemma,
                                         "pos": token.upos,
                                         "tag": token.xpos,
                                         "dep": token.dependency_relation,
                                         "head": token.governor+len_prevs-1 if token.governor != 0 else head
                                         }
                                        for token in doc.sentences[i].words
                                        ])
                    parsed[direction][lang_pair][type_].append(tmp)


with open("%sdata_parsed.json" % output, "w") as f:
    json.dump(parsed, f)
