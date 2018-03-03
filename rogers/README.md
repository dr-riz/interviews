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
- 

### 1st mvp

- simple record matching across both data with "verbatim" text comparison of fields
- printing a summary

1. generate readable records
2. use "verbatim" text comparison of fields to:
a. detect duplicates and store them in a file for validation
b. match across both data sets

### 2nd mvp
3. advance record matching using employ machine learning methods

Assumptions:
- ID is unique
- missing ID citation is not checked for duplication 

only around 20 duplicates in tens of thoudsands of citations. disabling duplicate detection for scholar.

### Challenges
unknown charset
Rizwans-MacBook-Pro:rogers rmian$ file -I DBLP1.csv 
DBLP1.csv: text/plain; charset=unknown-8bit

author names are also separate by comma

There is more than 1 way to slice a bread i.e. entity resolution is possible with different methods:


Scope
- 

Comments:
- dblp has about 2,600 records
- scholar has about 64,261 records


Methods
- changed line ending to mac local
- scope of matching to the title only


Questions:
- how to deal with special characters?

### References
1. How to Clean Text for Machine Learning with Python: https://machinelearningmastery.com/clean-text-machine-learning-python/
