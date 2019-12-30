import json

"""
this script will read the data and generate TRANS format files according to their orig_lang, src_lang, tgt_lang and whether they are hyp or ref
the TRANS format is used with some differences to facilitate our work:
([SET_ID][SRC_TGT_ORIG][SEG_ID])
with the seg id regenerated
"""

# modify these before executing
path_data = "/Users/mehec/nlp/approbas/prj/data/da_newstest2016.json"
path_output = "/Users/mehec/nlp/approbas/prj/data/"


with open(path_data, "r") as f:
    d = json.load(f)

da = set(x['orig_lang'] for x in d)
db = set(x['src_lang'] for x in d)
dc = set(x['tgt_lang'] for x in d)

for a in da:
    for b in db:
        for c in dc:
            for dd in ['hyp', 'ref']:
                content = "\n".join("%s ([newstest2016][%s_%s_%s][%d])" % (it, b, c, a, ind) for ind, it in enumerate(
                    x[dd] for x in d if x['orig_lang'] == a and x['src_lang'] == b and x['tgt_lang'] == c))
                if content:
                    with open("%s%s_%s_%s_%s.trans" % (path_output, b, c, a, dd), "w") as f:
                        f.write(content)
