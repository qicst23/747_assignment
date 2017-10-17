import os
import numpy
from collections import Counter, defaultdict
from itertools import count
import random


class Vocab:

    def __init__(self, w2i=None):
        if w2i is None: w2i = defaultdict(count(0).next)
        self.w2i = dict(w2i)
        self.i2w = {i:w for w,i in w2i.iteritems()}

    @classmethod
    def from_corpus(cls, corpus):
        w2i = defaultdict(count(0).next)
        for sent in corpus:
            [w2i[word] for word in sent]
        return Vocab(w2i)

    def size(self): return len(self.w2i.keys())

    def read(self, fname):
       """
       Read a file where each line is of the form "word1 word2 ..."
       Yields lists of the form [word1, word2, ...]
       """
       with file(fname) as fh:
         for line in fh:
            sent = line.strip().split()
            sent.append("<s>")
            yield sent




    
