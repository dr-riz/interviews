/* analyze.pig

Rizwans-MacBook-Pro:data rmian$ pig --version
Apache Pig version 0.15.0 (r1682971) 
compiled Jun 01 2015, 11:43:55

Using pig -x local

External libs: DataFu

*/

register /Users/rmian/Documents/jobs/interviews/paytm/WeblogChallenge-master/data/datafu-pig-incubating-1.3.3.jar

weblog = load 'random_10_examples.log' using PigStorage(' ') as (date_time:datetime, elb,	client_port, backend_port, request_processing_time, backend_processing_time, response_processing_time, elb_status_code, backend_status_code, received_bytes, sent_bytes, request, url, user_agent, ssl_cipher, ssl_protocol);

/* 

Processing & Analytical goals:

"1. Sessionize the web log by IP. Sessionize = aggregrate all page hits by visitor/IP during a fixed time window. https://en.wikipedia.org/wiki/Session_(web_analytics)"

Assumptions:
- fixed time window or session length = 10m
- page hits include both Get and Post requests
- paga hits aka page counts

*/

DEFINE Sessionize datafu.pig.sessions.Sessionize('10m'); 
DEFINE Median datafu.pig.stats.StreamingMedian();
DEFINE Quantile datafu.pig.stats.StreamingQuantile('0.9','0.95');
DEFINE VAR datafu.pig.VAR();

-- selected = FOREACH weblog GENERATE ToUnixTime(date_time) as timestamp, REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as visitor_ip, request, url;  

pv = FOREACH weblog GENERATE ToUnixTime(date_time) as time, REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as memberId, request, url; 

pv_sessionized = FOREACH (GROUP pv BY memberId) {
  ordered = ORDER pv BY time;
  GENERATE FLATTEN(Sessionize(ordered))
           AS (time,memberId,request, url, sessionId);
}

dump pv_sessionized; -- remove after development
-- pv_sessionized <== part 1: sessionized web data

/* to be deleted
	GENERATE

group_by_ip = group selected by visitor_ip; -- <== required sessions for part 1

-- bonus :-)
page_count = FOREACH group_by_ip GENERATE group, COUNT(selected.visitor_ip) as page_hits;
ordered_page_count = ORDER page_count BY page_hits; -- order by hit count for validation
*/

/* 

2. Determine the average session time

Assumptions: 
- a session of a single ip = all page hits during a fixed time window

todo:
- confirm ToUnixTime returns seconds or milliseconds
- confirm 

*/

session_times =
  FOREACH (GROUP pv_sessionized BY (sessionId,memberId)) {
    GENERATE group.sessionId as sessionId,
             group.memberId as memberId,
             (MAX(pv_sessionized.time) - MIN(pv_sessionized.time))
               / 1000.0 / 60.0 as session_length;
}

all_group = group session_times all;

avg_session_len = foreach all_group generate AVG(session_times.session_length) as avg_session_duration;

dump avg_session_len; -- <== part 2: average session length

/* to be deleted

min_max_times = FOREACH group_by_ip GENERATE group, MIN(selected.timestamp) as earliest_time, MAX(selected.timestamp) as latest_time;

delta_times = FOREACH min_max_times GENERATE group, MinutesBetween(latest_time,earliest_time) as delta_mins;

all_group = group delta_times all;

avg_session_len = foreach all_group generate AVG(delta_times.delta_mins) as avg_session_duration;

dump avg_session_len; -- <== answer to part 2

*/
/*

3. Determine unique URL visits per session. To clarify, count a hit to a unique URL only once per session.

*/

grouppv_by_session = group pv_sessionized by sessionId;
url_visits = FOREACH grouppv_by_session {
	unique_urls = DISTINCT pv_sessionized.url;
	GENERATE group, COUNT(unique_urls) as page_hits;
}

ordered_url_visits = ORDER url_visits BY page_hits; -- <== part 3: (ordered) unique URL visits per session

/*

4. Find the most engaged users, ie the IPs with the longest session times

Assumptions:
- i

*/

most_engaged_users = ORDER session_times by session_length; -- <== part 4: sessionid, ips with the longest session length

session_times =
  FOREACH (GROUP pv_sessionized BY (sessionId,memberId)) {
    GENERATE group.sessionId as sessionId,
             group.memberId as memberId,
             (MAX(pv_sessionized.time) - MIN(pv_sessionized.time))
               / 1000.0 / 60.0 as session_length; -- why dividing by 1000. it's already in seconds?
}

group_by_session = group session_times by sessionId;



all_group = group session_times all;

avg_session_len = foreach all_group generate AVG(session_times.session_length) as avg_session_duration;



delta_times = FOREACH min_max_times GENERATE group, MinutesBetween(latest_time,earliest_time) as delta_mins;

most_engaged_users = ORDER delta_times by delta_mins; -- <== answer to part 4

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

<-- not done yet