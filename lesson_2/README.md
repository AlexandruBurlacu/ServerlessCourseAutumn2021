# Serverless Course

## Lesson 2: Cloud computing and serverless computing. Defining our requirements and interfaces.
- 2.1. Review code from last time
- 2.2. What is a cloud? How is a cloud?
- 2.3. Serverless computing specifics. Interesting Use cases. Current limitations.
- 2.4. Basic requirements of a serverless platform
- 2.5. The architecture of a serverless platform
- 2.6. Defining the Management API for the serverless platform

## (Ultra-)Basic functional requirements for a serverless platform

- Create/instantiate Execution Media on demand, in our case wil be only one type of execution medium, a python3 container
- CRUD for Functions (FaaS event handlers)
- Trigger Function execution/execution media provisioning on some event


## Management API

- `GET /functions` - List all functions
- `POST /functions` - Create a new function
```
{
  event_type: EventType
  function_name: String
  function_body: Code
}
```

- `DELETE /functions/:function_id` - Pretty self explanatory

- `POST /functions/:event_type/trigger` - Trigger function execution
```
{
  request_headers: Headers
  request_path: Path
  request_body: Body
}
```


## Links

- [About serverless in general](https://martinfowler.com/articles/serverless.html)
- [About serverless limitations and implementation details](https://www.infoq.com/articles/serverless-internals/)
- [More on serverless limitations](https://blog.acolyer.org/2019/01/14/serverless-computing-one-step-forward-two-steps-back/)
- [About a new way to do serverless](https://blog.acolyer.org/2020/02/07/cloudburst/)

### Some usecases
- [Using serverless for data analytics](http://pywren.io/)
- [Using serverless for CI](https://hichaelmart.medium.com/lambci-4c3e29d6599b)
- [Scalable cache using serverless](https://www.usenix.org/system/files/fast20-wang_ao.pdf)
- [A more general tool to orchestrate serverless functions](https://cs.stanford.edu/~matei/papers/2019/usenix_atc_gg.pdf)

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 2</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
