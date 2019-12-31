import json
import os
import shutil
from subprocess import Popen, PIPE

input_ = "/Users/mehec/nlp/approbas/prj/data/data_regen.json"
temp = "/Users/mehec/nlp/approbas/prj/scores/temp/"
output = "/Users/mehec/nlp/approbas/prj/scores/"
terp = "/Users/mehec/nlp/approbas/prj/terp-master/bin/"
terp_ph_db = "/Users/mehec/nlp/approbas/prj/terp-master/data/phrases.db"
output_fm = "param nist"
modes_terp = ["p", "pa", "p_ter"]

if not os.path.isdir(temp):
    os.makedirs(temp)
if not os.path.isdir(output):
    os.makedirs(output)

with open(input_, "r") as f:
    data_regen = json.load(f)

for type_ in ['hyp', 'ref']:
    with open("%s%ss.trans" % (temp, type_), "w") as f:
        content = "\n".join("%s ([%s][%s][%d])" % (item[type_], direction, lang_pair, index) for direction, direction_dict in data_regen.items(
        ) for lang_pair, langpair_list in direction_dict.items() for index, item in enumerate(langpair_list))
        f.write(content)

param = "Reference File (filename)                : %srefs.trans\nHypothesis File (filename)               : %shyps.trans\nPhrase Database (filename)               : %s\nOutput Formats (list)                    : %s\nOutput Prefix (filename)                 : %ster" % (
    temp, temp, terp_ph_db, output_fm, output)

for mode_terp in modes_terp:
    with open("%ster%s.param" % (temp, mode_terp), "w") as f:
        f.write("%s%s." % (param, mode_terp))
    print(Popen("%ster%s %ster%s.param" % (terp, mode_terp, temp,
                                           mode_terp), stdout=PIPE, shell=True).stdout.read())

shutil.rmtree(temp)
