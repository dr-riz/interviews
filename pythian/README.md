# Pythian

Requirement:
Please don't try to make it production ready, as the goal of this assessment is to provide us with an idea of your coding style / thought process rather than a polished production-ready end-result. You are welcomed to use the Internet to support you in building out your own unique solution, however please note that your candidacy will not be considered further if you copy and paste the “solutions” from the many sites that we know exist! Please take the time to showcase your knowledge, skills and abilities to the hiring managers and make your answer your own – we want team members who are excited about solving puzzles and who have a passion for technology.

        "A Linux directory structure contains 100G worth of files. The
        depth and number of sub-directories and files is not known.
         Soft-links and hard-links can also be expected.  Write, in
        the language of your choice, a program that traverses the
        whole structure as fast as possible and reports duplicate
        files. Duplicates are files with same content.

        Be prepared to discuss the strategy that you've taken and its trade-offs."
 

Please note, we expect an implementation of this problem using Python/Java or any other general purpose programming languages. Using existing tools like fdupe is not a proper solution to this challenge.

 

Please provide a quick documentation that briefly summarizes the following:

Design approach [ to as well state the ways how performance optimizations were considered and approached]
Expected Inputs/Outputs
Assumptions and known limitations with the delivered code
Summary on how to run the test client and its pre-requisites


Approach:
- Iterative and agile, namely implement:
(1) quick and dirty first,
(2) and then address each assumption to improve

To this end, I use standard commands where possible and optimize for simplicity.

Assumptions:
- Linux distro with "find" and "cmp" available. 
- soft-link and hard-link are expected but ignored with "find" [2]
- each file is considered a duplicate of itself

Input: the search to search duplicate is set in $SEARCH
Output: list of duplicates in the $SEARCH/duplicate file

SEARCH=.
for file in $(find $SEARCH -type f -links 1); do find $SEARCH -type f -links 1 -exec cmp -s "$file" {} \; -exec echo "duplicate $file" {} \;  ; done > $SEARCH/duplicate

Quick metrics: 
- num_duplicates = number of lines in the duplicate file = wc -l $SEARCH/duplicate
- total number of comparisons = num_duplicates * num_duplicates

Discussion:
- finding duplicates with the above method is an n squared operation, where n is the number of files being compared. This is a brute force method. 
- the performance of "diff -q" and "cmp -s" is comparable [1]
This gives us a list of duplicate files with relative to the $SEARCH path. e.g. "duplicate ./svmTrain.m ./svmTrain.m"

Trade offs:
- "find" is readily available and is general purpose but performs the search on the disk, which is expensive. This is may be mitigated by file system cache.
- A C solution will load and compare the files in memory, yielding in higher performance. It is a custom solution and requires appropriate compilers to be installed.

Optimizations: (future work)
- pick low hanging fruit by determining duplicates on the larger files first, assuming larger duplicates are of greater concern e.g. disk space
- compare the file sizes first before inspecting their contents for duplicates. files cannot be duplicate, if their file sizes are different. This saves us reading their content.
- read file sizes in an n vector or array. then, create a n x n matrix, where cell value is 1 when the file sizes are different otherwise zero. only compare the content of two files if their respective cell is 1.
- in the same spirit, compare if the "file" type are same or different. only compare if their file types are the same. 

References:
*[1] https://unix.stackexchange.com/questions/153286/is-cmp-faster-than-diff-q
*[2] https://stackoverflow.com/questions/16282618/finding-files-that-are-not-hard-links-via-a-shell-script
*[3] https://linux.die.net/man/1/cmp
*[4] https://linux.die.net/man/1/find
 
