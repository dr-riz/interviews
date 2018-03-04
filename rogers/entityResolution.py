import string
import sys
# stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# stemming of words
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

from fuzzywuzzy import fuzz

print("Entity Resolution!")

dblp_tsv = "DBLP1.txt.tsv"
#dblp_tsv = "debug.tsv"
scholar_tsv = "Scholar.txt.tsv"
db_scholar_tsv = "DBLP_Scholar_perfectMapping_RizwanMian.csv"

fuzzy_threshold = 99

id_idx = 0
title_idx = 1
author_idx = 2
venue_idx = 3
yr_idx = 4
rowid_dx = 5

dblp_pubs = []
scholar_pubs = []
match_pubs=[]


def read_pubs(in_file):
	pubs = []
	counter=0
	table = str.maketrans('', '', string.punctuation)
	with open(in_file, "rb") as ins:
		header_line = next(ins) #ignore header
		for line in ins:
			line = line.decode('ascii').strip()
			tokens=line.split('\t')

			#preprocessing: lowercase
			tokens[title_idx] = tokens[title_idx].lower()
			tokens[author_idx] = tokens[author_idx].lower()
			tokens[venue_idx] = tokens[venue_idx].lower()
			
			#print("tokens[author_idx]=" + " ".join(tokens[author_idx]))
			
			#preprocessing: remove punctuation	
			tokens[title_idx] = tokens[title_idx].translate(table)
			tokens[author_idx] = tokens[author_idx].translate(table)
			
			# remove author initials (up to 2 alphabets) from author names
			tokens[author_idx] = " ".join([w for w in tokens[author_idx].split(" ") if len(w) > 2])

			#print("tokens[author_idx]=" + " ".join(tokens[author_idx]))
			
			# preprocessing: remove stop words e.g. 'the’, ‘is’, ‘are' from title		
			tokens[title_idx] = " ".join([w for w in tokens[title_idx].split(" ") if not w in stop_words])			
						
			# preprocessing: stemming of words e.g. fishing, fished reduce to stem fish									
			tokens[title_idx] = " ".join([porter.stem(w) for w in tokens[title_idx].split(" ")])	
						
			#print(tokens[author_idx])
			#if(counter==4):
				#sys.exit()
			publication = tokens
			pubs.append(publication)
			counter+=1
	return pubs

def entityResolution(first_list, second_list):
	num_matches=0
	num_index_errors=0
	counter=0
	matched = []
	out_file="matched.tsv"
	file_handler = open(out_file,"w")
	file_handler.write("did \t dtitle \t dauthor \t dvenue \t dyear \t drowid\n")	
	for aRecord in first_list:
		for idx, bRecord in enumerate(second_list):
			try:
				counter+=1
				#if(counter==4):
				#	sys.exit()
									
				#print("aRecord=" + ",".join(aRecord))
				#print("bRecord=" + ",".join(bRecord))
				
				a_authors=aRecord[author_idx]
				b_authors=bRecord[author_idx]
				
				if(a_authors!="" or b_authors!=""):
					author_ratio=fuzz.ratio(a_authors,b_authors)
				else:
					author_ratio=100					
										
				title_ratio=fuzz.token_sort_ratio(aRecord[title_idx],bRecord[title_idx])
				#print("author_ratio,title_Ratio=" + str(author_ratio) + "," + str(title_ratio))
				if((aRecord[yr_idx] == bRecord[yr_idx]) and \
					author_ratio >= fuzzy_threshold and \
					title_ratio >= fuzzy_threshold):
					#(aRecord[author_idx] == bRecord[author_idx]) and \
					#(aRecord[title_idx] == bRecord[title_idx])):
					num_matches+=1														
					matched.append(([aRecord,bRecord]))
				
					file_handler.write("\t".join(aRecord) + "\n")
					file_handler.write("\t".join(bRecord) + "\n")
			except IndexError:
				num_index_errors+=1
				continue
	print("num_matches=" + str(num_matches))
	print("num_index_errors=" + str(num_index_errors))
	file_handler.close()
	return matched

dblp_idx=0
scholar_idx=1

