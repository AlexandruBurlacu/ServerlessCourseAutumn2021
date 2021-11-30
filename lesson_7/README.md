# Serverless Course

## Lesson 7: Scaling out the system: Load balancing and Caches.
- (7.0) Scale Cube. How to scale a system
- (7.1) Load balancing strategies
  - (7.1.1) Back end Load Balancing
  - (7.1.2) Front end Load Balancing
    - (7.1.2.1) Round Robin vs Least Connected
    - (7.1.2.2) N load balancers for M services. Power of 2 Choices load balancing
    - (7.1.2.3) Sticky sessions. Consistent Hashing load balancing
    - (7.1.2.4) Issues
- (7.2) Caching
  - (7.2.1) Types of caches
  - (7.2.2) CDNs
  - (7.2.3) Edge Serverless Computing

### Links about Scalability

#### Front end (inter servers/zones) load balancing
- [DNS load balancing explained](https://www.dns-anycast.com/dns-load-balancing-explained/)
- [Anycast for load balancing](https://www.usenix.org/legacy/events/lisa10/tech/full_papers/Weiden.pdf)
- [Some more info about Anycast](https://www.cloudflare.com/learning/cdn/glossary/anycast-network/)
- [Chapter from the SRE Book by Google, on this very topic](https://sre.google/sre-book/load-balancing-frontend/)
- [Maglev is a very low latency load balancer, usually more useful closer to the front end of the cloud](https://blog.cloudflare.com/high-availability-load-balancers-with-maglev/)

#### Back end (inter applications/services) load balancing
- [A thread from Hacker News](https://news.ycombinator.com/item?id=14640811) in which people mention [this article from Vimeo](https://medium.com/vimeo-engineering-blog/improving-load-balancing-with-a-new-consistent-hashing-algorithm-9f1bd75709ed) on how load balancing is not not simple.
- [NGINX configuration for different types of load balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [Chapter from the SRE Book by Google, on this very topic #2](https://sre.google/sre-book/load-balancing-datacenter/)

#### Caching
- [Cold caches can cause thundering heards](https://instagram-engineering.com/thundering-herds-promises-82191c8af57d)
- [What is a CDNs](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)
- [More on caching](https://aws.amazon.com/caching/database-caching/)
- [Database caches](https://redfin.engineering/how-to-boost-postgresql-cache-performance-8db383dc2d8f), specifically Postgres

#### Edge serverless computing examples
- [From AWS](https://aws.amazon.com/lambda/edge/)
- [From Cloudlfare](https://workers.cloudflare.com/)
- [From Netlify](https://www.netlify.com/products/functions/)
- [A primer of using serverless and CDNs in a super efficient and cost effective way](https://www.troyhunt.com/serverless-to-the-max-doing-big-things-for-small-dollars-with-cloudflare-workers-and-azure-functions/)


### Keywords
- Murmurhash
- Consistency hashing
- Spanning Tree Protocol
- BGP
- GeoIP
- Prepopulated vs Lazy cache
- Memoization (in the context of algorithms and dynamic programming)


### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 7</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

