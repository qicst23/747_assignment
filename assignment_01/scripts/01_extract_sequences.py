#!/usr/bin/python

# This is a script to extract the sequence of medical codes from the diagnoses

import os, sys
import numpy

diagnosis_file = '../data/DIAGNOSES_ICD.csv'

# Read the file and populate the sequences array
sequences = []
visits = []
f = open(diagnosis_file)
count = 0 
seq = []
for line in f:
   if count == 0:
     count += 1
     continue
   line = line.split('\n')[0].split(',')
   visit_ID = line[2]
   icd_code = str(line[-1])
   #print "ICD code ", icd_code
   if count == 1:
     previous = visit_ID
     count += 1
   if previous == visit_ID:
     #print "Accumulating ", icd_code
     seq.append(icd_code)
   else:
     #print "Appending sequence " , seq
     sequences.append(seq)
     previous = visit_ID
     visits.append(visit_ID)
     seq = [icd_code]

assert len(visits) == len(sequences)
print len(sequences), len(visits)
print "Done"

g = open('../data/sequences.txt','w')
for seq in sequences:
    print seq
    g.write(' '.join(k for k in seq) + '\n')
g.close()
f.close()
