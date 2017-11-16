import sys
import cPickle


def convert_to_icd9(dxStr):
    if dxStr.startswith('E'):
        if len(dxStr) > 4: return dxStr[:4] + '.' + dxStr[4:]
        else: return dxStr
    else:
        if len(dxStr) > 3: return dxStr[:3] + '.' + dxStr[3:]
        else: return dxStr

def convert_to_3digit_icd9(dxStr):
    if dxStr.startswith('E'):
        if len(dxStr) > 4: return dxStr[:4]
        else: return dxStr
    else:
        if len(dxStr) > 3: return dxStr[:3]
        else: return dxStr




if __name__ == '__main__':
    diagnosisFile = '../../data/mimic3/mimic/mimic-code/data/DIAGNOSES_ICD.csv'
    outFile = 't'

    print "Building admission to ICD code list mapping"
    admission_code_map = {}
    admission_code_map_3digit = {}
    infd = open(diagnosisFile, 'r')
    infd.readline()
    for line in infd:
     try:
        tokens = line.strip().split(',')
        admission = int(tokens[2])
        sequence = int(tokens[3])
        code_str = 'D_' + convert_to_icd9(tokens[4][1:-1])
        code_str_3digit = 'D_' + convert_to_3digit_icd9(tokens[4][1:-1])
     except ValueError:
        print "Value Error at admission ID: ", admission , " and code ", code_str     
        if admission in admission_code_map: admission_code_map[admission].insert(sequence, code_str)
        else: 
          admission_code_map[admission] = ['']
          admission_code_map[admission].insert(sequence, code_str) 

