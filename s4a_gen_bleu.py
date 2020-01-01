import json
import re
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

input_ = "../data/data_regen.json"
output = "../scores/"

bleu_weights = (1, 0, 0, 0)
bleu_autoreweigh = True

with open(input_, "r") as f:
    data_regen = json.load(f)

punc = re.compile('[,…` .[•»/:#‘’!(;"?”)+«“\]]')

nist_seg = "\n".join("\t".join([direction,
                                "",
                                lang_pair,
                                str(ind),
                                str(sentence_bleu([list(filter(None,
                                                               re.split(punc, it["ref"]))), ],
                                                  list(filter(None,
                                                              re.split(punc, it["hyp"]))
                                                       ),
                                                  weights=bleu_weights,
                                                  auto_reweigh=bleu_autoreweigh
                                                  ))
                                ])
                     for direction, direction_dict in data_regen.items()
                     for lang_pair, langpair_list in direction_dict.items()
                     for ind, it in enumerate(langpair_list)
                     )

nist_doc = "\n".join("\t".join([direction,
                                "",
                                lang_pair,
                                str(corpus_bleu([[list(filter(None,
                                                              re.split(punc, it["ref"]))), ]
                                                 for it in langpair_list
                                                 ],
                                                [list(filter(None,
                                                             re.split(punc, it["hyp"])))
                                                 for it in langpair_list
                                                 ],
                                                weights=bleu_weights,
                                                auto_reweigh=bleu_autoreweigh
                                                ))
                                ])
                     for direction, direction_dict in data_regen.items()
                     for lang_pair, langpair_list in direction_dict.items()
                     )

nist_sys = "\n".join("\t".join([direction,
                                "",
                                str(corpus_bleu([[list(filter(None,
                                                              re.split(punc, it["ref"]))), ]
                                                 for langpair_list in direction_dict.values()
                                                 for it in langpair_list
                                                 ],
                                                [list(filter(None,
                                                             re.split(punc, it["hyp"])))
                                                 for langpair_list in direction_dict.values()
                                                 for it in langpair_list
                                                 ],
                                                weights=bleu_weights,
                                                auto_reweigh=bleu_autoreweigh
                                                ))
                                ])
                     for direction, direction_dict in data_regen.items()
                     )

with open("%sbleu_1g..seg.scr" % output, "w") as f:
    f.write(nist_seg)
with open("%sbleu_1g..doc.scr" % output, "w") as f:
    f.write(nist_doc)
with open("%sbleu_1g..sys.scr" % output, "w") as f:
    f.write(nist_sys)
