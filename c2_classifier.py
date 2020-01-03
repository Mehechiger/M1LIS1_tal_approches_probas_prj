from collections import Counter
from math import log


def load_direction_level(file_):
    pass


def load_langpair_level(file_):
    pass


def chunk_data(data, n):
    pass


def ttr(chunk):
    poss = Counter(token["pos"] for sent in chunk for token in sent)
    v = len(poss)
    v_1 = len({pos for pos in poss if poss[pos] == 1})
    n = sum(n_pos for n_pos in poss.values())
    return 100*log(n)/(1-v_1/v)


def mean_word_rank():
    pass


def cohesive_markers():
    pass


def pos_n_grams(chunk, n):
    return Counter("_".join(sent[i+j]["pos"] for j in range(i))
                   for sent in chunk
                   for i in range(len(sent)-n+1))


def chr_n_grams(chunk, n):
    return Counter(word["text"][i:i+n]
                   for sent in chunk
                   for word in sent
                   for i in range(len(word)-n+1))


def positional_token_frequency(chunk):
    """
    bu dui
    """
    c = Counter((sent[0], sent[1:2], sent[-1], sent[-2:-1], sent[-3:-2],
                 sent[2:-3]
                 )
                for sent in chunk
                )


def function_words():
    pass


def punc():
    pass


def pronouns():
    pass
