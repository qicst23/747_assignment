#!/usr/bin/sh


for i in 1 2 3 4 5 
 do
  for j in 16 32 64 128 256 512
   do
   
     python 08_train_seq2imp_printprediction_firstN.py ${i} ${j}
   done
 done

