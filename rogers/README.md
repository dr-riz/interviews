# Rogers

## Problem Description

“Entity resolution” is the problem of identifying which records in a database represent the same entity. When dealing with user data, it is often difficult to control the quality of the data inputted into the system. The poor quality of the data may be characterized by:
- Duplicated records
- Records that link to the same entity across different data sources
- Data fields with more than one possible representation (e.g. “P&G” and “Procter
and Gamble”)
In this assignment, you are provided with two datasets:
1. Scholar.csv
2. DBLP .csv
Each dataset contains the following columns:

| Id[.csvName] | title | author | venue | year | ROW_ID |
| ------------ | ----- | ------ | ------| ---- | ------ |

There are records that reference the same entity across the two datasets.

## Bringing Everything Together

Your assignment is to resolve the records to their respective entities, and write a final .csv named “DBLP_Scholar_perfectMapping_[YourName].csv” that only contain the resolved entities. The final .csv file should include the following column headings:

idDBLP: The matched DBLP.csv id
idScholar: The matched Scholar.csv id
DBLP_Match: The ROW_ID of the DBLP.csv file
Scholar_Match: The ROW_ID of the Scholar.csv file
Match_ID: A final column that combines the number from DBLP_Match and Scholar_Match, separated by an underscore.
The first row is provided as an example:

| idDBLP | idScholar | DBLP_Match | Scholar_Match | Match_ID | 
| --------- | -------- | ----------- | --------| ------ |
| conf/vldb/Levy96 | lDTPyBMtHVwJ | 1996 | 14 | 1996_14 |

Emphasis will be placed on the method and logic used in resolving the entities, rather than on the final result.

Asks:
- Your assignment is to resolve the records to their respective entities. A simple consolidation on text matching.

## Solution

Initial assessment: 
- dblp has about 2,600 records
- scholar has about 64,261 records
- attributes: title, author, venue, year
- metadata: id, row_id
- While datasets are suffixed by ".csv", they are not plain text ".csv" files. 
- In addition to columns, author names are also separate by comma
- At times, fields are missing e.g. ID, year

Domain Knowledge:
- a publication with the same exact title and authors cannot be published at two venues in the same year, or any other year for that matter
- order of author names matters as it shows the amount of their contribution
- it is rare to have authors with the same last name with publications with the same title, year and venue
- both short and long version of venue names are acceptable e.g. VLDB and Very Large Databases. Consequently, two citations using short or long are the same if the other attribute values are same.
- titles and authors' last names are not shortened. Only the venue
- With above, I claim that author names, title and year are usually enough to uniquely identify a publication

Approach:
- mvp based
- brute force

### 1st mvp

1. generate readable records 
	- saving the file as tsv
	- using generateReadableData.py to create readable records 
2. After minimal preprocessing, use "verbatim" text comparison of fields to:
	- match across both data sets
	- detect duplicates and store them in a file for validation

Results and Discussion:
We perform minimal preprocessing without using ML libraries, namely trailing white spaces and lower casing title, author and venue.
1. generating readable records with 2 steps: (i) saving the file as tsv (e.g. DBLP1.txt), and (ii) using python to create ascii records (e.g. DBLP1.txt.tsv). In this process, about 10% data is lost from both datasets. We'll revisit this loss of data in the next iteration. The new number of records for DBLP and Scholar are about 2,400 and 57,000 respectively. This resets our starting point.
2. The upper bound on number of matches is equal to the size of records in the smaller data set i.e. DBLP. Therefore, it is faster to first match records and then do data duplication. With this setup, the number of matches are 608 after removing 3 duplications (DBLP_Scholar_perfectMapping_RizwanMian.csv_dups.tsv), stored in DBLP_Scholar_perfectMapping_RizwanMian.csv as requested. These numbers and matches serve as the baseline for advanced preprocessing and text matching.

Separately, I checked for duplications in both data sets using the script under development. There are about 150 and 20 duplicates in dblp and scholar data sets, respectively.

git tag: first_mvp

### 2nd mvp
3. advanced preprocessing [1]: remove punctuation, stop words; stem words. Much more can be done.
4. advanced record matching using employ machine learning methods. Use fuzzy wuzzy [3,4]
	- fuzzywuzzy

Results and Discussion:
3. Tabling the improved matching after each preprocessing step

| preprocessing (cumulative)   | matches(#) | duplicates(#) | runtime(m) |
| ---------------------------- | ---------- | ------------- | ---------- | 
| first_mvp (baseline)         | 608   		| 3      		| 1          |
| remove punctuation e.g. "."  | 621   		| 3 			| 1.5 		 |
| remove stop words e.g. is    | 633   		| 3 			| 1.5  		 |
| sten word e.g. fished to fish| 640   		| 3				| 2.5		 | 

4. After preprocessing title and authors, using fuzz.ratio on author names (order does matter) and fuzz.token_sort_ratio on title as only keyword remain after stemming.
	- fuzzy_threshold = 100
	
	It is business decision to choose the fuzzy_threshold. 


### Challenges

Scope
- 

Methods
- changed line ending to mac local

### Outstanding
- include lost data sets when generating readable records
- optimize to run faster


### References
1. How to Clean Text for Machine Learning with Python: https://machinelearningmastery.com/clean-text-machine-learning-python/
2. Fuzzy String Matching in Python: https://marcobonzanini.com/2015/02/25/fuzzy-string-matching-in-python/
3. When to use which fuzz function to compare 2 strings: https://stackoverflow.com/questions/31806695/when-to-use-which-fuzz-function-to-compare-2-strings

