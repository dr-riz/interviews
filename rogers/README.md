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
- Two data sets, DBLP1.csv (dblp) and Scholar.csv (scholar)
	- dblp has about 2,600 records
	- scholar has about 64,261 records
- Columns or attributes: title, author, venue, year
- Metadata: id, row_id
- While datasets are suffixed by ".csv", they are not plain text ".csv" files. 
- In addition to attribute values, author names are also separate by comma
- At times, fields are missing e.g. ID, year

Domain Knowledge:
1. A publication with the same exact title and authors cannot be published at two venues in the same year, or any other year for that matter
2. Order of author names matters as it shows the amount of their contribution
3. It is rare to have authors with the same last name with publications with the same title, year and venue.
4. Both short and long versions of venue names are acceptable e.g. VLDB and Very Large Databases. Consequently, two citations using short or long are the same if the other attribute values are same.
5. Titles and authors' last names are not shortened. Only the venue. 
6. With above, I claim that the author names, title and year are usually enough to uniquely identify a publication. 

Approach:
- mvp based
- brute force

### 1st mvp

1. Generate readable records 
	- saving the file as tsv
	- using generateReadableData.py to create readable records 
2. After minimal preprocessing, use "verbatim" text comparison of fields to:
	- match across both data sets
	- detect duplicates and store them in a file for validation

**Results and Discussion:**
Without using any machine learning (ML) libraries, we perform minimal preprocessing: strip preceding and/or trailing white spaces, and lower case title, author and venue.
1. Generating readable records with 2 steps: (i) saving the file as tsv (e.g. DBLP1.txt), and (ii) using python to create ascii records (e.g. DBLP1.txt.tsv). In this process, about 10% data is lost from both datasets. We'll revisit this loss of data in the next iteration. The new number of records for dblp and scholar are about 2,400 and 57,000 respectively. This resets our starting point.
2. The upper bound on number of matches is equal to the size of records in the smaller dataset i.e. dblp. Therefore, it is faster to first match records and then do data deduplication. With this setup, the number of matches are 608 excluding 3 duplicates (DBLP_Scholar_perfectMapping_RizwanMian.csv_dups.tsv), stored in DBLP_Scholar_perfectMapping_RizwanMian.csv as requested. These numbers and matches serve as the baseline for advanced preprocessing and text matching.

Separately, I checked for duplications in both data sets using the script under development. There are about 150 and 20 duplicates in dblp and scholar data sets, respectively.

git tag: first_mvp

### 2nd mvp
3. Advanced preprocessing [1]: remove punctuation, stop words; stem words. Much more can be done.
4. Advanced record matching by ML. Using fuzzy wuzzy [3,4]

**Results and Discussion:**
3. Tabling the improved matching after each preprocessing step

| preprocessing (cumulative)   | matches(#) | duplicates(#) | runtime(m) |
| ---------------------------- | ---------- | ------------- | ---------- | 
| first_mvp (baseline)         | 608   		| 3      		| 1          |
| remove punctuation e.g. "."  | 621   		| 3 			| 1.5 		 |
| remove stop words e.g. is    | 633   		| 3 			| 1.5  		 |
| stem word e.g. fished to fish| 640   		| 3				| 2.5		 | 

This also has the unfortunate consequence of removing i and ii from "...part i" and "...part ii", hence they are treated as the same publication, though they are different publications (fasle match). We also notice that there is a modest increase of matches as we perform advanced preprocessing. It can be argued that the benefits do not warrant the increase in number of matches, and some components of preprocessing (e.g. removing stop words) may be discarded. This is left as future work.

4. After preprocessing title and authors, We use fuzz.ratio on author names (order does matter) and fuzz.token_sort_ratio on title as only keywords remain after stemming. Tabling the increased number of matches when lowering the fuzzy threshold. 

| fuzzy threshold  | matches(#) | duplicates(#) | runtime(m) |
| ---------------- | ---------- | ------------- | ---------- | 
| 100 | 1186 | 3 | 3.02 |
| 90 | 1292 | 6 | 3.23 |
| 80 | 1362 | 7 | 3.34 |
| 70 | 1415 | 14| 3.36 |

As we can see that the number of matches and duplicates increase as we lower the threshold. Most accurate matching happens when the threshold is 100, but we miss some matches (false negatives) e.g.: 
- dblp: Benchmarking Spatial Join Operations with Spatial Output	E Hoel, H Samet	VLDB	1995	40
- scholar: Benchmarking Spatial Join Operations with Spatial Output. 606-618	EG Hoel, H Samet		1995	5473

As we decrease the threshold, we do catch the above but also get wrong matches or false positives. For example, the following two are different citations:
- dblp: XSB as an Efficient Deductive Database Engine	K Sagonas, T Swift, D Warren	SIGMOD Conference	1994	1813
- scholar: XSB as a Deductive Database	K Sagonas, T Swift, D Warren	SIGMOD Conference	1994	1856

We want the most matches but must balance false negatives vs. false positives. The datasets are unlabeled, so it is difficult find out the number of false negative/positives. Next step might be to generate the same citations from both dblp and scholar databases, i.e. a controlled dataset. Then, use the script and different thresholds to measure the number of matches or misses. Business input on the preference of matches or misses is also relevant.

Finally, the de-duplicated matched citations (for threshold =70) are stored in DBLP_Scholar_perfectMapping_RizwanMian.csv.

### Outstanding
- Include lost data sets when generating readable records
- Optimize to run faster
- Use control datasets to measure matches and misses of the script

### References
1. How to Clean Text for Machine Learning with Python: https://machinelearningmastery.com/clean-text-machine-learning-python/
2. Fuzzy String Matching in Python: https://marcobonzanini.com/2015/02/25/fuzzy-string-matching-in-python/
3. When to use which fuzz function to compare 2 strings: https://stackoverflow.com/questions/31806695/when-to-use-which-fuzz-function-to-compare-2-strings

