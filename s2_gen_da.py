import json
import os
import sys

path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sdata/data_regen.json" % path
output = "%sscores/" % path

if not os.path.isdir(output):
    os.makedirs(output)

with open(input_, "r") as f:
    data_regen = json.load(f)

nist_seg = "\n".join("\t".join([direction, "", lang_pair, str(ind), str(it["score"])])
                     for direction, direction_dict in data_regen.items()
                     for lang_pair, langpair_list in direction_dict.items()
                     for ind, it in enumerate(langpair_list)
                     )

with open("%sda..seg.scr" % output, "w") as f:
    f.write(nist_seg)
