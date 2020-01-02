import json
import re
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk import word_tokenize as tok

input_ = "../data/data_regen.json"
output = "../scores/"

bleu_weights = (0, 0, 0, 4)
bleu_autoreweigh = True

with open(input_, "r") as f:
    data_regen = json.load(f)

"""
# punc = re.compile('[,…` .[•»/:#‘’!(;"?”)+«“\]]')
punc_data = ['"', '%', ':', '-', '6',
             '8', '“', '(', '€', '…',
             ' ', '»', '\xad', '@', '?',
             '+', '.', "'", '´', '‘',
             '[', '«', '`', '²', '–',
             '/', '9', '=', '2', ',',
             '7', '№', '°', ')', '\]',
             '_', '4', '!', '£', '~',
             '0', '$', '•', '1', '&',
             ';', '’', '5', '#', '”'
             ]
punc = re.compile('[%s]' % "".join(punc_data))
print(punc)
exit()
"""

nist_seg = "\n".join("\t".join([direction,
                                "",
                                lang_pair,
                                str(ind),
                                str(sentence_bleu([tok(it["ref"]), ],
                                                  tok(it["hyp"]),
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
                                str(corpus_bleu([[tok(it["ref"]), ]
                                                 for it in langpair_list
                                                 ],
                                                [tok(it["hyp"])
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
                                str(corpus_bleu([[tok(it["ref"]), ]
                                                 for langpair_list in direction_dict.values()
                                                 for it in langpair_list
                                                 ],
                                                [tok(it["hyp"])
                                                 for langpair_list in direction_dict.values()
                                                 for it in langpair_list
                                                 ],
                                                weights=bleu_weights,
                                                auto_reweigh=bleu_autoreweigh
                                                ))
                                ])
                     for direction, direction_dict in data_regen.items()
                     )

with open("%sbleu_%s..seg.scr" % (output, "".join(str(it) for it in bleu_weights)), "w") as f:
    f.write(nist_seg)
with open("%sbleu_%s..doc.scr" % (output, "".join(str(it) for it in bleu_weights)), "w") as f:
    f.write(nist_doc)
with open("%sbleu_%s..sys.scr" % (output, "".join(str(it) for it in bleu_weights)), "w") as f:
    f.write(nist_sys)
