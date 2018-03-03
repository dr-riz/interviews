print("generating readable data!\n")

import string

dblp_txt = "DBLP1.txt"
scholar_txt = "Scholar.txt"

def is_ascii(s):
    try:
        s.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

def extract_ascii_records(in_file):
	out_file = in_file + ".tsv"
	file_handler = open(out_file,"w") 
	records=0
	readable_records=0
	with open(in_file, "rb") as ins:
		for line in ins:
			records += 1
			if (is_ascii(line)):
				readable_records+=1
				line = line.decode('ascii')
				file_handler.write(line)

	print("== Summary (" + in_file + ")==")
	print("total records=" + str(records) + ", ascii records=" + str(readable_records) + \
		", %age ascii=" + str(readable_records/records*100))
	print("ascii records stored in: " + out_file + "\n")
	file_handler.close()
	
extract_ascii_records(dblp_txt)
extract_ascii_records(scholar_txt)