# thomsonreturs

An architect asked me to write pseudo code to match common words in two arrays.

An architect asked me to write pseudo code to match common words in two arrays.

A non-ML architect asked me, given two arrays of words write pseudo code to give a percent match of common words in two arrays. While the temptation is there to start preprocessing  arrays (e.g. normalizing, stemming etc.), I assumed the arrays have been preprocessed and provided the following pseudo-code

num_words = 0
num_matches = 0

```
for m in array1:
	for n in array2:
		num_words++
		if(m.equals(n))
			num_matches++

percent_match = num_matches / num_words * 100
```
