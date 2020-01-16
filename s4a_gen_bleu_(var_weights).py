import json
import re
import sys
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk import word_tokenize as tok

path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sdata/data_regen.json" % path
output = "%sscores/" % path

bleu_weights = (1, 0, 0, 0)
bleu_autoreweigh = True

with open(input_, "r") as f:
    data_regen = json.load(f)


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
