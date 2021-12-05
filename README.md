# getSauce - A Flask Based Web Application

A Flask Based Web-app which provides source for given screencap of Movies, Shows and Anime.

for this the app relies on [SauceNAO API](https://saucenao.com) and [pysauceno](https://github.com/FujiMakoto/pysaucenao) API wrapper.
it also saves search history in SQLite database which can be retrieved in Json file.

# Installation

application requires [Python](https://python.org) and other dependencies mentioned in the `requirements.txt` file.

- install required packages using following command,

```shell script
 pip install -r requirements.txt
```

- create a `.env` file and add following keys with appropriate values -
```shell script
API_KEY                       # your api key
SQLITE_URI                    # database connection string
SECRET_KEY                    # secret for flask
```

- run `app.py` file which will start the application.
