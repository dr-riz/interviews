print("Entity Resolution!")

dblp_fn = "DBLP1.csv"
hw_csv = "hw.csv"

#with open(dblp_fn) as f:
#    lines = f.readlines()
#print(lines)

with open(dblp_fn, "rb") as ins:
    titles = []
    for line in ins:  
    	line = line.decode('utf8').strip()
    	pub_title=line.split(',')[1]
    	titles.append(pub_title)
    	print(pub_title)
    	
    	break
		#content = [line.strip() for x in line.split(',')]
        #print content
        #break
        #array.append(line)
        
        
#with open(dblp_fn, "rb") as ins:
 #   array = []
  #  for line in ins:
   # 	print(line)
        #array.append(line)