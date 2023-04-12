#!/usr/bin/env bash

# LOAD PROPERTIES
#. version.properties

echo ">>> Environment vars"
echo _SERVICE_ACCOUNT: $_SERVICE_ACCOUNT
echo _BBVA_GAE_ENV: $_BBVA_GAE_ENV
echo _TOPIC_NAME: $_TOPIC_NAME

echo ">>> Delete build folder"
rm -rf build

echo ">>> Create build folder and subfolders"
mkdir build
mkdir build/src
mkdir build/src/send_sigma
mkdir build/src/init_sigma

echo ">>> Copy files to build/src/send_sigma"
cp -R src/send_sigma build/src
echo ">>> Copy files to build/src/init_sigma"
cp -R src/init_sigma build/src

# Local execution
#export _SERVICE_ACCOUNT=cloud--functions@dev-bbva-work-space-booking-sp.iam.gserviceaccount.com
#export _BBVA_GAE_ENV=dev

echo ">>> Folder content send_sigma:"
ls build/src/send_sigma
echo ">>> Folder content init_sigma:"
ls build/src/init_sigma

echo ">>> Deploy cf-send_sigma Cloud Function. Current folder:"
cd build/src/send_sigma
pwd
gcloud functions deploy cf-send_sigma --region=europe-west1 \
    --runtime=python39 --entry-point=send_sigma --memory=128MB --timeout=120s \
    --trigger-topic=$_TOPIC_NAME \
    --env-vars-file ./env-$_BBVA_GAE_ENV.yaml \
    --service-account=$_SERVICE_ACCOUNT

echo ">>> Deploy cf-init_sigma Cloud Function. Current folder:"
cd ../../../build/src/init_sigma
pwd
gcloud functions deploy cf-init_sigma --region=europe-west1 \
    --runtime=python39 --entry-point=init_sigma --memory=128MB --timeout=120s \
    --trigger-http \
    --env-vars-file ./env-$_BBVA_GAE_ENV.yaml \
    --service-account=$_SERVICE_ACCOUNT

echo ">>> Clean and delete build folder"
cd ../../..
rm -rf build