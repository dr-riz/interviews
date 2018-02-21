/* analyze.pig
My script includes three simple Pig Latin Statements.

legend:
- unknown variables are prefixed by 'x#'
*/


weblog = load 'random_10_examples.log' using PigStorage(' ') as (date_time:datetime, app,	visitor, local,	x1, x2,	x3,	x4,	x5,	x6,	x7,	request, url, brower_os, x8, tls);

selected = FOREACH weblog GENERATE date_time, REGEX_EXTRACT(visitor, '(.*):(.*)', 1) as visitor_ip, request, url;  

selected = FOREACH weblog GENERATE date_time, REGEX_EXTRACT(visitor, '(.*):(.*)', 1) as visitor_ip;  

sessionize = group selected by visitor_ip;

dump sessionize;

C = FOREACH sessionize GENERATE group, COUNT(selected.visitor_ip) as page_hits;
D = ORDER C BY mycount;

dump D

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



/* 

Processing & Analytical goals:

1. Sessionize the web log by IP. Sessionize = aggregrate all page hits by visitor/IP during a fixed time window. https://en.wikipedia.org/wiki/Session_(web_analytics)

Assumptions:
- granularity required is till second, so ignoring milli seconds

todo: 
- calculate the time span of logs based on time only

*/



drivers = LOAD 'drivers.csv' USING PigStorage(',');




nasdaqdaily = load ‘nasdaq_daily.gz’ using PigStorage(‘,’) as (exchange,stocke,date,open,high,low,close,volume,adjusted_close);

