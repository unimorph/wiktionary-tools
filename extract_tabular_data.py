# -*- coding: utf-8 -*-
import codecs
import re
import pandas as pd
import argparse
from collections import defaultdict
import sys
import os

#gather arguments
parser = argparse.ArgumentParser(description='Extract tabular paradigms from annotated templates.')
parser.add_argument('-candidates_dir',action='store',dest='candidates_dir',help='Location of candidate html pages.')
parser.add_argument('-annotation_dir',action='store',dest='annotation_dir',help='Location of raw/annotated table templates.')
parser.add_argument('-language',action='store',dest='language',help='Language to grab.')
args = parser.parse_args()

#regular expressions
lempat = r'<h1.*?>(.*?)</h1>'
locpat1 = r'</h2>.*?</h2>'
locpat2 = r'</h2>.*?</body>'
pospat = r'>(.*?)</h3>'


#input tables
orig_dir = os.path.join(args.annotation_dir,'raw_tables/') #original example tables for comparison #CHANGE
done_dir = os.path.join(args.annotation_dir,'annotated_tables/') #annotated example tables #CHANGE

#output directory
out_dir = './tabular_results/' #output data goes here
if not os.path.exists(out_dir):
	os.makedirs(out_dir)

#language
language = args.language

#output file
fout_name = out_dir + language + '_tabular_paradigms.txt'
fout = codecs.open(fout_name,'wb','utf-8')

#get the table patterns
n_tables = {}
v_tables = {}
adj_tables = {}

#loop through annotated directory
for n in os.listdir(done_dir + language):
	if n.endswith('example.csv'):
		mod_set = {}
		try:
			odata = pd.read_csv(orig_dir+language+'/'+n,dtype='unicode').fillna('')
			ddata = pd.read_csv(done_dir+language+'/'+n,dtype='unicode').fillna('')
		except:
			print(n)
			raise
		try:
			assert(odata.shape == ddata.shape) #make sure we really got the same table
		except:
			print(n)
			print(odata)
			print(ddata)
			print(odata.shape)
			print(ddata.shape)
			raise
		for i in range(odata.shape[0]):
			for j in range(odata.shape[1]):
				if odata.iloc[i,j] != ddata.iloc[i,j]:
					mod_set[(i,j)] = ddata.iloc[i,j]
		#if there were some actual annotations store them
		if len(mod_set) > 0:
			if n.startswith('N_'):
				n_tables[odata.shape] = mod_set
			if n.startswith('ADJ_'):
				adj_tables[odata.shape] = mod_set
			if n.startswith('V_'):
				v_tables[odata.shape] = mod_set


# #loop through languages
lnames = os.listdir(args.candidates_dir) #CHANGE
for ln in lnames:
	if ln == language: 
		names = os.listdir(os.path.join(args.candidates_dir, ln)) #CHANGE
		#loop through language pages
		#count = 0
		for n in names:
			#if n.startswith('candidate_33623.html'):
			if n.startswith('candidate'):
				fin = codecs.open(os.path.join(args.candidates_dir,ln,n),'rb','utf-8') #CHANGE
				page = fin.read().replace('<br>','|')
				fin.close()

				#get the lemma from the page
				match = re.search(lempat,page,flags=re.U|re.DOTALL)
				if match:
					lemma = match.group(1)
					#print lemma

					
					#adjectives
					match = re.search(ln+locpat1,page,flags=re.U|re.DOTALL)
					if not match:
						match = re.search(ln+locpat2,page,flags=re.U|re.DOTALL)
					if match:
						text = match.group()
						if u'Adjective</h3' in text:
							try:
								data = pd.read_html(text)
								if len(data) >= 1:
									data = pd.concat(data)
									shape = data.shape
									if shape in adj_tables:
										for mod,feats in adj_tables[shape].items():
											word = data.iloc[mod[0],mod[1]]
											if not pd.isnull(word):
												fout.write(lemma + '\t' + word + '\t' + feats + '\n')
										fout.write('\n')
							except:
								#if data.shape == (6,8):
								#	print data
								#	raise
								fout.write('----\t----\t----\n')
								fout.write('\n')
								pass

					#nouns
					match = re.search(ln+locpat1,page,flags=re.U|re.DOTALL)
					if not match:
						match = re.search(ln+locpat2,page,flags=re.U|re.DOTALL)
					if match:
						text = match.group()
						if u'Noun</h3>' in text:
							try:
								data = pd.read_html(text)
								if len(data) >= 1:
									data = pd.concat(data)
									shape = data.shape
									#SOME RUSSIAN HACKING
									if language == 'Russian' and lemma == u'дом':
										print(data)
										print(shape)
										print(n)
									#END RUSSIAN HACKING
									#SOME ARMENIAN HACKING
									if language == 'Armenian' and shape == (22,3):
										if data.iloc[1,1] == 'singular':
											shape = (23,3)
										#if 'Audio' in data.iloc[]
									#SOME HUNGARIAN HACKING
									if language == 'Hungarian':
										if data.iloc[2,1] == 'singular':
											shape = (30,3)
									#END ARMENIAN HACKING
									if shape in n_tables:
										for mod,feats in n_tables[shape].items():
											word = data.iloc[mod[0],mod[1]]
											#TEMPORARY ARMENIAN HACK
											#if word == 'plural':
											#	print data.iloc[1,1]
											#	print data.shape
											#END TEMPORARY ARMENIAN HACK
											#	data.to_csv('armenian_tmp.csv',encoding='utf-8',index=False)
											if not pd.isnull(word):
												fout.write(lemma + '\t' + word + '\t' + feats + '\n')
										fout.write('\n')
							except:
								#raise
								fout.write('----\t----\t----\n')
								fout.write('\n')
								#raise
								pass

					#verbs
					match = re.search(ln+locpat1,page,flags=re.U|re.DOTALL)
					if not match:
						match = re.search(ln+locpat2,page,flags=re.U|re.DOTALL)
					if match:
						text = match.group()
						if u'Verb</h3>' in text:
							try:
								data = pd.read_html(text)
								if len(data) >= 1:
									data = pd.concat(data)
									shape = data.shape
									#SOME RUSSIAN HACKING
									if language == 'Russian' and lemma == u'дом':
										print(data)
										print(shape)
										print(n)
									#END RUSSIAN HACKING

									#SPANISH HACK START
									if language == 'Spanish' and lemma == 'hablar':
										shape = (23,8)
									#SPANISH HACK END
									if shape in v_tables:
										for mod,feats in v_tables[shape].items():
											word = data.iloc[mod[0],mod[1]]
											if not pd.isnull(word):
												fout.write(lemma + '\t' + word + '\t' + feats + '\n')
										fout.write('\n')
							except:
								#print feats
								fout.write('----\t----\t----\n')
								fout.write('\n')
								#raise
								pass




#clean up
fout.close()















