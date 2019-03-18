# -*- coding: utf-8 -*-
import codecs
import re
import argparse
import sys

#gather arguments
parser = argparse.ArgumentParser(description='Clean out paradigms with errors.')
parser.add_argument('-language',action='store',dest='language',help='Language.')
args = parser.parse_args()

fin = codecs.open('./tabular_results/' + args.language + '_tabular_paradigms.txt','rb','utf-8') #CHANGE
fout = codecs.open('./tabular_results/' + args.language + '_tabular_paradigms_norm.txt','wb','utf-8') #CHANGE

paradigms = fin.read().split('\n\n')

vcount = 0
ncount = 0
acount = 0

for p in paradigms:
	# Exclude paradigms that caused exceptions during parsing.
	if '----' not in p:
		if '\tV;' in p: vcount += 1
		if '\tN;' in p: ncount += 1
		if '\tADJ;' in p: acount += 1
		fout.write(p + '\n\n')

#print language, number of verbs, adjectives, and nouns
print(args.language,vcount,acount,ncount)

#clean up
fin.close()
fout.close()




