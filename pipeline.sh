#!/bin/bash

set -e  # Initiate immediate exit in each check

echo "Installing packages for running this project..."
pip install -r requirements.txt
echo "Python packages installed successfully"

echo "Ensuring Kaggle API credentials are configured..."
KAGGLE_PATH="$HOME/.kaggle/kaggle.json"
if [ ! -f $KAGGLE_PATH ]; then
    echo "Your Kaggle API credentials are not set up"
    echo "To set them up:"
    echo "1. Go to https://www.kaggle.com/account"
    echo "2. Download 'kaggle.json' file from the API section"
    echo "3. Place it in: $HOME/.kaggle/"
    echo "4. Use chmod 600 $HOME/.kaggle/kaggle.json before running script again"
    exit 1
fi
echo "Your Kaggle API credentials are set up"

echo "Running the automated ETL pipeline..."
python ./project/pipeline.py
echo "Pipeline executed successfully. SQLite database is now available"

echo "Success!"
