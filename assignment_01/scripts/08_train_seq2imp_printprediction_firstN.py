#!/usr/bin/python

import numpy as np
import dynet as dy
from dynet_modules import sequence_to_sequence
from utils import Vocab
from collections import Counter, defaultdict
from itertools import count
import random

src_file = '../data/sequence_pairs_src.txt'
tgt_file = '../data/sequence_pairs_tgt.txt'
num_hidden = 32
num_input = 16
num_layers = 4
num_epochs = 50
early_save = 1

def read(fname):
    """
    Read a file where each line is of the form "word1 word2 ..."
    Yields lists of the form [word1, word2, ...]
    """
    with file(fname) as fh:
        for line in fh:
            sent = line.strip().split()
            # Keep only the first 3 characters
            for (a,k) in enumerate(sent):
                q = str(k).strip('"').strip("'")
                #print q
                sent[a] = q[0:3]
            sent.append("<s>")
            yield sent

# Read the file and extract all sequences
src = list(read(src_file))
tgt = list(read(tgt_file))
all_sequences = zip(src,tgt)
random.shuffle(all_sequences)

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
for sent in src:
    for w in sent:
        words.append(w)
        wc[w]+=1

for sent in tgt:
    for w in sent:
        words.append(w)
        wc[w]+=1

vw = Vocab.from_corpus([words])
S = vw.w2i["<s>"]
nwords = vw.size()


model = dy.Model()
trainer = dy.SimpleSGDTrainer(model)
seq2seq = sequence_to_sequence(num_layers, num_input, num_hidden, model, nwords, vw)


# Have fun

num_tagged = cum_loss = 0
for ITER in xrange(50):
    random.shuffle(train)
    for i,s in enumerate(train,1):
        if i % 1000 == 0:
            trainer.status()
            print cum_loss / num_tagged , " processed ", i , " of ", len(train)
            cum_loss = 0
            num_tagged = 0
        if i % 10000 == 0 or i == len(train)-1:
            dev_loss = dev_words = 0
            random.shuffle(valid)
            for sent in valid:
                loss_exp, pred = seq2seq.calculate_mostimportant_loss_return_firstN(sent[0], sent[1])
                dev_loss += loss_exp.scalar_value()
                dev_words += len(sent[0])
            print dev_loss / dev_words
            print pred, sent[1]
            # Save the model
            seq2seq.save('models_seq2imp')
            print "Saved model"
        # train on sent
        loss_exp, pred = seq2seq.calculate_mostimportant_loss_return_firstN(s[0], s[1])
        cum_loss += loss_exp.scalar_value()
        num_tagged += len(s[0])
        loss_exp.backward()
        trainer.update()
        if early_save == 1:
           seq2seq.save('models_seq2imp')
           print "Saved after first example"
           print pred, s[1]
           early_save =0 
    print "epoch %r finished" % ITER
    trainer.update_epoch(1.0)

    # Save the model
    seq2seq.save('models_seq2imp')
    print "Saved model"
 



