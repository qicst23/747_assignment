import sys, os
sys.path.append('/home3/srallaba/hacks/repos/clustergen_steroids')
from building_blocks.EncoderDecoderModels import *
import dynet as dy
import numpy as np
from math import sqrt
from sklearn import preprocessing
import random
from sklearn.metrics import mean_squared_error,accuracy_score,confusion_matrix
import time
import pickle
from sklearn.model_selection import train_test_split
from collections import defaultdict


hidden = sys.argv[1]
exp_name = sys.argv[2]
test_ratio = 0.1
validation_ratio = 0.1

debug = 1
test = 0
batching = 1

# Load the train, test and validation sets
with open('train_set.pkl', 'rb') as f:
     train_set = pickle.load(f)
with open('valid_set.pkl', 'rb') as f:
     valid_set = pickle.load(f)
with open('test_set.pkl', 'rb') as f:
     test_set = pickle.load(f)


# Architecture
arch = 'seq2seq_' + hidden

# Log file
logfile_name = exp_name + '/logs/log_' + arch + '.log'
g = open(logfile_name, 'w')
g.close()

# Saving Directory
save_dir = exp_name + '/outputs/' + arch
if not os.path.exists(save_dir):
   os.makedirs(save_dir)

# Results file
results_file = save_dir + '/results.txt'
g = open(results_file , 'w')
g.close()

# Files
sequences_file = '../../phase_reproduction/preprocessed/preprocessed.seqs'
labels_file = '../../phase_reproduction/preprocessed/preprocessed.3digitICD9.seqs'
tree_file = '../../phase_reproduction/trees/mimic.trees.level2.pk'

# Model and hyperparameters
units_input = 4894
units_hidden = int(hidden)
units_output = 26679
num_layers = 1
units_attention = 16
num_class = 26679
m = dy.Model()
M = m.add_lookup_parameters((1, units_output))
edm = EncoderDecoderModel(m, [num_layers, units_input, units_hidden, units_attention, units_output, dy.tanh,M ])
trainer = dy.AdamTrainer(m)
update_params = 32
batch_size = 32
num_batches = int(np.ceil(float(len(train_set[0])) / float(batch_size)))

####### Helper Functions ############

def padMatrix(seqs, labels, num_input, num_class):
    #print "Input dimensions: ", num_input
    lengths = np.array([len(seq) for seq in seqs]) - 1
    n_samples = len(seqs)
    maxlen = np.max(lengths)

    x = np.zeros((maxlen, n_samples, num_input))
    y = np.zeros((maxlen, n_samples, 26679))
    mask = np.zeros((maxlen, n_samples))

    for idx, (seq, lseq) in enumerate(zip(seqs,labels)):
        for xvec, subseq in zip(x[:,idx,:], seq[:-1]): xvec[subseq] = 1.
        for yvec, subseq in zip(y[:,idx,:], lseq[1:]): yvec[subseq] = 1.
        mask[:lengths[idx], idx] = 1.

    lengths = np.array(lengths)

    return x, y, mask, lengths

def calculate_dimSize(seqFile):
    seqs = pickle.load(open(seqFile, 'rb'))
    codeSet = set()
    for patient in seqs:
        for visit in patient:
            for code in visit:
                codeSet.add(code)
    return max(codeSet) + 1

####################################

input_dim = calculate_dimSize(sequences_file)
num_class = calculate_dimSize(labels_file)
print "Number of batches: ", num_batches
Start = time.time()
for epoch in range(30):
  start_time = time.time()
  print " Epoch ", epoch
  train_loss = 0
  count = 0
  for index in random.sample(range(num_batches), num_batches):
        count += 1
        batch_x = train_set[0][index*batch_size:(index+1)*batch_size]
        batch_y = train_set[1][index*batch_size:(index+1)*batch_size]
        x, y, mask, lengths = padMatrix(batch_x, batch_y, input_dim , num_class)
        A = np.swapaxes(x,1,2)
        B = np.swapaxes(y,1,2)
        for a,b in zip(A,B):
          dy.renew_cg()
          a = np.asarray(np.transpose(a))
          b = np.asarray(np.transpose(b))
          loss = edm.calculate_loss(a,b)
          train_loss += loss.value()
          loss.backward()
        trainer.update()
        if count % 10 == 1:
           print "Train loss after ", count , " number of batches is :", train_loss/(count*batch_size)       
  print " Train loss after epoch ", epoch, " is ", train_loss/(count*batch_size)

  # Get Validation Loss
  valid_loss = 0
  count_valid = 0
  for idx in range(len(valid_set)):
        batch_x = valid_set[0][idx]
        batch_y = valid_set[1][idx]
        x, y, mask, lengths = padMatrix(batch_x, batch_y, input_dim , num_class)
        A = np.swapaxes(x,1,2)
        B = np.swapaxes(y,1,2)
        for a,b in zip(A,B):
          dy.renew_cg()
          count_valid += 1
          a = np.asarray(np.transpose(a))
          b = np.asarray(np.transpose(b))
          loss = edm.calculate_loss(a,b)
          valid_loss += loss.value()
  print " Valid loss after epoch ", epoch, " is ", valid_loss/(count_valid)

  # Get Test loss
  test_loss = 0
  count_test = 0
  for idx in range(len(test_set)):
        batch_x = test_set[0][idx]
        batch_y = test_set[1][idx]
        x, y, mask, lengths = padMatrix(batch_x, batch_y, input_dim , num_class)
        A = np.swapaxes(x,1,2)
        B = np.swapaxes(y,1,2)
        for a,b in zip(A,B):
          dy.renew_cg()
          count_test += 1
          a = np.asarray(np.transpose(a))
          b = np.asarray(np.transpose(b))
          loss = edm.calculate_loss(a,b)
          test_loss += loss.value()
  print " Test loss after epoch ", epoch, " is ", test_loss/count_test

  end_time = time.time()
  duration = end_time - start_time
  start_time = end_time
  print " I think I will run for ", duration * (30 - epoch) / 60 , "minutes"
  print '\n'
  f = open(logfile_name, 'a')
  f.write( "Train Loss after epoch: " + str(epoch).zfill(3) + " : " + str(train_loss/(count*batch_size)) + '\n')
  f.write( "Valid Loss after epoch: " + str(epoch).zfill(3) + " : " + str(valid_loss/count_valid) + '\n')
  f.write( " Test Loss after epoch: " + str(epoch).zfill(3) + " : " + str(test_loss/count_test) + '\n')
  f.close()
