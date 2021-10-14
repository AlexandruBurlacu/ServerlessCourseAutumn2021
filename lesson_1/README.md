# Serverless Course

## Lesson 1: Intro and creation of a simple pair of WebHook client/server


In order to run this project, first create a virtual environment, either using `conda` or `venv` and then install everything with `pip install -r requirements.txt`.

After that, run first the `webhook_server.py` using `uvicorn`, like this:

```
uvicorn webhook_server:app
```

And then, run the same way `webhook_listener.py`, but on port 7000. `uvicorn webhook_server:app --port 7000`

Play around with both in browser from their respective Swagger pages at `/docs`


### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 1</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

