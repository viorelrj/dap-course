# Seminar 2

[This](https://sre.google/sre-book/monitoring-distributed-systems/) paper focuses on what is system monitoring and analyses its uses and pitfalls.

Monitoring is collecting and aggregating quantitative data about the system, such as query time, service load, etc. Monitoring is quite important because it allows us detect errors in system communication and detecting bottleneck services and allows understanding how to scale it properly, using empirical data.

The best practice is to look for 4 things when monitoring:
* Latency - A bug might result in increased time of response
* Traffic - Detecting either amount of requests or the amount of data transfered in streaming connections
* Errors - Unusual rate of errors might indicate a poor quality of a service
* Saturation - Calculating the load on the service might be indicative about scaling oportunities. Especialy this would be useful for notifying about a database running out of space

It is important to select and inspect the data.

A common pitfal, for example, would be to average out the time per request in a window of 5 seconds. This is an opportunity for Really long processing time to hide between many short ones. A better approach would be to classify them into time ranges and count how many were between [0.1 and 0.3], [0.3 and 0.7] and so on.

I would generally prefer to use black-box monitoring to detect possible symptoms and really tune in with white-box on critical information, for example monitoring database fullness. Overmonitoring and raising too much importance to several warnings might be bad, because warning the administrator about transient errors might overwhelm them and cause an important warning go unnoticed, which is exactly what happened at Bigtable SRE.

