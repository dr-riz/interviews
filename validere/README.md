# Validere

Requirement:
Design and implement a "least recently used" cache, which evicts the least recently used item. The cache should map from keys to values and be initialized with a max size. When it is full, it should evict the least recently used item. Please provide test cases.

Implementation:
Method used from [1]. Took the approach of path of least resistance and optimized code for simplicity and conciseness. All test cases are mine.

Assumptions:
- tests must run in the order I specified
- tests assume the cache size to be 3, the cache can be defined of any size

Outstanding:
- tests using junit
- packaging and jar file

References:
1. https://stackoverflow.com/questions/6398902/best-way-to-implement-lru-cache
2. https://www.javatpoint.com/java-linkedhashmap