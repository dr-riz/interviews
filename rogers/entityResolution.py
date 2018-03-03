print("Entity Resolution!")

import string
import csv
# stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# stemming of words
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

dblp_tsv = "DBLP1.txt.tsv"
scholar_tsv = "Scholar.txt.tsv"
db_scholar_tsv = "DBLP_Scholar_perfectMapping_RizwanMian.csv"

id_idx = 0
title_idx = 1
author_idx = 2
venue_idx = 3
yr_idx = 4
rowid_dx = 5

# remove punctuation from each word
#print(string.punctuation)
table = str.maketrans('', '', string.punctuation)
#print(table)

dblp_pubs = []
scholar_pubs = []
match_pubs=[]

def read_pubs(in_file):
	pubs = []
	with open(in_file, "rb") as ins:	
		for line in ins:
			line = line.decode('ascii').strip()
			#preprocessing: lowercase
			line = line.lower()
			tokens=line.split('\t')
			#preprocessing: removed punctuation
			#publication = [w.translate(table) for w in tokens]
			publication = tokens
			#preprocessing: Filter out Stop Words [from the title] e.g. our, it etc.
	#	    	print(publication[title_idx])
	#	    	publication[title_idx] = \
	#	    		[w for w in publication[title_idx] if not w in stop_words]
	#   		print(publication[title_idx])
			#preprocessing: stemming of words e.g. fishing, fished reduce to stem fish
	#	    	print(publication[title_idx])
	#	    	publication[title_idx] = \
	#	    		[porter.stem(w) for w in publication[title_idx]]	
	#	    	print(publication[title_idx])
			pubs.append(publication)
	return pubs


def entityResolution(first_list, second_list):
	num_matches=0
	num_index_errors=0
	matched = []
	for aRrecord in first_list:
		for idx, bRecord in enumerate(second_list):
			try:
				#print(bRecord)
				if((aRrecord[yr_idx] == bRecord[yr_idx]) and \
					(aRrecord[author_idx] == bRecord[author_idx]) and \
					(aRrecord[title_idx] == bRecord[title_idx])):
					num_matches+=1
														
					matched.append(([aRrecord,bRecord]))
						
				    #print match idx in the 2nd list
					#print("match: " + str(idx))

			except IndexError:
				num_index_errors+=1
				continue
	
	print("num_matches=" + str(num_matches))
	print("num_index_errors=" + str(num_index_errors))
	return matched

dblp_idx=0
scholar_idx=1

def dedup(pub_list, in_file):
	print("before dedup, len(pub_list)=" + str(len(pub_list)))
	out_file=in_file + "_dups.tsv"	
	file_handler = open(out_file,"w")
	file_handler.write("id \t title \t author \t venue \t year \t rowid \n")
	num_duplicates=0
	num_index_errors=0
	
	for aRrecord in pub_list:
		for idx, bRecord in enumerate(pub_list):
			try:
				#print(bRecord)
				if((aRrecord[dblp_idx][rowid_dx] != bRecord[dblp_idx][rowid_dx]) and \
					(aRrecord[dblp_idx][yr_idx] == bRecord[dblp_idx][yr_idx]) and \
					(aRrecord[dblp_idx][author_idx] == bRecord[dblp_idx][author_idx]) and \
					(aRrecord[dblp_idx][title_idx] == bRecord[dblp_idx][title_idx])):
					num_duplicates+=1
					
					file_handler.write(aRrecord[dblp_idx][id_idx] + "\t" + aRrecord[dblp_idx][title_idx] + "\t" + \
						aRrecord[dblp_idx][author_idx] + "\t" + aRrecord[dblp_idx][venue_idx] + "\t" + \
						aRrecord[dblp_idx][yr_idx] + "\t" + aRrecord[dblp_idx][rowid_dx] + "\n")
				
					file_handler.write(bRecord[dblp_idx][id_idx] + "\t" + bRecord[dblp_idx][title_idx] + "\t" + \
						bRecord[dblp_idx][author_idx] + "\t" + bRecord[dblp_idx][venue_idx] + "\t" + \
						bRecord[dblp_idx][yr_idx] + "\t" + bRecord[dblp_idx][rowid_dx] + "\n")
			
					#remove duplicate from the list
					#print("deleting: " + str(idx))
					del pub_list[idx]
			except IndexError:
				num_index_errors+=1
				continue
	
	print("num_duplicates=" + str(num_duplicates))
	print("after dedup, len(pub_list)=" + str(len(pub_list)))
	print("num_index_errors=" + str(num_index_errors))
	print("for validation/reference, duplicates stored in " + out_file)
	file_handler.close()
	return pub_list


	
dblp_pubs = read_pubs(dblp_tsv)	
scholar_pubs = read_pubs(scholar_tsv)	

#dedup(scholar_pubs, scholar_tsv) # disabling since only 23 duplicates, and takes a very long time to search
#print("after dedup, len(scholar_pubs)=" + str(len(scholar_pubs)))

#entityResolution(dblp_pubs,scholar_pubs)
match_pubs = entityResolution(dblp_pubs,dblp_pubs)

print("before dedup, len(match_pubs)=" + str(len(match_pubs)))
dedup_pubs = dedup(match_pubs, db_scholar_tsv)
print("after dedup, len(dedup_pubs)=" + str(len(dedup_pubs)))


out_file=db_scholar_tsv
file_handler = open(out_file,"w")
file_handler.write('idDBLP,idScholar,DBLP_Match,Scholar_Match,Match_ID\n')
for match in dedup_pubs:
	file_handler.write(match[dblp_idx][id_idx] + "," + match[scholar_idx][id_idx] + "," + \
		match[dblp_idx][rowid_dx] + "," + match[scholar_idx][rowid_dx] + "," + \
		match[dblp_idx][rowid_dx] + "_" + match[scholar_idx][rowid_dx] + "\n")
file_handler.close()