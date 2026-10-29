#!/bin/sh

# Unit test and coverage
echo "***** Unit Test *****"
coverage run -m pytest -v 
echo "***** Coverage tests *****"
coverage report --omit="*/tests/*,*/venv/*,*scrapping*" -m ./*.py ./parrao_weather_bot/*.py 

# Linter checks
echo "***** Linter: Checking Python syntax errors *****"
flake8 ./*.py parrao_weather_bot tests --count --select=E9,F63,F7,F82 --show-source --statistics
# Style warnings below are advisory and do not determine test success.
echo "***** Linter: Checking Python syntax patterns *****"
flake8 ./*.py parrao_weather_bot tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics