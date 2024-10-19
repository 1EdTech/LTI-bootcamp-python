#!/bin/bash

# Default to exercise1 if no parameter is provided
ACTIVITY=${ACTIVITY_NUMBER:-1}

# Navigate to the specified exercise directory
cd /usr/src/app/activities/activity$ACTIVITY

echo "Running exercise activity$ACTIVITY"

# Run the exercise's main Python script
python app.py
