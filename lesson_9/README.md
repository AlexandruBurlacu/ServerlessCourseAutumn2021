# Serverless Course

## Lesson 9, final lecture: Ensuring fault tolerance
- (9.1) Measuring availability
  - (9.1.1) The usual way
    - (9.1.1.1) Time-based (uptime / total time)
    - (9.1.1.2) Count-based (successful requests / total requests)
  - (9.1.2) The better way (time-based per user)
- (9.2) Fault tolerance patterns
  - (9.2.1) Retries with exponential backoff and jitter
  - (9.2.2) Circuit breaking
  - (9.2.3) Bulkheads
  - (9.2.4) Rate limiting and throttling
  - (9.2.5) Watchdog threads
- (9.3) Can we go beyond Fault tolerance? Anti-fragility?
  - (9.3.1) Chaos engineering
  - (9.3.2) Post-mortems and 5 Whys
  - (9.3.3) Observability
  - (9.3.4) CI/CD/Automation
  - (9.3.5) Regression Suite
  - (9.3.6) Exploratory Tests


### Links about Fault-Tolerance

#### Availability measures
- [About how Google uses a better way to measure availability](https://blog.acolyer.org/2020/02/26/meaningful-availability/)
- [A few notes from AWS about availability](https://d1.awsstatic.com/whitepapers/aws_availability_and_beyond_white_paper.pdf)


#### Fault-tolerance patterns
- [How to handle cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)
- [Or if it's not yet that bad, just overloads](https://sre.google/sre-book/handling-overload/)

- [Why choose specifically exponential backoffs with jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Same question as above, but you're lazy and don't want to dive so deep](https://stackoverflow.com/questions/46939285/why-is-random-jitter-applied-to-back-off-strategies)
- [Circuit breakers](https://iyer.ai/circuit-breakers-in-microservices/)

- [About rate-limiting](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)
- [More about rate-limiting](https://stackoverflow.com/questions/1450217/what-is-the-best-way-to-implement-a-rate-limiting-algorithm-for-web-requests)
- [Throttling and debouncing](https://redd.one/blog/debounce-vs-throttle)

- [Watchdogs, very high-level](https://www.cloudcomputingpatterns.org/watchdog/)

- [What are bulkheads](https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead)
- [How bulkheads are implemented in Hystrix](https://stackoverflow.com/questions/30391809/what-is-bulkhead-pattern-used-by-hystrix)


#### Misc
- [Docker resource limits can be used as primitive bulkheads](https://docs.docker.com/engine/reference/commandline/run/#set-ulimits-in-container---ulimit), especially usefull when there's a risk of excesive resource usage.
- A combination of `docker restart`, shell scripts and `cron` can be used as a very rough watchdog
- [Exploratory testing](https://www.guru99.com/exploratory-testing.html), or for a more detailed and somewhat philosophical explanation, see the Exploratory Testing chapter in the book "The art of agile development, 1st edition", on page 344.
- [Why are post-mortems important, and how to conduct them well](https://sre.google/sre-book/postmortem-culture/)


### Keywords
- Apache Hystrix
- Resilience4j
- Antifragile
- Netflix Chaos Monkey
- Nines (3 and a half 9s => 99.95%, five nines => 99.999%)
- MTTR (mean time to recover) and MTBF (mean time between failures)


### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 9</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

