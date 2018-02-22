/* analyze.pig

Rizwans-MacBook-Pro:data rmian$ pig --version
Apache Pig version 0.15.0 (r1682971) 
compiled Jun 01 2015, 11:43:55

*/

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

time_log = FILTER weblog BY timestamp < timestamp + 15m;

*/

selected = FOREACH weblog GENERATE timestamp, REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as visitor_ip, request, url;  

group_by_ip = group selected by visitor_ip; -- <== required sessions for part 1

-- bonus :-)
page_count = FOREACH group_by_ip GENERATE group, COUNT(selected.visitor_ip) as page_hits;
ordered_page_count = ORDER page_count BY page_hits; -- order by hit count for validation

/* 

2. Determine the average session time

Assumptions: 
- a session of a single ip = all page hits during a fixed time window
*/

min_max_times = FOREACH group_by_ip GENERATE group, MIN(selected.timestamp) as earliest_time, MAX(selected.timestamp) as latest_time;

delta_times = FOREACH min_max_times GENERATE group, MinutesBetween(latest_time,earliest_time) as delta_mins;

all_group = group delta_times all;

-- session_count = foreach all_group generate count(delta_times);

-- session_count = FOREACH (GROUP delta_times ALL) GENERATE COUNT(delta_times);

-- session_len = foreach all_group generate (delta_times.group,delta_times.delta_mins),SUM(delta_times.delta_mins);

-- session_len = foreach all_group generate (delta_times.group,delta_times.delta_mins),AVG(delta_times.delta_mins) as avg_session_duration;

session_len = foreach all_group generate AVG(delta_times.delta_mins) as avg_session_duration;


/*

3. Determine unique URL visits per session. To clarify, count a hit to a unique URL only once per session.

Assumptions: 
- session length includes the entire duration of the log

*/

group_by_url = group selected by url;
url_visits = FOREACH group_by_url GENERATE group, COUNT(selected.url) as page_hits;
ordered_url_visits = ORDER url_visits BY page_hits;

/*

4. Find the most engaged users, ie the IPs with the longest session times

Assumptions:
- 

*/

delta_times = FOREACH min_max_times GENERATE group, MinutesBetween(latest_time,earliest_time) as delta_mins;

most_engaged_users = ORDER delta_times by delta_mins;

/*

Additional questions for Machine Learning Engineer (MLE) candidates:

1. Predict the expected load (requests/second) in the next minute

Assumptions:
- the log is in the ascending order of timestamps. By eye balling, the log is loosely follows this assumption.
- each record in the log represents a request

method: simple time series or running average. average the number of transactions in last some minutes, say 5m, to estimate load next minute

*/

predlog = load 'web_log.csv' using PigStorage(' ') as (timestamp:datetime, elb,	client_port, backend_port, request_processing_time, backend_processing_time, response_processing_time, elb_status_code, backend_status_code, received_bytes, sent_bytes, request, url, user_agent, ssl_cipher, ssl_protocol);

selected = FOREACH weblog GENERATE timestamp, REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as visitor_ip, request, url; 