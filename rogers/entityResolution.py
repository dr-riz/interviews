import csv

print("Entity Resolution!")

dblp_csv = "DBLP2.csv"
scholar_csv = "Scholar.csv"
db_scholar_csv = "DBLP_Scholar_perfectMapping_RizwanMian.csv"
hw_csv = "hw.csv"

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

counter=0
with open(dblp_csv, "rb") as ins:
    dblp_pubs = []
    for line in ins:
    	if (is_ascii(line)):
    		counter+=1
	    	print(line)
    	#line.strip()
    	#line = line.decode('utf8').strip()
    	#publication=line.split('\t')
    	#dblp_pubs.append(publication)
    	#print(publication)
    	
    	#break
		#content = [line.strip() for x in line.split(',')]
        #print content
        #break
        #array.append(line)
#print(dblp_pubs) 

print(counter)
#for aRrecord in dblp_pubs:
#	for bRecord in dblp_pubs:
#		if(aRrecord[dblp_author_idx] == bRecord[dblp_author_idx]):
#			print("duplicate with rowids: " + aRrecord[dblp_rowid_dx] + "," + \
#				bRecord[dblp_rowid_dx] + "\n")

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