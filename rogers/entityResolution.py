print("Entity Resolution!")

import string

dblp_tsv = "DBLP1.txt.tsv"
scholar_tsv = "Scholar.txt.tsv"
db_scholar_tsv = "DBLP_Scholar_perfectMapping_RizwanMian.csv"

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
	with open(in_file, "rb") as ins:
		header_line = next(ins) #ignore header
		for line in ins:
			line = line.decode('ascii').strip()
			tokens=line.split('\t')
			#preprocessing: lowercase
			tokens[title_idx] = tokens[title_idx].lower()
			tokens[author_idx] = tokens[author_idx].lower()
			tokens[venue_idx] = tokens[venue_idx].lower()			
			publication = tokens
			pubs.append(publication)
	return pubs

def entityResolution(first_list, second_list):
	num_matches=0
	num_index_errors=0
	matched = []
	for aRrecord in first_list:
		for idx, bRecord in enumerate(second_list):
			try:
				if((aRrecord[yr_idx] == bRecord[yr_idx]) and \
					(aRrecord[author_idx] == bRecord[author_idx]) and \
					(aRrecord[title_idx] == bRecord[title_idx])):
					num_matches+=1														
					matched.append(([aRrecord,bRecord]))
	
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
	file_handler.write("did \t dtitle \t dauthor \t dvenue \t dyear \t drowid \t sid \t stitle \t sauthor \t svenue \t syear \t srowid \n")
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
						aRrecord[dblp_idx][yr_idx] + "\t" + aRrecord[dblp_idx][rowid_dx] + "\t" )
						
					file_handler.write(aRrecord[scholar_idx][id_idx] + "\t" + aRrecord[scholar_idx][title_idx] + "\t" + \
						aRrecord[scholar_idx][author_idx] + "\t" + aRrecord[scholar_idx][venue_idx] + "\t" + \
						aRrecord[scholar_idx][yr_idx] + "\t" + aRrecord[scholar_idx][rowid_dx] + "\n")
				
					file_handler.write(bRecord[dblp_idx][id_idx] + "\t" + bRecord[dblp_idx][title_idx] + "\t" + \
						bRecord[dblp_idx][author_idx] + "\t" + bRecord[dblp_idx][venue_idx] + "\t" + \
						bRecord[dblp_idx][yr_idx] + "\t" + bRecord[dblp_idx][rowid_dx] + "\t")
					
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
scholar_pubs = read_pubs(scholar_tsv)	
match_pubs = entityResolution(dblp_pubs,scholar_pubs)
dedup_pubs = dedup(match_pubs, db_scholar_tsv)


out_file=db_scholar_tsv
print("dedup ER stored in " + out_file)
file_handler = open(out_file,"w")
file_handler.write('idDBLP,idScholar,DBLP_Match,Scholar_Match,Match_ID\n')
for match in dedup_pubs:
	file_handler.write(match[dblp_idx][id_idx] + "," + match[scholar_idx][id_idx] + "," + \
		match[dblp_idx][rowid_dx] + "," + match[scholar_idx][rowid_dx] + "," + \
		match[dblp_idx][rowid_dx] + "_" + match[scholar_idx][rowid_dx] + "\n")
file_handler.close()