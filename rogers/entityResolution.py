print("Entity Resolution!")

import string
import csv
# stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# stemming of words
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

dblp_csv = "DBLP.tsv"
scholar_csv = "Scholar.csv"
db_scholar_csv = "DBLP_Scholar_perfectMapping_RizwanMian.csv"

#with open(dblp_fn) as f:
#    lines = f.readlines()
#print(lines)

dblp_id_idx = 0
dblp_title_idx = 1
dblp_author_idx = 2
dblp_venue_idx = 3
dblp_yr_idx = 4
dblp_rowid_dx = 5

def is_ascii(s):
    try:
        s.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

# remove punctuation from each word
print(string.punctuation)
table = str.maketrans('', '', string.punctuation)
#print(table)

records=0
readable_records=0
dblp_pubs = []

with open(dblp_csv, "rb") as ins:	
    for line in ins:
    	records += 1
    	if (is_ascii(line)):
    		readable_records+=1
    		line = line.decode('ascii').strip()
			#preprocessing: lowercase
    		line = line.lower()
	    	tokens=line.split('\t')
	    	#preprocessing: removed punctuation
	    	publication = [w.translate(table) for w in tokens]
	    	#preprocessing: Filter out Stop Words [from the title] e.g. our, it etc.
#	    	print(publication[dblp_title_idx])
#	    	publication[dblp_title_idx] = \
#	    		[w for w in publication[dblp_title_idx] if not w in stop_words]
 #   		print(publication[dblp_title_idx])
	    	#preprocessing: stemming of words e.g. fishing, fished reduce to stem fish
#	    	print(publication[dblp_title_idx])
#	    	publication[dblp_title_idx] = \
#	    		[porter.stem(w) for w in publication[dblp_title_idx]]	
#	    	print(publication[dblp_title_idx])
	    	dblp_pubs.append(publication)

print("publications processed=" + str(readable_records/records*100))


dblp_id_idx = 0
dblp_title_idx = 1
dblp_author_idx = 2
dblp_venue_idx = 3
dblp_yr_idx = 4
dblp_rowid_dx = 5

dup_records="duplicate_records.tsv"
file_handler = open(dup_records,'w') 
num_duplicates=0
file_handler.write("id \t title \t author \t venue \t year \t rowid \n")
for aRrecord in dblp_pubs:
	for bRecord in dblp_pubs:
		if((aRrecord[dblp_rowid_dx] != bRecord[dblp_rowid_dx]) and \
			#(aRrecord[dblp_id_idx] == bRecord[dblp_id_idx]) and \
			#(aRrecord[dblp_yr_idx] == bRecord[dblp_yr_idx]) and \
			(aRrecord[dblp_author_idx] == bRecord[dblp_author_idx]) and \
			(aRrecord[dblp_title_idx] == bRecord[dblp_title_idx])):
			num_duplicates+=1
					
			file_handler.write(aRrecord[dblp_id_idx] + "\t" + aRrecord[dblp_title_idx] + "\t" + \
				aRrecord[dblp_author_idx] + "\t" + aRrecord[dblp_venue_idx] + "\t" + \
				aRrecord[dblp_yr_idx] + "\t" + aRrecord[dblp_rowid_dx] + "\n")
				
			file_handler.write(bRecord[dblp_id_idx] + "\t" + bRecord[dblp_title_idx] + "\t" + \
				bRecord[dblp_author_idx] + "\t" + bRecord[dblp_venue_idx] + "\t" + \
				bRecord[dblp_yr_idx] + "\t" + bRecord[dblp_rowid_dx] + "\n")				

print("num_duplicates=" + str(num_duplicates));
file_handler.close() 			
			#print("duplicate with rowids: " + aRrecord[dblp_rowid_dx] + "," + \
			#	bRecord[dblp_rowid_dx])


#i=0;
#while i in range(len(dblp_pubs)):
#	i +=1 
#	j = i
#	while j
#    print(colors[i])

    
#file = open(db_scholar_csv,'w') 
#header
#file.write('idDBLP,idScholar,DBLP_Match,Scholar_Match,Match_ID\n') 
#file.write(publication[dblp_id_idx] + "," + publication[dblp_id_idx] + "," + \
#	publication[dblp_rowid_dx] + "," + publication[dblp_rowid_dx] + "," + \
#	publication[dblp_rowid_dx] + "_" + publication[dblp_rowid_dx] + "\n")




#file.close() 
        
#with open(dblp_fn, "rb") as ins:
 #   array = []
  #  for line in ins:
   # 	print(line)
        #array.append(line)
        
