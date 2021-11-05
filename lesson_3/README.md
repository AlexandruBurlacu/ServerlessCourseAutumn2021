# Serverless Course

## Lesson 3: Implementing a rough serverless core. The API.


In order to run this project, first create a virtual environment, either using `conda` or `venv` and then install everything with `pip install -r requirements.txt`.

After that, run the `app.py` using `uvicorn`, like this:

```
uvicorn app:app
```

**Note**: don't run it with `--reload`, because if you do, the server will notice changes in the working directory when you create a new function, restart the server, and in turn delete the "database" entry about the said function.

Play around with both in browser from their respective Swagger pages at `/docs`.

A basic workflow would be:
1. Create a serverless function with `POST /functions`
2. List available serverless functions with `GET /functions`
3. Finally, trigger a function execution with `POST /functions/trigger`


## Links

- [The architecture of a serverless platform](https://tomasz.janczuk.org/2018/03/how-to-build-your-own-serverless-platform.html), the first half of the article
- [The code written during the lecture](https://github.com/AlexandruBurlacu/ServerlessCourseAutumn2021/tree/lesson-3-it-works-but-ugly), the steps to launch it and the example workflow are the same as described above. 


### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 3</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

