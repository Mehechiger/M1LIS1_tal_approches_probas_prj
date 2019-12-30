import json
import os
from collections import defaultdict, Counter
import numpy as np

path_data = "/Users/mehec/nlp/approbas/prj/data/da_newstest2016.json"
path_trans = "/Users/mehec/nlp/approbas/prj/data_trans/"

with open(path_data, "r") as f:
    data = json.load(f)

list_src = set(x['src_lang'] for x in data)
list_tgt = set(x['tgt_lang'] for x in data)
list_orig = set(x['orig_lang'] for x in data)

data_regen = defaultdict(lambda: defaultdict(list))


for datum in data:
    data_regen['forward' if datum['src_lang'] == datum['orig_lang'] else 'reverse']["%s_%s" % (
        datum['src_lang'], datum['tgt_lang'])].append(datum)
"""
"""
print([k["src"] for k in data_regen["forward"]["ru_en"] if k["seg_id"] == "2"])
exit()
"""
"""


fw_das = {lang_pair: np.mean([item['score'] for item in langpair_list])
          for lang_pair, langpair_list in data_regen['forward'].items()}
rv_das = {lang_pair: np.mean([item['score'] for item in langpair_list])
          for lang_pair, langpair_list in data_regen['reverse'].items()}
fw_da = np.mean([v for v in fw_das.values()])
rv_da = np.mean([v for v in rv_das.values()])
print(fw_das, rv_das, fw_da, rv_da)
exit()

if not os.path.isdir(path_trans):
    os.makedirs(path_trans)

for direction, direction_dict in data_regen.items():
    for lang_pair, langpair_list in direction_dict.items():
        for type_ in ['hyp', 'ref']:
            content = "\n".join("%s ([%s][%s][%d])" % (
                item[type_], direction, lang_pair, index) for index, item in enumerate(langpair_list))
            with open("%s%s_%s_%s.trans" % (path_trans, direction, lang_pair, type_), 'w') as f:
                f.write(content)

for type_ in ['hyp', 'ref']:
    with open("%swhole_%s.trans" % (path_trans, type_), "w") as f:
        content = "\n".join("%s ([%s][%s][%d])" % (item[type_], direction, lang_pair, index) for direction, direction_dict in data_regen.items(
        ) for lang_pair, langpair_list in direction_dict.items() for index, item in enumerate(langpair_list))
        f.write(content)
