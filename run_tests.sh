#!/bin/bash

# Set Current Directory
PWD=`pwd`

cd *_app

python -m unittest discover -s tests -v

cd $PWD