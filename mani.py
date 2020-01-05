import json

with open("../data/data_parsed.json", "r") as f:
    d = json.load(f)

for dd in d:
    for l in d[dd]:
        for t in d[dd][l]:
            for i in range(len(d[dd][l][t])):
                for j in range(len(d[dd][l][t][i])):
                    if d[dd][l][t][i][j]["head"] == 0:
                        d[dd][l][t][i][j]["head"] = -1

with open("../data/data_parsed.json", "w") as f:
    json.dump(d, f)
