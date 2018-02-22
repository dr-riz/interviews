/* analyze.pig

Rizwans-MacBook-Pro:data rmian$ pig --version
Apache Pig version 0.15.0 (r1682971) 
compiled Jun 01 2015, 11:43:55



legend:
- unknown variables are prefixed by 'x#'



register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/hadoop-core-1.0.4.jar
register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/commons-cli-1.2.jar
register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/commons-io-2.3.jar
register /usr/local/Cellar/pig/0.15.0/libexec/lib/hadoop1-runtime/commons-logging-1.1.1.jar
register /usr/local/Cellar/pig/0.15.0/libexec/pig-0.15.0-core-h1.jar
register /usr/local/Cellar/pig/0.15.0/libexec/pig-0.15.0-core-h2.jar

*/

weblog = load 'random_10_examples.log' using PigStorage(' ') as (timestamp:datetime, app,	client_port, local,	x1, x2,	x3,	x4,	x5,	x6,	x7,	request, url, brower_os, x8, tls);

weblog = load 'random_10_examples.log' using PigStorage(' ') as (timestamp:datetime, elb,	client_port, backend_port, request_processing_time, backend_processing_time, response_processing_time, elb_status_code, backend_status_code, received_bytes, sent_bytes, request, url, user_agent, ssl_cipher, ssl_protocol);

/* 

Processing & Analytical goals:

"1. Sessionize the web log by IP. Sessionize = aggregrate all page hits by visitor/IP during a fixed time window. https://en.wikipedia.org/wiki/Session_(web_analytics)"

Assumptions:
- time period is from 9 to 10
- page hits include both Get and Post requests
- paga hits aka page counts
- granularity required is till second, so ignoring milli seconds

todo: 
- filter by time
- calculate the time span of logs based on time only

lower_bound = ToDate('2015-07-22', 'yyyy-MM-dd');

time_log = FILTER weblog BY timestamp < '2015-07-22T05';

*/

time_log = FILTER weblog BY timestamp < timestamp + 15m;


selected = FOREACH weblog GENERATE timestamp, REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as visitor_ip, request, url;  

group_by_ip = group selected by visitor_ip; -- <== required sessions for part 1

-- bonus :-)
page_count = FOREACH group_by_ip GENERATE group, COUNT(selected.visitor_ip) as page_hits;
ordered_page_count = ORDER page_count BY page_hits;

/* 

2. Determine the average session time

Assumptions: 
- a session of a single ip = all page hits during a fixed time window
*/

min_max_times = FOREACH group_by_ip GENERATE group, MIN(selected.timestamp) as earliest_time, MAX(selected.timestamp) as latest_time;

delta_times = FOREACH min_max_times GENERATE group, MinutesBetween(latest_time,earliest_time) as delta_mins;

all_group = group delta_times all;

session_count = foreach all_group generate count(delta_times);

session_count = FOREACH (GROUP delta_times ALL) GENERATE COUNT(delta_times);

session_len = foreach all_group generate (delta_times.group,delta_times.delta_mins),SUM(delta_times.delta_mins);

session_len = foreach all_group generate (delta_times.group,delta_times.delta_mins),AVG(delta_times.delta_mins) as avg_session_duration;

avg_session_duration = FOREACH (GROUP delta_times ALL) GENERATE group, SUM(delta_mins);


delta_times.group, delta_times.delta_mins, avg(delta_times.delta_mins); 

avg_session_time = FOREACH delta_times generate count(group), sum(delta_mins);
   (employee_data.name,employee_data.daily_typing_pages),SUM(employee_data.daily_typing_pages);








delta_times = foreach min_max_times GENERATE group, MinutesBetween(min_max_times.latest_time, min_max_times.earliest_time);


times = foreach group_by_ip GENERATE group, MAX(group_by_ip.timestamp) as latest_time, MIN(group_by_ip.timestamp) as earliest_time;

 FOREACH sessions GENERATE group, avg(selected.timestamp) as avg_time;


avg_session_time = FOREACH sessions GENERATE group, avg(selected.timestamp) as avg_time;
ordered_page_count = ORDER avg_session_time BY avg_time;
DUMP selected; 


date_data = LOAD 'date.txt' USING PigStorage(',') as (id:int,date:chararray);
todate_data = foreach date_data generate ToDate(date,'yyyy/MM/dd HH:mm:ss') as (timestamp:DateTime);


b = FILTER a BY date < ToDate('2013-01-01');

start_time='1989/09/26 09:00:00';
mydate = ToDate('1989/09/26 09:00:00', 'yyyy/MM/dd HH:mm:ss');

sessionize = 

selected = FOREACH weblog GENERATE timestamp, client_port, url;  
DUMP selected; 



tokenized = FOREACH weblog GENERATE REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as visitor_ip; 
DUMP tokenized;

tokenized = FOREACH weblog GENERATE REGEX_EXTRACT(timestamp, 'T(.*)\.(.*)', 1) as time; 
DUMP tokenized;

tokenized = FOREACH weblog GENERATE REGEX_EXTRACT(timestamp, 'T(.*)\.(.*)', 1) as time; 
DUMP tokenized;
  

split

B = GROUP weblog BY ;





drivers = LOAD 'drivers.csv' USING PigStorage(',');




nasdaqdaily = load ‘nasdaq_daily.gz’ using PigStorage(‘,’) as (exchange,stocke,date,open,high,low,close,volume,adjusted_close);

