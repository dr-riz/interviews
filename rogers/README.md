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
- While datasets are suffixed by ".csv", they are not plain text ".csv" files. 
- In addition to columns, author names are also separate by comma
- At times, fields are missing e.g. ID, year

### 1st mvp

1. generate readable records 
a. saving the file as tsv
b. using generateReadableData.py to create readable records 
2. After minimal preprocessing, use "verbatim" text comparison of fields to:
a. match across both data sets
b. detect duplicates and store them in a file for validation

Results and Discussion:
We perform minimal preprocessing without using ML libraries, namely trailing white spaces and lower casing title, author and venue.
1. generating readable records with 2 steps: (i) saving the file as tsv (e.g. DBLP1.txt), and (ii) using python to create ascii records (e.g. DBLP1.txt.tsv). In this process, about 10% data is lost from both datasets. We'll revisit this loss of data in the next iteration. The new number of records for DBLP and Scholar are about 2,400 and 57,000 respectively. This resets our starting point.
2. The upper bound on number of matches is equal to the size of records in the smaller data set i.e. DBLP. Therefore, it is faster to first match records and then do data duplication. With this setup, the number of matches are 608 after removing 3 duplications (DBLP_Scholar_perfectMapping_RizwanMian.csv_dups.tsv), stored in DBLP_Scholar_perfectMapping_RizwanMian.csv as requested. These numbers and matches serve as the baseline for advanced preprocessing and text matching.

Separately, I checked for duplications in both data sets. There are about 150 and 20 duplicates in dblp and scholar data sets, respectively.

git tag: first_mvp

### 2nd mvp
3. advanced preprocessing:
a. recall baseline: 608 matches + 3 dups
b. remove punctuation e.g. ".": 621 matches + 3 dups
c. remove stop words e.g. is, and: 633 matches + 3 dups
d. stemming, removing stop words, 
 
4. advanced record matching using employ machine learning methods

### Challenges

Scope
- 

Methods
- changed line ending to mac local

### Outstanding
- include lost data sets when generating readable records


### References
1. How to Clean Text for Machine Learning with Python: https://machinelearningmastery.com/clean-text-machine-learning-python/
