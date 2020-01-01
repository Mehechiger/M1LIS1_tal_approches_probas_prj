import json
from collections import defaultdict

input_ = "../data/da_newstest2016.json"
output = "../data/"

with open(input_, "r")as f:
    data = json.load(f)

data_regen = defaultdict(lambda: defaultdict(list))

for datum in data:
    data_regen['forward'
               if datum['src_lang'] == datum['orig_lang']
               else 'reverse'
               ]["%s_%s" % (datum['src_lang'], datum['tgt_lang'])
                 ].append(datum)

with open("%sdata_regen.json" % output, "w") as f:
    json.dump(data_regen, f)
