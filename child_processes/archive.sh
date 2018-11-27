#!/bin/bash

ARCHIVE_DIR=$1
echo $ARCHIVE_DIR

if [ ! -d "$HOME/$ARCHIVE_DIR" ]; then
    echo "making directory $HOME/$ARCHIVE_DIR"
    mkdir -p $HOME/$ARCHIVE_DIR
fi

FILES=$(ls | grep 'sensors_data_*')
cp data/sensors_output_* $HOME/$ARCHIVE_DIR

echo "last 5 files copied: (if there are 5..)"
ls $HOME/$ARCHIVE_DIR | tail -5