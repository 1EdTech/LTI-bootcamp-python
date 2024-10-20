#!/usr/bin/bash

ACTIVITY=${ACTIVITY_NUMBER:-4}
cd /usr/src/app/activities/activity$ACTIVITY

echo "Running exercise activity$ACTIVITY"

python /usr/src/app/activities/activity$ACTIVITY/app.py
