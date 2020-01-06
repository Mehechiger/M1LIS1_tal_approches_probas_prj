import json

with open("../data/data_parsed.json", "r") as f:
    d = json.load(f)


for lp in d["forward"]:
    for i in range(len(d["forward"][lp]["src"])):
        sent = d["forward"][lp]["src"][i]
        try:
            if sent in d["reverse"]["%s_%s" % (lp.split("_")[1], lp.split("_")[0])]["ref"]:
                pass
            else:
                d["reverse"]["%s_%s" %
                             (lp.split("_")[1], lp.split("_")[0])]["ref"].append(sent)
        except KeyError:
            d["reverse"]["%s_%s" % (lp.split("_")[1], lp.split("_")[0])] = {
                "ref": []}
            d["reverse"]["%s_%s" %
                         (lp.split("_")[1], lp.split("_")[0])]["ref"].append(sent)

for lp in d["reverse"]:
    for i in range(len(d["reverse"][lp]["ref"])):
        sent = d["reverse"][lp]["ref"][i]
        try:
            if sent in d["forward"]["%s_%s" % (lp.split("_")[1], lp.split("_")[0])]["src"]:
                pass
            else:
                d["forward"]["%s_%s" %
                             (lp.split("_")[1], lp.split("_")[0])]["src"].append(sent)
        except KeyError:
            d["forward"]["%s_%s" % (lp.split("_")[1], lp.split("_")[0])] = {
                "src": []}
            d["forward"]["%s_%s" %
                         (lp.split("_")[1], lp.split("_")[0])]["src"].append(sent)

"""
with open("../data/data_parsed.json", "w") as f:
    json.dump(d, f)
"""
