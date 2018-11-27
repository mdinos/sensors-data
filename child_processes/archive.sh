#!/bin/bash

ARCHIVE_DIR=$1
echo $ARCHIVE_DIR

if [ ! -d "$HOME/$ARCHIVE_DIR" ]; then
    echo "Making directory $HOME/$ARCHIVE_DIR"
    mkdir $HOME/$ARCHIVE_DIR
fi

FILES=$(ls | grep 'sensors_data_*')
cp data/sensors_output_* $HOME/$ARCHIVE_DIR

echo "Last 5 files copied:"
ls $HOME/$ARCHIVE_DIR | tail -5

exit 0