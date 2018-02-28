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

### Challenges
unknown charset
Rizwans-MacBook-Pro:rogers rmian$ file -I DBLP1.csv 
DBLP1.csv: text/plain; charset=unknown-8bit

author names are also separate by comma

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


