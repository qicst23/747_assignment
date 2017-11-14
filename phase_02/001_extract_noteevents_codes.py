#!/usr/bin/python

import os, sys
import csv
from collections import defaultdict

icd_ids = defaultdict(lambda: len(icd_ids))
debug = 1

diagnosis_file = '../../data/mimic3/mimic/mimic-code/data/DIAGNOSES_ICD.csv'
noteevents_file = '../../data/mimic3/mimic/mimic-code/data/NOTEEVENTS.csv' 

#"ROW_ID","SUBJECT_ID","HADM_ID","SEQ_NUM","ICD9_CODE"
subject_id_array = []
admission_id_array = []
sequence_num_array = []
icd_code_array = []
with open(diagnosis_file , 'r') as f:
    lines = f.readlines()
    for line  in lines[1:]:
        row = line.split('\n')[0]
        subject_id_array.append(row.split(',')[1])
        admission_id_array.append(row.split(',')[2])
        sequence_num_array.append(row.split(',')[3])
        icd_code_array.append(row.split(',')[4])

# For every subject, create a folder
admission_count = -1
admission_previous = ' '
subject_previous = ' ' 
for (count, subject) in enumerate(subject_id_array):
   if subject == "11897":
     debug = 1
   else:
     debug = 0
   if debug :
      print "Processing the subject ", subject
   path = '../data_parsed/' + subject
   admission_id = admission_id_array[count]
   if debug:
      print "Admission ID ", admission_id
   if admission_id == admission_previous and subject == subject_previous:
       pass
   elif subject == subject_previous and admission_id != admission_previous:   # Same patient but new visit
       admission_count += 1
       admission_previous = admission_id
   elif subject != subject_previous:
       admission_count = 0
       subject_previous = subject
       admission_previous = admission_id
   icd_code = icd_code_array[count]
   icd_code = icd_code.strip('"')[0:4]
   if not os.path.exists(path):
      os.makedirs(path)
   text_file = path + '/' + str(admission_count).zfill(4) + '_' + admission_id + '.codes' 
   text_file = path + '/' + admission_id + '.codes'
   if admission_count == -1:
      g = open(text_file,'w')
      g.close()
      admission_count += 1
   else:
     with open(text_file ,'a') as g:
       if len(icd_code) < 3:
          print admission_id, subject 
          continue
       else:
          icd_ids[icd_code]
          g.write(icd_code + '\n')
      
'''   
subject_id_array = []
admission_id_array = []
text_array = []
c = 1
with open(noteevents_file, 'r') as f:
    lines = csv.reader(f)
    for line  in lines:
     if c == 1:
      c +=1
      pass 
     else:
        #row = line.split('\n')[0].split()
        row = line
        #print "Row: ", row
        subject_id_array.append(row[1])
        admission_id_array.append(row[2])
        text_array.append(row[-1])

# For every subject, update the text

for (subject, admission, text) in zip(subject_id_array, admission_id_array, text_array):
      path = '../data_parsed/' + subject
      text_file = path + '/' +  admission + '.noteevents'
      with open(text_file ,'a') as g:
        g.write(text + '\n')

      
'''

f = open('icd_ids.txt','w')
for icd_id in icd_ids:
    f.write( 'My id for the icd code  ' + str(icd_id) + ' is ' + str(icd_ids[icd_id]) + '\n')
f.close()
