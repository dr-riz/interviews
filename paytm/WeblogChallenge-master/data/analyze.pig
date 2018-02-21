/* analyze.pig

Rizwans-MacBook-Pro:data rmian$ pig --version
Apache Pig version 0.15.0 (r1682971) 
compiled Jun 01 2015, 11:43:55

My script includes three simple Pig Latin Statements.

legend:
- unknown variables are prefixed by 'x#'
*/


register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/hadoop-core-1.0.4.jar
register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/commons-cli-1.2.jar
register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/commons-io-2.3.jar
register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/commons-logging-1.1.1.jar

weblog = load 'random_100_examples.log' using PigStorage(' ') as (date_time:datetime, app,	visitor, local,	x1, x2,	x3,	x4,	x5,	x6,	x7,	request, url, brower_os, x8, tls);


/* 

Processing & Analytical goals:

1. Sessionize the web log by IP. Sessionize = aggregrate all page hits by visitor/IP during a fixed time window. https://en.wikipedia.org/wiki/Session_(web_analytics)

Assumptions:
- time period is from 9 to 10
- page hits include both Get and Post requests
- granularity required is till second, so ignoring milli seconds

todo: 
- filter by time
- calculate the time span of logs based on time only

lower_bound = ToDate('2015-07-22T11:02:43', 'yyyy-MM-ddTHH:mm:ss');

time_log = FILTER weblog BY date_time < '2015-07-22T05';

*/

selected = FOREACH weblog GENERATE date_time, REGEX_EXTRACT(visitor, '(.*):(.*)', 1) as visitor_ip, request, url;  

selected = FOREACH weblog GENERATE date_time, REGEX_EXTRACT(visitor, '(.*):(.*)', 1) as visitor_ip;  

sessions = group selected by visitor_ip; -- <== required sessions for part 1

page_count = FOREACH sessions GENERATE group, COUNT(selected.visitor_ip) as page_hits;
ordered_page_count = ORDER C BY page_hits;

dump D

/* 

2. Determine the average session time

*/





DUMP selected; 





sessionize = 

selected = FOREACH weblog GENERATE date_time, visitor, url;  
DUMP selected; 



tokenized = FOREACH weblog GENERATE REGEX_EXTRACT(visitor, '(.*):(.*)', 1) as visitor_ip; 
DUMP tokenized;

tokenized = FOREACH weblog GENERATE REGEX_EXTRACT(date_time, 'T(.*)\.(.*)', 1) as time; 
DUMP tokenized;

tokenized = FOREACH weblog GENERATE REGEX_EXTRACT(date_time, 'T(.*)\.(.*)', 1) as time; 
DUMP tokenized;
  

split

B = GROUP weblog BY ;





drivers = LOAD 'drivers.csv' USING PigStorage(',');




nasdaqdaily = load ‘nasdaq_daily.gz’ using PigStorage(‘,’) as (exchange,stocke,date,open,high,low,close,volume,adjusted_close);

