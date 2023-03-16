
<div align="center">
<img src="./img/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://falken-home.herokuapp.com/static/home_project/img/falken_logo.png" width=50 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.2.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/parrao_weather_bot) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/parrao_weather_bot) ![Test coverage](https://img.shields.io/badge/test%20coverage-92%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/parrao_weather_bot)


[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com) [![Twitter](https://img.shields.io/twitter/follow/richionline?style=social)](https://twitter.com/richionline)

</div>

---
Process that every secific time get and publish weather data from Cercedilla in Twitter through Google Cloud Platform technology. A Cloud Function that get the weather data and publish it, and a Cloud Scheduler that every X time call the Cloud Function.

##### Deploy
```bash
It has to copy the content of parrao_weather_bot.py file in Cloud Function 
section in Google Cloud Platform, inside main.py file.
```
##### Setup

```bash
pip install -r requirements.txt
```
##### Setup Tests

```bash
pip install -r requirements-tests.txt
```
##### Running the app

```bash
python ./parrao_weather_bot.py
```

##### Running the tests with pytest and coverage

```bash
./scripts/check_project.sh
```

##### Environment vars
```bash
ENV_PRO=N
LOG_LEVEL=INFO

# Weather station API key
API_KEY=XXXXXXXXXXXX
STATION_ID=XXXXXXXXXXXX

# Twitter params
CONSUMER_KEY=XXXXXXXXXXXX
CONSUMER_SECRET=XXXXXXXXXXXX
ACCESS_TOKEN=XXXXXXXXXXXX
ACCESS_TOKEN_SECRET=XXXXXXXXXXXX
```
---

##### Doc API wunderground.com

API General doc: https://docs.google.com/document/d/1eKCnKXI9xnoMGRRzOL1xPCBihNV2rOet08qpE_gArAY/edit
API Current conditions: https://ibm.co/v2PWSCC

##### Versions

1.3.0 Saving daily data in DB
1.2.0 Add new cron for tweet daily resume
1.1.0 Change the data source to personal weather station
1.0.0 First version

