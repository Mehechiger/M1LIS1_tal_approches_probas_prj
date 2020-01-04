import sys
import json
from collections import defaultdict

path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sdata/da_newstest2016.json" % path
output = "%sdata/" % path

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
