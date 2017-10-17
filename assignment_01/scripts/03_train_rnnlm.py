#!/usr/bin/python

import numpy as np
import dynet as dy
from dynet_modules import language_model
from utils import Vocab
from collections import Counter, defaultdict
from itertools import count
import random

diagnosis_file = '../data/sequences.txt'
num_hidden = 128
num_input = 128
num_layers = 1
num_epochs = 50

def read(fname):
    """
    Read a file where each line is of the form "word1 word2 ..."
    Yields lists of the form [word1, word2, ...]
    """
    with file(fname) as fh:
        for line in fh:
            sent = line.strip().split()
            sent.append("<s>")
            yield sent


# Read the file and extract all sequences
all_sequences=list(read(diagnosis_file))

# Train Valid split
train = []
valid = []
for a, k in enumerate(all_sequences):
   if a%10 == 1:
      valid.append(k)
   else:
      train.append(k) 


# Word Count and representation
words=[]
wc=Counter()
for sent in all_sequences:
    for w in sent:
        words.append(w)
        wc[w]+=1


vw = Vocab.from_corpus([words])
S = vw.w2i["<s>"]
nwords = vw.size()


model = dy.Model()
trainer = dy.AdamTrainer(model)
rnnlm = language_model(num_layers, num_input, num_hidden, model, nwords, vw)


# Have fun

num_tagged = cum_loss = 0
for ITER in xrange(50):
    random.shuffle(train)
    for i,s in enumerate(train,1):
        if i % 500 == 0:
            trainer.status()
            print cum_loss / num_tagged , " processed ", i , " of ", len(train)
            cum_loss = 0
            num_tagged = 0
        if i % 10000 == 0 or i == len(train)-1:
            dev_loss = dev_words = 0
            for sent in test:
                loss_exp = rnnlm.calculate_LM_loss(sent)
                dev_loss += loss_exp.scalar_value()
                dev_words += len(sent)
            print dev_loss / dev_words
            # Save the model
            rnnlm.save('models')
            print "Saved model"
        # train on sent
        loss_exp = rnnlm.calculate_LM_loss(s)
        cum_loss += loss_exp.scalar_value()
        num_tagged += len(s)
        loss_exp.backward()
        trainer.update()
    print "epoch %r finished" % ITER
    trainer.update_epoch(1.0)

    # Save the model
    rnnlm.save('models')
    print "Saved model"
 



