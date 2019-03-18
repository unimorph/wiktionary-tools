# -*- coding: utf-8 -*-
import codecs
import re
import pandas as pd
import argparse
from collections import defaultdict
import os

#grab arguments
parser = argparse.ArgumentParser(description='Extract tabular paradigms from annotated templates.')
parser.add_argument('-candidates_dir',action='store',dest='candidates_dir',help='Location of html candidates.')
args = parser.parse_args()

#regular expressions
locpat1 = r'</h2>.*?</h2>'
locpat2 = r'</h2>.*?</body>'

#output tables written here
out_dir1 = './raw_tables/' #CHANGE
out_dir2 = './annotated_tables/' #CHANGE

#loop through languages
lnames = os.listdir(args.candidates_dir) #CHANGE
for ln in lnames:
	#if not ln.startswith('.') and ln == 'Greek': #CHANGE THIS FILTER
	if not ln.startswith('.'):
	#if ln == 'Bengali': #test on Bengali first...
		print(ln) #what language are you working on...

		adj_shape_count_dict = defaultdict(int)
		adj_shape_example_dict = {}
		n_shape_count_dict = defaultdict(int)
		n_shape_example_dict = {}
		pn_shape_count_dict = defaultdict(int)
		pn_shape_example_dict = {}
		v_shape_count_dict = defaultdict(int)
		v_shape_example_dict = {}

		names = os.listdir(os.path.join(args.candidates_dir,ln)) #CHANGE
		#loop through language pages
		for n in names:
			#if n.startswith('candidate_377012.html'):
			if n.startswith('candidate'):
				fin = codecs.open(os.path.join(args.candidates_dir, ln, n),'rb','utf-8') #CHANGE
				page = fin.read()
				fin.close()

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
								adj_shape_count_dict[shape] += 1
								adj_shape_example_dict[shape] = data
						except:
							#print('ADJECTIVE ERROR')
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
								n_shape_count_dict[shape] += 1
								n_shape_example_dict[shape] = data
						except:
							#print('NOUN ERROR')
							pass

				#pronouns
				match = re.search(ln+locpat1,page,flags=re.U|re.DOTALL)
				if not match:
					match = re.search(ln+locpat2,page,flags=re.U|re.DOTALL)
				if match:
					text = match.group()
					if u'Pronoun</h3>' in text:
						try:
							data = pd.read_html(text)
							if len(data) >= 1:
								data = pd.concat(data)
								shape = data.shape
								pn_shape_count_dict[shape] += 1
								pn_shape_example_dict[shape] = data
						except:
							#print('PRONOUN ERROR')
							pass

				#verbs
				match = re.search(ln+locpat1,page,flags=re.U|re.DOTALL)
				if not match:
					match = re.search(ln+locpat2,page,flags=re.U|re.DOTALL)
				if match:
					text = match.group()
					if u'Verb</h3>' in text and u'-unud' not in text: #ESTONIAN HACK TO GET BETTER EXAMPLE...
						try:
							data = pd.read_html(text)
							if len(data) >= 1:
								data = pd.concat(data)
								shape = data.shape
								v_shape_count_dict[shape] += 1
								v_shape_example_dict[shape] = data
						except:
							#print('VERB ERROR')
							pass

		#create directories to store output
		if not os.path.exists(out_dir1 + ln):
			os.makedirs(out_dir1 + ln)
		if not os.path.exists(out_dir2 + ln):
			os.makedirs(out_dir2 + ln)

		#write the example outputs for the language
		for shape,table in adj_shape_example_dict.items():
			count = '%06d' % adj_shape_count_dict[shape]
			shape = str(shape).replace(' ','')
			table.to_csv(out_dir1+ln +'/ADJ_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)
			table.to_csv(out_dir2+ln +'/ADJ_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)

		for shape,table in n_shape_example_dict.items():
			count = '%06d' % n_shape_count_dict[shape]
			shape = str(shape).replace(' ','')
			table.to_csv(out_dir1+ln +'/N_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)
			table.to_csv(out_dir2+ln +'/N_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)

		for shape,table in pn_shape_example_dict.items():
			count = '%06d' % pn_shape_count_dict[shape]
			shape = str(shape).replace(' ','')
			table.to_csv(out_dir1+ln +'/PN_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)
			table.to_csv(out_dir2+ln +'/PN_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)

		for shape,table in v_shape_example_dict.items():
			count = '%06d' % v_shape_count_dict[shape]
			shape = str(shape).replace(' ','')
			table.to_csv(out_dir1+ln +'/V_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)
			table.to_csv(out_dir2+ln +'/V_' + count + '_' + shape + '_example.csv',encoding='utf-8',index=False)















