import os
import numpy as np
import sys
sys.path.append('/home3/srallaba/hacks/repos/clustergen_steroids')
from building_blocks.DNNs import *
import dynet as dy
from sklearn.model_selection import train_test_split
import random
from sklearn.metrics import log_loss
from sklearn.metrics import roc_auc_score

exp_dir = sys.argv[2]

input = np.loadtxt('input_sequences')
print "Loaded input"
output = np.loadtxt('output_sequences')
print "Loaded output"

X_train, X_test, y_train, y_test = train_test_split(input, output, test_size=0.1)
print "Split the data into train and test"

num_input = len(input[0])
num_output = num_input
num_hidden = int(sys.argv[1])
m = dy.Model()

arch = str(num_hidden) + '_' + str(num_hidden)
log_file = exp_dir + '/logs/log_' + arch + '.txt' 
g = open(log_file,'w')
g.close()

results_file = exp_dir + '/results/result_' + arch + '.txt'
g = open(results_file,'w')
g.close()


dnn_1 = FeedForwardNeuralNet(m, [num_input, [num_hidden, num_hidden], num_output, [dy.rectify, dy.rectify, dy.logistic]])
trainer = dy.AdamTrainer(m)

train = zip(X_train, y_train)
test = zip(X_test, y_test)

for epoch in range(40):
   print "Epoch: ", epoch
   random.shuffle(train)
   train_loss = 0
   count = 0
   for (inp,out) in train:
     count += 1
     dy.renew_cg()
     loss = dnn_1.calculate_loss_classification(dy.inputTensor(inp), dy.inputTensor(out))
     train_loss += loss.value()
     loss.backward()
     if count % 32 == 1:
        trainer.update()
   print " Train loss after epoch ", epoch, " : ", str(float(train_loss/count)) 
   g = open(log_file,'a')
   g.write(" Train loss after epoch " + str(epoch) + " : " + str(float(train_loss/count)) + '\n')
   g.close()

   test_loss = 0
   count_test = 0
   for (i_t, o_t) in test:
     count_test += 1
     dy.renew_cg()
     labels = dnn_1.predict(dy.inputTensor(i_t))
     y_pred = labels.value()
     print y_pred
     print o_t
     test_loss += log_loss(o_t, y_pred)

   print " Test loss: ", test_loss/float(count_test)
   g = open(results_file,'a')
   g.write(" Test loss after epoch " + str(epoch) + " : " + str(float(test_loss/count_test)) + '\n')
   g.close()
   print '\n'






