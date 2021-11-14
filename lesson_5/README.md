# Serverless Course

## Lesson 5: Finishing what we started last time + reducing latencies in the system

- (5.0) Improving the system: reducing startup time and increasing hardware utilization.
- (5.1) Make it run async
- (5.2) Timeouts
- (5.3) Hot vs Cold latency. Environment reuse
- (5.4) Application-level tricks


In order to run this project, first create a virtual environment, either using `conda` or `venv` and then install everything with `pip install -r requirements.txt`.

After that, run the `app.py` using `uvicorn`, like this:

```
uvicorn app:app
```

Then, run `python gateway.py`


## Links

- [The code written during the lecture](https://github.com/AlexandruBurlacu/ServerlessCourseAutumn2021/tree/lesson-5-it-works-but-no-libs)
- Gatway is based on the code from [this blogpost](https://mleue.com/posts/simple-python-tcp-server/)
- [Some optimizations for a serverless platform](https://tomasz.janczuk.org/2018/03/how-to-build-your-own-serverless-platform.html), the second half of the article


### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 5</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

