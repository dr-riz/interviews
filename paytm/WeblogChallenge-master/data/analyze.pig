/* analyze.pig

Rizwans-MacBook-Pro:data rmian$ pig --version
Apache Pig version 0.15.0 (r1682971) 
compiled Jun 01 2015, 11:43:55

Using pig -x local

External libs: DataFu

*/

register datafu-pig-incubating-1.3.3.jar

weblog = LOAD '2015_07_22_mktplace_shop_web_log_sample.log.gz' using PigStorage(' ') as (date_time:datetime, elb, client_port, backend_port, request_processing_time, backend_processing_time, response_processing_time, elb_status_code, backend_status_code, received_bytes, sent_bytes, request, url, user_agent, ssl_cipher, ssl_protocol);

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

L = LIMIT pv_sessionized 3; -- <== part 1: sessionized web data
dump L;

/* 

2. Determine the average session time

*/

session_times =
  FOREACH (GROUP pv_sessionized BY (sessionId,memberId)) {
    GENERATE group.sessionId as sessionId,
             group.memberId as memberId,
             (MAX(pv_sessionized.time) - MIN(pv_sessionized.time))
               / 60.0 as session_length;
}

session_stats = FOREACH (GROUP session_times ALL) {
  GENERATE
    AVG(session_times.session_length) as avg_session,
    SQRT(VAR(session_times.session_length)) as std_dev_session,
    Median(session_times.session_length) as median_session,
    Quantile(session_times.session_length) as quantile_session;
}

DESCRIBE session_stats; -- <== part 2: includes average session time
DUMP session_stats; 

/*

3. Determine unique URL visits per session. To clarify, count a hit to a unique URL only once per session.

*/

group_by_session = group pv_sessionized by sessionId;
url_visits = FOREACH group_by_session {
	unique_urls = DISTINCT pv_sessionized.url;
	GENERATE group, COUNT(unique_urls) as page_hits;
}

ordered_url_visits = ORDER url_visits BY page_hits;  -- <== part 3: (ordered) unique URL visits per session

/*

4. Find the most engaged users, ie the IPs with the longest session times

*/

long_sessions = FILTER session_times BY session_length > session_stats.quantile_session.quantile_0_95;
  
most_engaged_users = DISTINCT (FOREACH long_sessions GENERATE memberId, session_length);
DUMP most_engaged_users; -- <== part 4: ips with the longest session length

/*

Additional questions for Machine Learning Engineer (MLE) candidates:

1. Predict the expected load (requests/second) in the next minute

Assumptions:
- each record in the log represents a request

Method: simple time series or running average. average the number of transactions in last some minutes, say 5, to estimate load next minute

*/

all_group = group pv all;
max_timestamp = foreach all_group generate MAX(pv.time) as max_time;

last_m_samples = FILTER pv BY time > (max_timestamp.max_time/60 - 5); -- convert to min and subtract 5m

last_m_samples_all = Group last_m_samples All;
rate = foreach last_m_samples_all  Generate COUNT(last_m_samples.request) as num_requests;
prediction = FOREACH rate GENERATE num_requests/5.0*60.0 as requests_per_second:double;
dump prediction; -- <== part 1: MLE predict the expected load (requests/second) 

/*

2. Predict the session length for a given IP [only]

Assumptions:
- frequency distribution of session lengths is bell-like

Discussion: Ask is to predict the session length (regression) given one feature only, namely ip address. An ip address is (near) unique. We need features to generalize to train a regression model. For example, received_bytes is a generalizable and a numeric feature. In this example, the intuition is if the size of the request received from the client is large, so will be the session length or duration.

Unless, an ip address is a proxy to a generalizable feature such as population of the city where the traffic is coming from, for example. This merits investigation and left as future work.

Suppose, ip address does not generalize then a simple alternate might be to provide an mean or median value. Even mode works. I augment mean value with standard deviation to provide variance in the prediction.

In my first 100 examples of the provide log (or web_catalog.csv), the mean and median are very different suggesting that the frequency distribution is NOT bell-like. In such cases, median might be a work around or better yet transform the distribution into bell-like shape, also left for future work.

Method: 
Using session_stats from part (4) of P&A.

*/

dump session_stats;
predicted_session_length = FOREACH session_stats GENERATE avg_session, std_dev_session;
dump predicted_session_length;

/*

3. Predict the number of unique URL visits by a given IP [bound to a session]

Assumptions:
- frequency distribution of url visits is bell-like

Discussion: the discussion on ip address as a feature in MLE part 2 also applies here.

Method: Using session_stats from part (3) of P&A.

*/

url_stats = FOREACH (GROUP ordered_url_visits ALL) {
  GENERATE
    AVG(ordered_url_visits.page_hits) as avg_hits,
    SQRT(VAR(ordered_url_visits.page_hits)) as std_dev_hits,
    Median(ordered_url_visits.page_hits) as median_hits;
}

dump url_stats;
predicted_unquie_URL_visits = FOREACH url_stats GENERATE avg_hits, std_dev_hits;
dump predicted_unquie_URL_visits;