import json
import re
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

input_ = "/Users/mehec/nlp/approbas/prj/data/data_regen.json"
output = "/Users/mehec/nlp/approbas/prj/scores/"

with open(input_, "r") as f:
    data_regen = json.load(f)

punc = re.compile('[,…` .[•»/:#‘’!(;"?”)+«“\]]')

nist_seg = "\n".join("\t".join([direction, "", lang_pair, str(ind), str(sentence_bleu([list(filter(None, re.split(punc, it["ref"]))), ], list(filter(None, re.split(
    punc, it["hyp"])))))]) for direction, direction_dict in data_regen.items() for lang_pair, langpair_list in direction_dict.items() for ind, it in enumerate(langpair_list))

nist_doc = "\n".join("\t".join([direction, "", lang_pair, str(corpus_bleu([[list(filter(None, re.split(punc, it["ref"]))), ] for it in langpair_list], [list(filter(
    None, re.split(punc, it["hyp"]))) for it in langpair_list]))]) for direction, direction_dict in data_regen.items() for lang_pair, langpair_list in direction_dict.items())

nist_sys = "\n".join("\t".join([direction, "", str(corpus_bleu([[list(filter(None, re.split(punc, it["ref"]))), ] for langpair_list in direction_dict.values() for it in langpair_list], [
                     list(filter(None, re.split(punc, it["hyp"]))) for langpair_list in direction_dict.values() for it in langpair_list]))]) for direction, direction_dict in data_regen.items())

with open("%sbleu..seg.scr" % output, "w") as f:
    f.write(nist_seg)
with open("%sbleu..doc.scr" % output, "w") as f:
    f.write(nist_doc)
with open("%sbleu..sys.scr" % output, "w") as f:
    f.write(nist_sys)
