# WeblogChallenge
As requested, this is a clone from [Paytm Challenge](https://github.com/PaytmLabs/WeblogChallenge). I annote with my notes. 

The challenge is to make analytical \[and predictive\] observations about the data using the distributed tools below.

## Processing & Analytical goals:
1. Sessionize the web log by IP. Sessionize = aggregrate all page hits by visitor/IP during a fixed time window.
    https://en.wikipedia.org/wiki/Session_(web_analytics)

> fixed time window or session length = 10m

```
grunt> describe pv_sessionized; -- <== part 1: sessionized web data
pv_sessionized: {time: long,memberId: chararray,request: bytearray,url: bytearray,sessionId: chararray}
```

2. Determine the average session time

```
DESCRIBE session_stats; -- <== part 2: includes average session time
session_stats: {avg_session: double,std_dev_session: double,median_session: (quantile_0_5: double),quantile_session: (quantile_0_9: double,quantile_0_95: double)}
DUMP session_stats; 
(44.39341719679457,..) -- 44m cannot be true as the session time window is 10m?
```

3. Determine unique URL visits per session. To clarify, count a hit to a unique URL only once per session.

```
ordered_url_visits = ORDER url_visits BY page_hits;  -- <== part 3: (ordered) unique URL visits per session
```

4. Find the most engaged users, ie the IPs with the longest session times

```
DUMP most_engaged_users; -- <== part 4: ips with the longest session length
...
(223.176.170.194,569.4)
(223.176.171.134,649.6)
(223.223.143.253,423.3)
```

## Additional questions for Machine Learning Engineer (MLE) candidates:
1. Predict the expected load (requests/second) in the next minute

> Method: simple time series or running average. average the number of transactions in last some minutes, say 5, to estimate load next minute
```
dump prediction; -- <== part 1: MLE predict the expected load (requests/second) 
(1.3902E7) -- seems very high!!!
```

2. Predict the session length for a given IP [only]

*Discussion: Ask is to predict the session length (regression) given one feature only, namely ip address. My peers actually build a model \[1,2\]. I hold a different view. An ip address is (near) unique. We need features to generalize to train a regression model. For example, received_bytes is a generalizable and a numeric feature. In this example, the intuition is if the size of the request received from the client is large, so will be the session length or duration.

*Unless, an ip address is a proxy to a generalizable feature such as population of the city where the traffic is coming from, for example. This merits investigation and left as future work.

*Suppose, ip address does not generalize then a simple alternate might be to provide an mean or median value. Even mode works. I augment mean value with standard deviation to provide variance in the prediction.

*In my first 100 examples of the provide log (or web_catalog.csv), the mean and median are very different suggesting that the frequency distribution is NOT bell-like. In such cases, median might be a work around or better yet transform the distribution into bell-like shape, also left for future work.

> Method: Using session_stats from part (4) of P&A.

```
describe predicted_session_length;
predicted_session_length: {avg_session: double,std_dev_session: double}
dump predicted_session_length;
(44.393417196794196,143.88047555352557) -- standard deviation is many folds of mean
```

3. Predict the number of unique URL visits by a given IP [bound to a session]

> Assumptions: frequency distribution of url visits is bell-like
* Discussion: the discussion on ip address as a feature in MLE part 2 also applies here.
> Method: Using session_stats from part (3) of P&A.

```
describe predicted_unquie_URL_visits;
predicted_unquie_URL_visits: {avg_hits: double,std_dev_hits: double}
dump predicted_unquie_URL_visits;
(9.526594804735819,116.89537611835442)
```

## Tools allowed (in no particular order):
- Used path of least resistance. Pig on local mac.

### Additional notes:
- You are allowed to use whatever libraries/parsers/solutions you can find provided you can explain the functions you are implementing in detail.
| Used DataFu for Sessionzation and Stats calculation
- IP addresses do not guarantee distinct users, but this is the limitation of the data. As a bonus, consider what additional data would help make better analytical conclusions
| To identify unique users: augment with other features such as user agent, 
| To predict: do some feature engineering, extract the region of ip address
- For this dataset, complete the sessionization by time window rather than navigation. Feel free to determine the best session window time on your own, or start with 15 minutes.
| I see this as a convergence exercise. 
- The log file was taken from an AWS Elastic Load Balancer:
http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/access-log-collection.html#access-log-entry-format


## What are we looking for? What does this prove?

We want to see how you handle:
- New technologies and frameworks
- Messy (ie real) data
- Understanding data transformation
This is not a pass or fail test, we want to hear about your challenges and your successes with this particular problem.

## Challenges faced
- data handling with the syntax of pig latin
- Unclear purpose of the analytical and prediction exercise as that would have guided the investigation. One possible objective is maximum user engagement.

## References
1. https://github.com/lawrenceyan/WeblogChallenge
2. https://github.com/shuangao/paytm
3. http://datafu.incubator.apache.org/docs/datafu/getting-started.html
