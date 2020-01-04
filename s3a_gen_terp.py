import json
import os
import sys
import shutil
from subprocess import Popen, PIPE

path = sys.path[0]
if path[-8:] != "/scripts":
    print('scripts must be under "scripts" folder!')
    exit()
path = path[:-7]

input_ = "%sdata/data_regen.json" % path
temp = "%sscores/temp/" % path
output = "%sscores/" % path
terp = "%sterp-master/bin/" % path
terp_ph_db = "%sterp-master/data/phrases.db" % path
modes_terp = ["p", ]
params = ["Reference File (filename) : ",
          "Hypothesis File (filename) : ",
          "Phrase Database (filename) : ",
          "Default Shift Cost (float)               : ",
          "Output Formats (list) : ",
          "Output Prefix (filename) : "
          ]
param_values = ["%srefs.trans" % temp,
                "%shyps.trans" % temp,
                terp_ph_db,
                "10.0",
                "param nist",
                "%ster" % output
                ]

if not os.path.isdir(temp):
    os.makedirs(temp)
if not os.path.isdir(output):
    os.makedirs(output)

with open(input_, "r") as f:
    data_regen = json.load(f)

for type_ in ['hyp', 'ref']:
    with open("%s%ss.trans" % (temp, type_), "w") as f:
        content = "\n".join("%s ([%s][%s][%d])" % (item[type_], direction, lang_pair, index)
                            for direction, direction_dict in data_regen.items()
                            for lang_pair, langpair_list in direction_dict.items()
                            for index, item in enumerate(langpair_list)
                            )
        f.write(content)


param = "\n".join("%s%s" % (params[i], param_values[i])
                  for i in range(len(params))
                  )

for mode_terp in modes_terp:
    with open("%ster%s.param" % (temp, mode_terp), "w") as f:
        f.write("%s%s_punishshift." % (param, mode_terp))
    print(Popen("%ster%s %ster%s.param" % (terp, mode_terp, temp, mode_terp),
                stdout=PIPE,
                shell=True
                ).stdout.read()
          )

shutil.rmtree(temp)
