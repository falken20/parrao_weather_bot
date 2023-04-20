#!/usr/bin/env bash

echo ">>> Environment vars"
echo _SERVICE_ACCOUNT: $_SERVICE_ACCOUNT

echo ">>> Delete build folder"
rm -rf build

echo ">>> Create build folder and subfolders"
mkdir build
mkdir build/src
mkdir build/src/parrao_weather_bot

echo ">>> Copy files to build/src/parrao_weather_bot"
cp -R main.py build/src
cp -R parrao_weather_bot build/src

# Local execution
#export _SERVICE_ACCOUNT=cloud--functions@dev-bbva-work-space-booking-sp.iam.gserviceaccount.com

echo ">>> Folder content parrao_weather_bot:"
ls build/src/parrao_weather_bot
echo ">>> Deploy cf-send_sigma Cloud Function. Current folder:"
cd build/src/parrao_weather_bot
pwd

gcloud functions deploy cercedilla-weather-bot --region=europe-west1 \
    --runtime=python37 --entry-point=parrao_weather_bot --memory=128MB --timeout=120s \
    --env-vars-file ./credentials.yaml \
    --service-account=$_SERVICE_ACCOUNT \
    --trigger-http --source=.

gcloud functions deploy cercedilla-weather-daily-bot --region=europe-west1 \
    --runtime=python37 --entry-point=parrao_weather_bot --memory=128MB --timeout=120s \
    --env-vars-file ./credentials.yaml \
    --service-account=$_SERVICE_ACCOUNT \
    --trigger-http --source=.

echo ">>> Clean and delete build folder"
cd ../../..
rm -rf build