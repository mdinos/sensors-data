#!/bin/bash

DIRECTORY=sensors-data-archive

if [ ! -d "$HOME/$DIRECTORY" ]; then
    echo "Making directory $DIRECTORY"
    mkdir $HOME/$DIRECTORY
fi

FILES=$(ls | grep 'sensors_data_*')
cp data/sensors_output_* $HOME/$DIRECTORY

echo "Last 5 files copied:"
ls $HOME/$DIRECTORY | tail -5

exit 0