def dedup(pub_list, in_file):
	print("before dedup, len(pub_list)=" + str(len(pub_list)))
	out_file=in_file + "_dups.tsv"	
	file_handler = open(out_file,"w")
	file_handler.write("did \t dtitle \t dauthor \t dvenue \t dyear \t drowid \t sid \t stitle \t sauthor \t svenue \t syear \t srowid \n")
	num_duplicates=0
	num_index_errors=0
	
	for aRecord in pub_list:
		for idx, bRecord in enumerate(pub_list):
			try:
				a_id = aRecord[dblp_idx][id_idx]
				b_id = bRecord[dblp_idx][id_idx]
				a_rowid = aRecord[dblp_idx][rowid_dx]
				b_rowid = bRecord[dblp_idx][rowid_dx]
				a_yr = aRecord[dblp_idx][yr_idx]
				b_yr = bRecord[dblp_idx][yr_idx]
				a_authors = aRecord[dblp_idx][author_idx]
				b_authors = bRecord[dblp_idx][author_idx]
				a_title = aRecord[dblp_idx][title_idx]
				b_title = bRecord[dblp_idx][title_idx]
				a_venue = aRecord[dblp_idx][venue_idx]
				b_venue = bRecord[dblp_idx][venue_idx]
				
				if(a_authors!="" or b_authors!=""):
					author_ratio=fuzz.ratio(a_authors,b_authors)
				else:
					author_ratio=100		
				
				title_ratio=fuzz.token_sort_ratio(a_title,b_title)
				
				if((a_rowid != b_rowid) and \
					(a_yr == bRecord[dblp_idx][yr_idx]) and \
					(author_ratio >= fuzzy_threshold) and \
					(title_ratio >= fuzzy_threshold)):
					
#				if((a_rowid != b_rowid) and \
#					(a_yr == bRecord[dblp_idx][yr_idx]) and \
#					(a_authors == b_authors) and \
#					(a_title == b_title)):
					num_duplicates+=1
					
					file_handler.write(a_id + "\t" + a_title + "\t" + \
						a_authors + "\t" + a_venue + "\t" + \
						a_yr + "\t" + a_rowid + "\t" )
						
					file_handler.write(aRecord[scholar_idx][id_idx] + "\t" + aRecord[scholar_idx][title_idx] + "\t" + \
						aRecord[scholar_idx][author_idx] + "\t" + aRecord[scholar_idx][venue_idx] + "\t" + \
						aRecord[scholar_idx][yr_idx] + "\t" + aRecord[scholar_idx][rowid_dx] + "\n")
				
					file_handler.write(b_id + "\t" + b_title + "\t" + \
						b_authors + "\t" + b_venue + "\t" + \
						b_yr + "\t" + b_rowid + "\t" )
					
					file_handler.write(bRecord[scholar_idx][id_idx] + "\t" + bRecord[scholar_idx][title_idx] + "\t" + \
						bRecord[scholar_idx][author_idx] + "\t" + bRecord[scholar_idx][venue_idx] + "\t" + \
						bRecord[scholar_idx][yr_idx] + "\t" + bRecord[scholar_idx][rowid_dx] + "\n")
			
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
#scholar_pubs = read_pubs(scholar_tsv)	
#match_pubs = entityResolution(dblp_pubs,scholar_pubs)
match_pubs = entityResolution(dblp_pubs,dblp_pubs)
dedup_pubs = dedup(match_pubs, db_scholar_tsv)
dedup_pubs = match_pubs


out_file=db_scholar_tsv
print("dedup ER stored in " + out_file)
file_handler = open(out_file,"w")
file_handler.write('idDBLP,idScholar,DBLP_Match,Scholar_Match,Match_ID\n')
for match in dedup_pubs:
	file_handler.write(match[dblp_idx][id_idx] + "," + match[scholar_idx][id_idx] + "," + \
		match[dblp_idx][rowid_dx] + "," + match[scholar_idx][rowid_dx] + "," + \
		match[dblp_idx][rowid_dx] + "_" + match[scholar_idx][rowid_dx] + "\n")
file_handler.close()