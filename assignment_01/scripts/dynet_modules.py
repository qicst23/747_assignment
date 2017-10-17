#!/usr/bin/python

import dynet as dy
import numpy as np
import pickle, os

debug = 0

class SaveableModel(object):
  
   def __init__(self, model):
     self.model = model

   def save(self, path):
     if not os.path.exists(path): os.makedirs(path)
     self.model.save(path, '/model')

   @staticmethod
   def load(model, path, load_model_params=True):
      if not os.path.exists(path): raise Exception("Model "+path+" does not exist")
      with open(path + '/model', "r") as f: self.model = pickle.load(f)
      return self.model

class language_model(SaveableModel):
   
   def __init__(self, num_layers, num_input, num_hidden, model, nwords, vw):
     self.num_layers = num_layers
     self.num_input = num_input
     self.num_hidden = num_hidden
     self.model = model
     self.RNN = dy.LSTMBuilder(self.num_layers, self.num_input, self.num_hidden, self.model)
     self.nwords = nwords
     self.vw = vw
     self.add_params()

   def add_params(self):
     ### This is to add extra parameters to put the model on steroids
     
     # Softmax weights/biases on top of LSTM outputs
     self.W_sm = self.model.add_parameters((self.nwords, self.num_hidden))
     self.b_sm = self.model.add_parameters(self.nwords)
     self.lookup = self.model.add_lookup_parameters((self.nwords, self.num_input))
    
     
   def get_LM(self):
     return self.RNN
   
   def get_model(self):
     return self.model

   def save(self, path):
     if not os.path.exists(path): os.makedirs(path)
     arr = [ self.num_layers, self.num_input, self.num_hidden, self.W_sm, self.b_sm ]
     self.model.save(path + '/model')
     with open(path + '/model_hyps', 'w') as f: pickle.dump(arr, f) 

   def print_params(self):
      print self.num_layers
      print self.num_input
      print self.num_hidden

   def load_model(self, model, path):
      model.populate(path + '/model')
      with open(path+"/model_hyps", "r") as f: arr = pickle.load(f)
      self.model = model
      self.num_layers = arr[0]
      self.num_input = arr[1]
      self.num_hidden = arr[2]
      self.W_sm = arr[3]
      self.b_sm = arr[4]

   def load_copy(self, model, path):
       if not os.path.exists(path): raise Exception("Model "+path+" does not exist")
       with open(path+"/model_hyps", "r") as f: arr = pickle.load(f)
       model.populate(path + '/model')
       return model

   @staticmethod
   def load(model, path):
       if not os.path.exists(path): raise Exception("Model "+path+" does not exist")
       with open(path+"/model_hyps", "r") as f: arr = pickle.load(f)
       model.populate(path + '/model')
       return model
   
   def calculate_LM_loss(self, sequence):
      
      # Renew the computation graph
      dy.renew_cg()
 
      # Initialize the RNN
      f_init = self.RNN.initial_state()
  
      # Initialize the parameters
      W_exp = dy.parameter(self.W_sm)
      b_exp = dy.parameter(self.b_sm)

      # Get the ids for ICD codes
      wids = [self.vw.w2i[w] for w in sequence]
      #print wids      
      #print wids[0]
      #print dy.lookup(self.lookup, wids[0])

      # Start the RNN
      s = f_init.add_input(dy.lookup(self.lookup, wids[-1])) 

      # Feed the vectors into the RNN and predict the next code
      losses = []
      for wid in wids:
        score = W_exp * s.output() + b_exp
        loss = dy.pickneglogsoftmax(score, wid)
        losses.append(loss)
        s = s.add_input(self.lookup[wid]) 
      return dy.esum(losses)
  

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






if debug == 1:
   m = dy.Model()
   A = language_model(1,128,256,m)
   A.save("test_LM.save")
   A.print_params()

   m2 = dy.Model()
   B = language_model(1,128,256,m2)
   B.load_model(m, 'test_LM.save')
   B.print_params()



