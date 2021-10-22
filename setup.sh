#!/bin/bash

# Set Current Directory
PWD=`pwd`

# check if Python 3 is installed
version="$(python3 -V 2>&1)"
if [[ $version != "Python 3"* ]]
then
    version="$(python -V 2>&1)"
    if [[ $version != "Python 3"* ]]
    then
        echo 'Error: You dont have Python 3 installed' >&2
        exit 1
    fi
fi

# Check if pip is installed
version="$(pip3 -V 2>&1)"
if [[ $version != "pip"* ]]
then
    echo 'Error: You dont have pip installed' >&2
    exit 1
fi

# Create virtual environment
python3 -m venv $PWD/venv

# Function to virtual environment
activate () {
    echo 'Starting virtual environment'
  . $PWD/venv/bin/activate
    echo 'Gathering requirements with pip freeze'
    pip3 freeze > $PWD/requirements.txt
    cat $PWD/requirements.txt
    # install requirements
    echo 'Checking installation of requirements'
    pip3 install -r $PWD/requirements.txt
}

activate



