
<div align="center">
<img src="./img/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://richionline-portfolio.nw.r.appspot.com/static/assets/falken_logo_trans.png" width=50 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.5.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/parrao_weather_bot) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/parrao_weather_bot) ![Test coverage](https://img.shields.io/badge/test%20coverage-95%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/parrao_weather_bot)


[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com)

</div>

---
Process that periodically retrieves and publishes weather data from Cercedilla to a Telegram channel using Google Cloud Platform. Cloud Functions fetch and publish the data, and Cloud Scheduler triggers them.

##### Deploy

Run the configured Cloud Build trigger to deploy both functions using [cloudbuild.yaml](cloudbuild.yaml). The HTTP entry points are `parrao_weather_bot` and `parrao_weather_bot_daily` in [main.py](main.py); deploy the root source and its dependencies, not a single copied file.

Configure the runtime environment variables on both functions before deploying. [cloud_function.txt](cloud_function.txt) and [cloud_scheduler.txt](cloud_scheduler.txt) are reference examples, not current configuration exports. [deploy.sh](deploy.sh) is a legacy deployment script and is not the recommended workflow.

##### Setup

Use the Python version configured for Cloud Functions, currently Python 3.10 in the build configuration. Create a local environment and fill in the values copied from [.env_template](.env_template); never commit credentials.

```bash
python3.10 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
cp .env_template .env
```
##### Setup Tests

```bash
.venv/bin/python -m pip install -r requirements-tests.txt
```
##### Running the app

```bash
.venv/bin/python main.py
```

This runs the current and daily handlers. With `ENV_PRO=N`, weather is fetched and messages are logged without publishing or saving daily data. `ENV_PRO=Y` enables Telegram publishing and daily database writes. A valid `DATABASE_URL` is required when the application starts, including in preview mode.

Before enabling daily database writes, initialize the configured database:

```bash
.venv/bin/python main_db.py
```

##### Sending a Telegram message from the terminal

```bash
.venv/bin/python -m telegram_cli "Test message"
printf 'First line\nSecond line\n' | .venv/bin/python -m telegram_cli
.venv/bin/python -m telegram_cli --dry-run "Test message"
```

The CLI loads `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from `.env` with priority over exported variables. Sending is real unless `--dry-run` is specified, regardless of `ENV_PRO`. The CLI does not need the weather API or a database.

##### Running the tests with pytest and coverage

```bash
.venv/bin/python -m pytest
PATH="$PWD/.venv/bin:$PATH" ./check_app.sh
```

Tests use SQLite in memory and mocked Telegram and weather API requests. The check script prints coverage and lint results; its final style check is advisory, so review the output rather than relying only on its exit code. The legacy scraper is outside this test suite.

##### Environment vars
```bash
ENV_PRO=N
LOG_LEVEL=INFO

# Weather station API key
API_KEY=XXXXXXXXXXXX
STATION_ID=XXXXXXXXXXXX

# Database
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE

# Telegram bot
TELEGRAM_BOT_TOKEN=XXXXXXXXXXXX
TELEGRAM_CHAT_ID=@your_channel_or_chat_id
```

Replace the example values with your configuration. Configure these values in both Cloud Functions as runtime environment variables. Add the bot as a channel administrator with permission to publish. The scraper under `parrao_weather_bot/` is retained as legacy code; it is not used by the deployed handlers and additionally requires `pandas` if run manually.
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