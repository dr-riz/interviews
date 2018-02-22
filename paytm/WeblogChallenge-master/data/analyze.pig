/* analyze.pig

Rizwans-MacBook-Pro:data rmian$ pig --version
Apache Pig version 0.15.0 (r1682971) 
compiled Jun 01 2015, 11:43:55

Using pig -x local

External libs: DataFu

*/

register /Users/rmian/Documents/jobs/interviews/paytm/WeblogChallenge-master/data/datafu-pig-incubating-1.3.3.jar

weblog = load 'web_log.csv' using PigStorage(' ') as (date_time:datetime, elb,	client_port, backend_port, request_processing_time, backend_processing_time, response_processing_time, elb_status_code, backend_status_code, received_bytes, sent_bytes, request, url, user_agent, ssl_cipher, ssl_protocol);

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
DEFINE VAR datafu.pig.stats.VAR();

pv = FOREACH weblog GENERATE ToUnixTime(date_time) as time, REGEX_EXTRACT(client_port, '(.*):(.*)', 1) as memberId, request, url; 

pv_sessionized = FOREACH (GROUP pv BY memberId) {
  ordered = ORDER pv BY time;
  GENERATE FLATTEN(Sessionize(ordered))
           AS (time,memberId,request, url, sessionId);
}

L = LIMIT pv_sessionized 3; <== part 1: sessionized web data

dump L; -- remove after development

/* 

2. Determine the average session time

Assumptions: 
- a session of a single ip = all page hits during a fixed time window

*/

session_times =
  FOREACH (GROUP pv_sessionized BY (sessionId,memberId)) {
    GENERATE group.sessionId as sessionId,
             group.memberId as memberId,
             (MAX(pv_sessionized.time) - MIN(pv_sessionized.time))
               / 60.0 as session_length;
}

all_group = group session_times all;

avg_session_len = foreach all_group generate AVG(session_times.session_length) as avg_session_duration;

dump avg_session_len; -- <== part 2: average session length

/*

3. Determine unique URL visits per session. To clarify, count a hit to a unique URL only once per session.

*/

group_by_session = group pv_sessionized by sessionId;
url_visits = FOREACH group_by_session {
	unique_urls = DISTINCT pv_sessionized.url;
	GENERATE group, COUNT(unique_urls) as page_hits;
}

ordered_url_visits = ORDER url_visits BY page_hits; -- <== part 3: (ordered) unique URL visits per session

/*

4. Find the most engaged users, ie the IPs with the longest session times

*/

session_stats = FOREACH (GROUP session_times ALL) {
  GENERATE
    AVG(session_times.session_length) as avg_session,
    SQRT(VAR(session_times.session_length)) as std_dev_session,
    Median(session_times.session_length) as median_session,
    Quantile(session_times.session_length) as quantile_session;
}

long_sessions = FILTER session_times BY
  session_length > session_stats.quantiles_session.quantile_0_95;
  
most_engaged_users = DISTINCT (FOREACH long_sessions GENERATE memberId, session_length);
DUMP most_engaged_users; -- <== part 4: ips with the longest session length

/*

Additional questions for Machine Learning Engineer (MLE) candidates:

1. Predict the expected load (requests/second) in the next minute

Assumptions:
- the log is in the ascending order of timestamps. By eye balling, the log is loosely follows this assumption.
- each record in the log represents a request

method: simple time series or running average. average the number of transactions in last some minutes, say 5m, to estimate load next minute

*/

all_group = group pv all;
max_timestamp = foreach all_group generate MAX(pv.time) as max_time;

last_m_samples = FILTER pv BY time > (max_timestamp.max_time/60 - 5); -- convert to min and subtract 5m

last_m_samples_all = Group last_m_samples All;
rate = foreach last_m_samples_all  Generate COUNT(last_m_samples.request) as num_requests;
prediction = FOREACH rate GENERATE num_requests/5.0*60.0 as requests_per_second:double;
dump prediction; -- <== part 1: MLE predict the expected load (requests/second) 

/*

2. Predict the session length for a given IP

Assumptions:
- frequency distribution of session lengths is normal-like

*/

dump session_stats;
predicted_session_length = FOREACH session_stats GENERATE avg_session, std_dev_session


/*

3. Predict the number of unique URL visits by a given IP [not bound to a session]

Assumptions:
- frequency distribution of session lengths is normal-like

*/

session_stats = FOREACH (GROUP session_times ALL) {
  GENERATE
    AVG(session_times.session_length) as avg_session,
    SQRT(VAR(session_times.session_length)) as std_dev_session,
    Median(session_times.session_length) as median_session,
    Quantile(session_times.session_length) as quantile_session;
}


group_by_session = group pv_sessionized by sessionId;
url_visits = FOREACH group_by_session {
	unique_urls = DISTINCT pv_sessionized.url;
	GENERATE group, COUNT(unique_urls) as page_hits;
}

ordered_url_visits = ORDER url_visits BY page_hits; -- <== part 3: (ordered) unique URL visits per session

url_stats = FOREACH (GROUP ordered_url_visits ALL) {
  GENERATE
    AVG(ordered_url_visits.page_hits) as avg_hits,
    SQRT(VAR(ordered_url_visits.page_hits)) as std_dev_hits,
    Median(ordered_url_visits.page_hits) as median_hits;
}

dump url_stats;
predicted_unquie_URL_visits = FOREACH url_stats GENERATE avg_hits, std_dev_hits;
