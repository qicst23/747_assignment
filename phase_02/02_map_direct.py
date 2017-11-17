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


#hidden = sys.argv[1]
#exp_name = sys.argv[2]
test_ratio = 0.1
validation_ratio = 0.1

debug = 1
test = 0
batching = 0

# Load the train, test and validation sets
with open('train_set.pkl', 'rb') as f:
     train_set = pickle.load(f)
with open('valid_set.pkl', 'rb') as f:
     valid_set = pickle.load(f)
with open('test_set.pkl', 'rb') as f:
     test_set = pickle.load(f)



# Model and hyperparameters

for epoch in range(30):
  start_time = time.time()
  print " Epoch ", epoch
  train_loss = 0
  count = 0
  for index in random.sample(range(len(train_set)), len(train_set)):
       src = train_set[0][index]
       tgt = train_set[1][index]
       if debug:
          print "Source: ", src
          print "Target: ", tgt
