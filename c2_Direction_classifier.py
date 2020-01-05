from collections import Counter, defaultdict
from math import log
import re


class Direction_classifier:
    def __init__(self, train, dev):
        self.train, self.dev = train, dev
        self.ngram_features = ["pos", "chr"]
        self._features = {"ttr",
                          "mean_word_rank",
                          "cohesive_markers",
                          "pos_2_grams",
                          "pos_3_grams",
                          "chr_2_grams",
                          "chr_3_grams",
                          "positional_token_frequency",
                          "function_words",
                          "puncs",
                          "pronouns",
                          "mean_dep_tree_depth"
                          }
        self.set_features()
        self.vec = defaultdict(int)

    def set_features(self, features=None):
        if not features:
            features = self._features

        self.pos_ns = set()
        self.chr_ns = set()
        self.features = set()
        self.features_ = set()

        non_existent_features = set()

        for feature in features:
            if any(feature[:len(ngf)] == ngf for ngf in self.ngram_features) and feature[-6:] == "_grams":
                self.features.add(re.compile(
                    "(?<=_)\d(?=_)").sub("n", feature))
                self.features_.add(feature)
                eval("self.%s_ns" % feature.split("_")[0]).add(
                    int(feature.split("_")[1]))
            elif feature in self._features:
                self.features.add(feature)
                self.features_.add(feature)
            else:
                non_existent_features.append(feature)
        if non_existent_features:
            print("some features do not exist: %s" %
                  " ".join(non_existent_features)
                  )
        print("now using features: %s" %
              " ".join(self.features_)
              )

        if not self.features:
            print("must use some features!")
            exit()

    def ttr(self, chunk):
        poss = Counter(token["pos"] for sent in chunk for token in sent)
        v = len(poss)
        v_1 = len({pos for pos in poss if poss[pos] == 1})
        n = sum(n_pos for n_pos in poss.values())
        return {"&*ttr*&": 100*log(n)/(1-v_1/v)}

    def mean_word_rank(self, chunk):
        """
        """
        return {}

    def cohesive_markers(self, chunk):
        """
        """
        return {}

    def pos_n_grams(self, chunk):
        return Counter("_".join(sent[i+j]["pos"] for j in range(i))
                       for sent in chunk
                       for n in self.pos_ns
                       for i in range(len(sent)-n+1)
                       )

    def chr_n_grams(self, chunk):
        return Counter("&*chr_n_grams*&%s" % token["text"][i:i+n]
                       for sent in chunk
                       for token in sent
                       for n in self.chr_ns
                       for i in range(len(token)-n+1)
                       )

    def positional_token_frequency(self, chunk):
        positional_tokens = zip(*((sent[0]["text"],
                                   sent[1:2]["text"],
                                   sent[-1]["text"],
                                   sent[-2:-1]["text"],
                                   sent[-3:-2]["text"]
                                   )
                                  for sent in chunk
                                  ))
        positional_token_counts = (Counter(pos_tokens)
                                   for pos_tokens in positional_tokens
                                   )
        token_counts = Counter(token["text"]
                               for sent in chunk
                               for token in sent
                               )
        return {"&*pos_%s_token_freq*&%s" % (ind, token): pos_token_count/token_counts[token]
                for ind, pos_token_counts in enumerate(positional_token_counts)
                for token, pos_token_count in pos_token_counts.items()
                if token in token_counts
                }

    def function_words(self, chunk):
        """
        """
        return {}

    def puncs(self, chunk):
        return {"&*puncs*&%s" % punc: punc_count/sum(len(sent) for sent in chunk)
                for punc, punc_count in Counter(token["text"]
                                                for sent in chunk
                                                for token in sent
                                                if token["pos"] == "PUNCT"
                                                ).items()
                }

    def pronouns(self, chunk):
        return {"&*prons*&": len([1
                                  for sent in chunk
                                  for token in sent
                                  if token["pos"] == "PRON"
                                  ])/sum(len(sent) for sent in chunk)}

    def mean_dep_tree_depth(self, chunk):
        def bottom_up(sent, head):
            head = sent[head]
            if head == -1:
                return 1
            else:
                return bottom_up(sent, head)+1

        depths = 0
        n = 0
        for sent in chunk:
            sent = [token["head"] for token in sent]
            depths += max(bottom_up(sent, head) for head in sent)
        return {"&*mean_dep_tree_depth*&": depths/len(chunk)}

    def update(self):
        pass

    def train(self):
        pass

    def classify(self, chunk):
        for feature in self.features:
            print(eval("self.%s" % feature)(chunk))
