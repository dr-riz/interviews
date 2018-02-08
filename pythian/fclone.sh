#!/bin/bash

for file in $(find $SEARCH -type f -links 1); 
	do find $SEARCH -type f -links 1 -exec cmp -s "$file" {} \; -exec echo "duplicate $file" {} \;  ; 
done > ./duplicate

