
import os, sys
import numpy as np

patient_sequences = '../data/patient_sequences.txt'

# Read the file into an array
sequences_array = []
f = open(patient_sequences)
for line in f:
    line = line.split('\n')[0]
    sequences_array.append(line)


sequencepairs_array = []
# Ngram the array and pick sequences
for (a,b) in zip(*[sequences_array[i:] for i in range(2)]):
    if a.split()[0] == b.split()[0]:
         print  '   Identical. A: ', a, " B: ", b
         sequencepairs_array.append(' '.join(k for k in a.split()[1:]) + ' - ' + ' '.join(k for k in b.split()[1:] ))
    else:
         print " Not the same ", a.split()[0], b.split()[0]

g = open('../data/sequence_pairs.txt','w')
for p in sequencepairs_array:
    g.write(p + '\n')
