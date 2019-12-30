from collections import defaultdict


def load_scr(scr):
    score = defaultdict(lambda: defaultdict(list))
    with open(scr, "r") as f:
        for line in f.readlines():
            l = line.split()
            score[l[0]][l[1]].append(float(l[3]))
    return score
