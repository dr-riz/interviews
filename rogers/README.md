# Rogers

**Problem description and instructions are in Entity_Resolution.pdf**

Asks in a nutshell: 
- match the citations in both datasets
- deduplicate redundant matches
- address more than one possible representation e.g. VLDB and Very Large Databases represent the same venue

## Solution

Initial assessment: 
- Two data sets, DBLP1.csv (or dblp) and Scholar.csv (or scholar)
	- dblp has about 2,600 records
	- scholar has about 64,261 records
- Columns or attributes: title, author, venue, year
- Metadata: id, row_id
- While datasets are suffixed by ".csv", they are not plain text ".csv" files. 
- In addition to attribute values, author names are also separate by comma
- At times, attribute values are missing values e.g. ID, year
- At times, url is provided in place of citation id. We perform no checking on citation id and use it verbatim in output.csv

Our Domain Knowledge:
1. A publication with the same exact title and authors cannot be published at two venues in the same year, or any other year for that matter
2. Order of author names matters as it shows the amount of their contribution
3. It is rare to have authors with the same last name with publications with the same title, year and venue.
4. Both short and long versions of venue names are acceptable e.g. VLDB and Very Large Databases. Consequently, two citations using short or long are the same if the other attribute values are same.
5. Titles and authors' last names are not shortened. Only the venue. 
6. With the above, we claim that the author names, title and year are usually enough to uniquely identify a publication. With this assertion, we defer the resolution of long and short venue names.

Our Approach:
- mvp based
- brute force

### 1st mvp

1. Generate readable records 
	- saving the file as tsv
	- using generateReadableData.py to create readable records 
2. After minimal preprocessing, use "verbatim" text comparison of fields to:
	- match citation across both data sets
	- detect duplicates and store them in a file for validation

**Results and Discussion:**
Without using any machine learning (ML) libraries, we perform minimal preprocessing: strip preceding and/or trailing white spaces, and lower case title, author and venue.
1. Generating readable records with 2 steps: (i) saving the file as tsv (e.g. DBLP1.txt), and (ii) using python to create text or ascii records (e.g. DBLP1.txt.tsv). In this process, about 10% data is lost from both datasets. We'll revisit this loss of data in the next iteration. The new number of records for dblp and scholar are about 2,400 and 57,000 respectively. This resets our starting point.
2. The upper bound on number of matches is equal to the size of records in the smaller dataset i.e. dblp. Therefore, it is faster to first match records and then do data deduplication. With this setup, the number of matches are 608 excluding 3 duplicates, stored in DBLP_Scholar_perfectMapping_RizwanMian.csv as requested. These numbers and matches serve as the baseline for advanced preprocessing and text matching.

Separately, I checked for duplications within both datasets using the script under development. There are about 150 and 20 duplicates in dblp and scholar data sets, respectively.

git tag: first_mvp

### 2nd mvp
3. Advanced preprocessing [1]: remove punctuation, stop words; stem words. Much more can be done.
4. Advanced record matching with ML. Using fuzzy wuzzy [3,4]

**Results and Discussion:**

3. We table the improved matching after each preprocessing step

| preprocessing (cumulative)   | matches(#) | duplicates(#) | runtime(m) |
| ---------------------------- | ---------- | ------------- | ---------- | 
| first_mvp (baseline)         | 608   		| 3      		| 1          |
| remove punctuation e.g. "."  | 621   		| 3 			| 1.5 		 |
| remove stop words e.g. is    | 633   		| 3 			| 1.5  		 |
| stem word e.g. fished to fish| 640   		| 3				| 2.5		 | 

This also has the unfortunate consequence of removing i and ii from "...part i" and "...part ii", hence they are treated as the same publication, though they are not (fasle match). We also notice that there is a modest increase of matches as we perform advanced preprocessing. It can be argued that the benefits do not warrant the increase in number of matches, and some components of preprocessing (e.g. removing stop words) may be discarded. This is left as future work.

4. After preprocessing title and authors, We use fuzz.ratio on author names (order does matter) and fuzz.token_sort_ratio on title as only keywords remain after stemming. We table the increased number of matches when lowering the fuzzy threshold (also stored in stats.csv).

| fuzzy threshold  | matches(#) | duplicates(#) | runtime(m) |
| ---------------- | ---------- | ------------- | ---------- | 
| 100 | 1186 | 3 | 3.02 |
| 90 | 1292 | 6 | 3.23 |
| 80 | 1362 | 7 | 3.34 |
| 70 | 1415 | 14| 3.36 |

For inspection, fully qualified matches with preprocessed text are stored in matched.tsv. As we can see that the number of matches and duplicates increase as we lower the threshold. Most accurate matching happens when the threshold is 100, but we miss some matches (false negatives) e.g.: 
- dblp: Benchmarking Spatial Join Operations with Spatial Output	E Hoel, H Samet	VLDB	1995	40
- scholar: Benchmarking Spatial Join Operations with Spatial Output. 606-618	EG Hoel, H Samet		1995	5473

For inspection, duplicates for each threshold are stored in duplicates.tsv. As we decrease the threshold, we do catch the above but also get wrong matches or false positives. For example, the following two are different citations:
- dblp: XSB as an Efficient Deductive Database Engine	K Sagonas, T Swift, D Warren	SIGMOD Conference	1994	1813
- scholar: XSB as a Deductive Database	K Sagonas, T Swift, D Warren	SIGMOD Conference	1994	1856

We want the most matches but must balance false negatives vs. false positives. The datasets are unlabeled, so it is difficult find out the number of false negative/positives. Next step might be to generate the same citations from both dblp and scholar databases, i.e. a controlled dataset. Then, use the script and different thresholds to measure the number of matches or misses. Business input on the preference of matches or misses is also relevant.

Finally, the de-duplicated matched citations (for threshold =70) are stored in DBLP_Scholar_perfectMapping_RizwanMian.csv. The name template is suggested by the instructions. As we demonstrate above, there are tradeoffs and hence our mapping is less than perfect.

git tag: second_mvp

### Future Work
- Include lost data sets when generating readable records
- Use control datasets to measure matches and misses of the script
- Catch more than one representation VLDB and Very Large Databases
- Optimize code for improved readability and performance

### References
1. How to Clean Text for Machine Learning with Python: https://machinelearningmastery.com/clean-text-machine-learning-python/
2. Fuzzy String Matching in Python: https://marcobonzanini.com/2015/02/25/fuzzy-string-matching-in-python/
3. When to use which fuzz function to compare 2 strings: https://stackoverflow.com/questions/31806695/when-to-use-which-fuzz-function-to-compare-2-strings

