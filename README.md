
<div align="center">
<img src="./img/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://richionline-portfolio.nw.r.appspot.com/static/assets/falken_logo_trans.png" width=50 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.5.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/parrao_weather_bot) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/parrao_weather_bot) ![Test coverage](https://img.shields.io/badge/test%20coverage-93%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/parrao_weather_bot)


[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com)

</div>

---
Process that periodically retrieves and publishes weather data from Cercedilla to a Telegram channel using Google Cloud Platform. Cloud Functions fetch and publish the data, and Cloud Scheduler triggers them.

##### Deploy
```bash
It has to copy the content of parrao_weather_bot.py file in Cloud Function 
section in Google Cloud Platform, inside main.py file.
```
OR 
```bash
Execute Build trigger in Google Console when push repo
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

# Telegram bot
TELEGRAM_BOT_TOKEN=XXXXXXXXXXXX
TELEGRAM_CHAT_ID=@your_channel_or_chat_id
```

Configure these values in both Cloud Functions as runtime environment variables. Add the bot as a channel administrator with permission to publish.
---

##### Doc API wunderground.com

API General doc: https://docs.google.com/document/d/1eKCnKXI9xnoMGRRzOL1xPCBihNV2rOet08qpE_gArAY/edit
API Current conditions: https://ibm.co/v2PWSCC

##### Versions
- 1.5.0 Replace X publishing with Telegram Bot API
- 1.4.1 Python version of Cloud Functions raise to Python 3.10
- 1.3.1 cloudbuild.yaml to deploy functions
- 1.3.0 Saving daily data in DB
- 1.2.0 Add new cron for daily weather summary
- 1.1.0 Change the data source to personal weather station
- 1.0.0 First version

##### Learning tips
- Google Cloud Build
- Google Cloud Functions
- Google Cloud Scheduler
- SqlAlchemy