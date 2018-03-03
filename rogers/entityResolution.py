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
				if((aRrecord[rowid_dx] != bRecord[rowid_dx]) and \
					(aRrecord[yr_idx] == bRecord[yr_idx]) and \
					(aRrecord[author_idx] == bRecord[author_idx]) and \
					(aRrecord[title_idx] == bRecord[title_idx])):
					num_duplicates+=1
					
					file_handler.write(aRrecord[id_idx] + "\t" + aRrecord[title_idx] + "\t" + \
						aRrecord[author_idx] + "\t" + aRrecord[venue_idx] + "\t" + \
						aRrecord[yr_idx] + "\t" + aRrecord[rowid_dx] + "\n")
				
					file_handler.write(bRecord[id_idx] + "\t" + bRecord[title_idx] + "\t" + \
						bRecord[author_idx] + "\t" + bRecord[venue_idx] + "\t" + \
						bRecord[yr_idx] + "\t" + bRecord[rowid_dx] + "\n")
			
					#remove duplicate from the list
					print("deleting: " + str(idx))
					del pub_list[idx]
			except IndexError:
				num_index_errors+=1
				continue
	
	print("num_duplicates=" + str(num_duplicates))
	print("after dedup, len(pub_list)=" + str(len(pub_list)))
	print("num_index_errors=" + str(num_index_errors))
	print("for validation/reference, duplicates stored in " + out_file)
	file_handler.close()
	
#dblp_pubs = read_pubs(dblp_tsv)	
#dedup(dblp_pubs, dblp_tsv)
print("after dedup, len(dblp_pubs)=" + str(len(dblp_pubs)))

scholar_pubs = read_pubs(scholar_tsv)	
dedup(scholar_pubs, scholar_tsv)
		
			#print("duplicate with rowids: " + aRrecord[rowid_dx] + "," + \
			#	bRecord[rowid_dx])


#i=0;
#while i in range(len(dblp_pubs)):
#	i +=1 
#	j = i
#	while j
#    print(colors[i])

    
#file = open(db_scholar_tsv,'w') 
#header
#file.write('idDBLP,idScholar,DBLP_Match,Scholar_Match,Match_ID\n') 
#file.write(publication[id_idx] + "," + publication[id_idx] + "," + \
#	publication[rowid_dx] + "," + publication[rowid_dx] + "," + \
#	publication[rowid_dx] + "_" + publication[rowid_dx] + "\n")




#file.close() 
        
#with open(dblp_fn, "rb") as ins:
 #   array = []
  #  for line in ins:
   # 	print(line)
        #array.append(line)
        
