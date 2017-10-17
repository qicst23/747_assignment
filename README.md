# 747_assignment
Repo to hold 747 assignment and project. 

To train the latest models,

cd assignment_01/scripts and run

sh train.sh

train.sh basically runs the training with
a) different hidden layer configs and 
b) different number of medical codes in the current visit to consider while predicting the diagnosis in the next visit

and puts the models into the folder models_$$. 
See the script **_train_**.py for specific details.
