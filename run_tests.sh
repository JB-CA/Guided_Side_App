#!/bin/bash

# Set Current Directory
PWD=`pwd`

# Change to directory where the tests are located
cd *_app

# Run tests
python3 -m unittest discover -s tests -v

# Change back to original directory
cd $PWD