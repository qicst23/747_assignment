import os
from collections import defaultdict
import numpy as np

folder = '../data_parsed'
sequencable_array = []
for (dirpath, dirnames, filenames) in os.walk(folder):
     filenames = sorted(filenames)
     count = 0    
     for file in filenames:
        if file.endswith('.codes'):
           count += 1
     if count > 1:
        for file in filenames:
           if file.endswith('.codes'):
             sequencable_array.append(dirpath + '/' + file)


# '../data_parsed/10924/0001_181890.codes', '../data_parsed/31439/0000_112353.codes', '../data_parsed/31439/0001_114626.codes'
sscount = 0
input_sequences = []
output_sequences = []
subject_previous = ' '
sequence_previous = ' '
for arr in sequencable_array:
    subject = arr.split('/')[-2]   
    if sscount == 0:
       print subject
       sscount += 1
    if subject == subject_previous:
       with open(arr, 'r') as f:
           lines = f.readlines()
           sequence = ' '.join(k.split('\n')[0] for k in lines)
           if sscount == 1:
              sequence_previous = sequence
              sscount += 1
              continue
           else: 
              input_sequences.append(sequence_previous)
              output_sequences.append(sequence)
              sequence_previous = sequence
    else:
           subject_previous = subject
           sscount = 1
print "Input Sequence: ",  input_sequences[0]
print "Output Sequence: ",  output_sequences[0]
print "The number of sequences: ", len(input_sequences)


icd_codes = defaultdict(lambda: len(icd_codes))

def make_multihot(seq):
  A = np.empty([1,4134])
  Abar = A.tolist()[0]
  for code in seq:
     icd = icd_codes[code]
     Abar[icd] = 1
  return ' '.join(str(a) for a in Abar)
     



f = open('input_sequences','w')
g = open('output_sequences','w')

for seq in input_sequences:
   f.write(make_multihot(seq) + '\n')
for seq in output_sequences:
   g.write(make_multihot(seq) + '\n')

