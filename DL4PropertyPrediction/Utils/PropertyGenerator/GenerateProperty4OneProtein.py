#!/usr/bin/python


## This script generates the structure properties from native structure, with information encoded in tpl and initial angle file
## the intial angle file is generated by PDB_Tool
## this script is adapted from Yujuan Gao's code, but looks like that further improvement is needed

import os,sys

if len(sys.argv) != 5:
    print 'usage: GenerateProperty4OneProtein.py proteinName tplFile initialAngFile finalAngFile'
    exit(-1)

target = sys.argv[1]
tpl_path = sys.argv[2]
ang_path = sys.argv[3]
out_path = sys.argv[4]

f = open(tpl_path, 'r')
tpls = f.readlines()
f.close()

f = open(ang_path, 'r')
angs = f.readlines()
f.close()

def abstract(ang):
    segs = ang.split()
    angg = ''
    for i in range(2, len(segs)):
        seg = segs[i]
        angg += '\t'
        angg += seg 
    return angg


## read the full sequence from the tpl file
for ll in tpls:
    ll = ll.strip()
    if ll.startswith('SEQRES'):
	segs = ll.split()
	seq = segs[3]
	break

## read the PDB sequence (i.e., DSSP sequence) from the tpl file
for ll in tpls:
    ll = ll.strip()
    if ll.startswith('DSSP'):
	segs = ll.split()
	pdb = segs[3]
	break

pdb_nogaps = pdb.replace('-', '')

assert ( len(angs)-1 == len(pdb_nogaps) )

miss = [ (a!=b) for a, b in zip(seq, pdb) ]

fout = open(out_path, 'w')

fout.write('Missing\t' + angs[0])
ii = 0
for i, missing in zip(range(len(seq)), miss):
    if missing == 1:
	fout.write('%d\t%d\t%c\n' % (missing, i+1, seq[i]))
    else:
	ii += 1
        angg = abstract(angs[ii].strip())
	fout.write('%d\t%d\t%c%s\n' % (missing, i+1, seq[i], angg))

fout.close()
