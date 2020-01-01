import pandas as pd


def load_scr(scr):
    with open(scr, "r") as f:
        lines = (line.split() for line in f.readlines())
        return pd.DataFrame(([line[0], line[1], int(line[2]), float(line[3])] for line in lines),
                            columns=["direction", "lang_pair", "seg_id", "score"])
