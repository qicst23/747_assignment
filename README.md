# 747_assignment
Repo to hold 747 assignment and project. 

To train the latest models,

cd assignment_01/scripts and run

sh train.sh

train.sh basically runs the training with  
a) different hidden layer configs and   
b) different number of medical codes in the current visit to consider while predicting the diagnosis in the next visit  

and puts the models into the folder models_$$. 
See the corresponding **_train_**.py for specific details.


Experiment configs available:

1) Training the medical codes of a particular visit to discover the structure among the diagnosed diseases ( similar to Language Modeling ) - 02_rnnlm.py  
2) Training the medical codes of current visit to predict the medical codes in the next visit - 06_train_seq2seq.py  
3) Training the medical codes of current visit to predict the most important disease code in the next visit ( similar to Machine Translation ) - 07_train_seq2imp_printprediction.py  
4) Training on the first N medical codes of current visit to predict the most important disease code in the next visit - 08_train_seq2imp_printprediction_firstN.py


Experiments about hierarchical attention in the sub folder phase_02

Running the basic scripts populates a whole bunch of folders ( one for each patient )
