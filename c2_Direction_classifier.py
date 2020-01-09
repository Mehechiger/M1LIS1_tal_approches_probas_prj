from collections import Counter, defaultdict
from math import log, sqrt
import numpy as np
import re


class Direction_classifier:
    def __init__(self, train=None, dev=None, features=None):
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
        self.set_features(features)
        self.w = defaultdict(int)
        self.x_norm_mean = defaultdict(lambda: 0)
        self.x_norm_std = defaultdict(lambda: 1)
        self.m = 0
        self.n_updates = 0

    def del_learned(self):
        self.w = defaultdict(int)
        self.x_norm_mean = defaultdict(lambda: 0)
        self.x_norm_std = defaultdict(lambda: 1)
        self.m = 0
        self.n_updates = 0

    def set_datasets(self, train, dev):
        self.train, self.dev = train, dev

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

    def get_w(self):
        return self.w.copy()

    def get_n_updates(self):
        return self.n_updates

    def ttr(self, chunk, type_):
        poss = Counter(token["pos"] for sent in chunk for token in sent)
        v = len(poss)
        v_1 = len({pos for pos in poss if poss[pos] == 1})
        n = sum(n_pos for n_pos in poss.values())
        try:
            return defaultdict(int, {"&*%s_ttr*&" % type_: 100*log(n)/(1-v_1/v)})
        except ZeroDivisionError:
            return defaultdict(int)

    def mean_word_rank(self, chunk, type_):
        """
        """
        return defaultdict(int, {})

    def cohesive_markers(self, chunk, type_):
        """
        """
        return defaultdict(int, {})

    def pos_n_grams(self, chunk, type_):
        return defaultdict(int,
                           Counter("%s_%s" % (type_,
                                              "_".join(sent[i+j]["pos"]
                                                       for j in range(n)
                                                       )
                                              )
                                   for sent in chunk
                                   for n in self.pos_ns
                                   for i in range(len(sent)-n+1)
                                   )
                           )

    def chr_n_grams(self, chunk, type_):
        return defaultdict(int,
                           Counter("&*%s_chr_n_grams*&%s" % (type_, token["text"][i:i+n])
                                   for sent in chunk
                                   for token in sent
                                   for n in self.chr_ns
                                   for i in range(len(token["text"])-n+1)
                                   )
                           )

    def positional_token_frequency(self, chunk, type_):
        def get_slice_(l, start, end, key):
            try:
                if start == end:
                    return l[start][key]
                else:
                    return l[start:end][0][key]
            except IndexError:
                return None

        positional_tokens = zip(*((get_slice_(sent, 0, 0, "lemma"),
                                   get_slice_(sent, 1, 2, "lemma"),
                                   get_slice_(sent, -1, -1, "lemma"),
                                   get_slice_(sent, -2, -1, "lemma"),
                                   get_slice_(sent, -3, -2, "lemma"),
                                   )
                                  for sent in chunk
                                  ))
        positional_token_counts = (defaultdict(int, Counter(pos_tokens))
                                   for pos_tokens in positional_tokens
                                   )
        token_counts = defaultdict(int,
                                   Counter(token["lemma"]
                                           for sent in chunk
                                           for token in sent
                                           )
                                   )
        return defaultdict(int,
                           {"&*%s_pos_%s_token_freq*&%s" % (type_, ind, token): pos_token_count/token_counts[token]
                            for ind, pos_token_counts in enumerate(positional_token_counts)
                            for token, pos_token_count in pos_token_counts.items()
                            if token in token_counts and token
                            }
                           )

    def function_words(self, chunk, type_):
        """
        """
        return defaultdict(int, {})

    def puncs(self, chunk, type_):
        return defaultdict(int,
                           {"&*%s_puncs*&%s" % (type_, punc): punc_count/sum(len(sent) for sent in chunk)
                            for punc, punc_count in Counter(token["text"]
                                                            for sent in chunk
                                                            for token in sent
                                                            if token["pos"] == "PUNCT"
                                                            ).items()
                            }
                           )

    def pronouns(self, chunk, type_):
        return defaultdict(int,
                           {"&*%s_prons*&" % type_: len([1
                                                         for sent in chunk
                                                         for token in sent
                                                         if token["pos"] == "PRON"
                                                         ])/sum(len(sent) for sent in chunk)
                            }
                           )

    def mean_dep_tree_depth(self, chunk, type_):
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
        return defaultdict(int, {"&*%s_mean_dep_tree_depth*&" % (type_): depths/len(chunk)})

    def get_mean_xs(self, xs):
        return defaultdict(int,
                           {feature: sum(x[feature]
                                         for x in xs
                                         if feature in x
                                         )/len(xs)
                            for feature in set(feature
                                               for x in xs
                                               for feature in x
                                               )
                            }
                           )

    def get_std_xs(self, xs, mean_xs):
        n = len(xs) if len(xs) > 1 else 2
        return defaultdict(int,
                           {feature: sqrt(sum((x[feature]-mean_xs[feature])**2
                                              for x in xs
                                              if feature in x
                                              )/(n-1)
                                          )
                            for feature in set(feature
                                               for x in xs
                                               for feature in x
                                               )
                            }
                           )

    def update_x_norm_params(self, xs):
        n = len(xs)
        mean_xs = self.get_mean_xs(xs)
        std_xs = self.get_std_xs(xs, mean_xs)
        features = set(feature
                       for x in xs
                       for feature in x
                       ).union(self.x_norm_mean)

        x_norm_mean = defaultdict(int,
                                  {feature: (self.m*self.x_norm_mean[feature]+n*mean_xs[feature]
                                             )/(self.m+n)
                                   for feature in features
                                   }
                                  )
        self.x_norm_std = defaultdict(lambda: 1,
                                      {feature: sqrt((self.m*(self.x_norm_std[feature]**2+(x_norm_mean[feature]-self.x_norm_mean[feature])**2
                                                              )+n*(std_xs[feature]**2+(x_norm_mean[feature]-mean_xs[feature])**2)
                                                      )/(self.m+n-1)
                                                     )
                                       for feature in features
                                       }
                                      )
        self.x_norm_mean = x_norm_mean
        for k, v in self.x_norm_std.items():
            if v == 0:
                self.x_norm_std[k] = 1

        self.m += n

    def norm_xs(self, xs):
        self.update_x_norm_params(xs)
        return [defaultdict(int,
                            {feature: (feature_val-self.x_norm_mean[feature])/self.x_norm_std[feature]
                             for feature, feature_val in x.items()
                             }
                            )
                for x in xs
                ]

    def get_xs(self, chunks_pair):
        xs = []
        for i in range(len(chunks_pair["src"])):
            xs.append(defaultdict(int))
            for feature in self.features:
                for type_ in ["src", "ref"]:
                    xs[i].update(eval("self.%s" % feature)(chunks_pair[type_][i],
                                                           type_
                                                           ))
        return xs

    def update(self, vec, y):
        self.n_updates += 1
        for k, v in vec.items():
            self.w[k] += v*y

    def iterate(self, xs, ys):
        len_ = len(xs)
        for i in range(len_):
            if self.classify(xs[i]) != ys[i]:
                self.update(xs[i], ys[i])

    def learn(self):
        if not self.train or not self.dev:
            print("cannot learn without datasets!")
            exit()

        chunks_src, chunks_ref, chunks_pred = list(zip(*self.train))
        xs, ys = (self.norm_xs(self.get_xs({"src": chunks_src,
                                            "ref": chunks_ref
                                            })),
                  chunks_pred
                  )

        last_ones = []
        while True:
            print("training..., pass %s" % (len(last_ones)+1),
                  end="\r"
                  )
            self.iterate(xs, ys)
            print("training..., pass %s - done" % (len(last_ones)+1))
            print("evaluating on dev..., pass %s - " % len(last_ones),
                  end="\r"
                  )
            last_ones.append((self.evaluate(), self.w.copy()))
            print("evaluating on dev..., pass %s - done. accuracy %s%%" %
                  (len(last_ones), last_ones[-1][0]*100))
            if len(last_ones) >= 6 and min(ones[0] for ones in last_ones[-6:-4]
                                           ) >= max(ones[0] for ones in last_ones[-3:-1]):
                self.w = last_ones[np.argmax([ones[0]
                                              for ones in last_ones
                                              ])][1].copy()
                break

    def classify(self, x):
        return 1 if sum(self.w[k]*v for k, v in x.items() if k in self.w) >= 0 else -1

    def evaluate(self, chunks_triplets=None):
        if not chunks_triplets:
            chunks_triplets = self.dev
        len_ = len(chunks_triplets)
        chunks_src, chunks_ref, chunks_pred = list(zip(*chunks_triplets))
        xs, ys = (self.norm_xs(self.get_xs({"src": chunks_src,
                                            "ref": chunks_ref
                                            })),
                  chunks_pred
                  )
        return sum(self.classify(xs[i]) == ys[i] for i in range(len_))/len_
