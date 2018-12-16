#!/bin/bash

ARCHIVE_DIR=$1

if [[ ! -d ${HOME}/${ARCHIVE_DIR} ]]; then
    echo "making directory $HOME/$ARCHIVE_DIR"
    mkdir -p $HOME/$ARCHIVE_DIR
else 
    echo "directory exists, proceeding.."
fi

FILES=$(ls | grep 'sensors_data_*')
cp data/sensors_output_* $HOME/$ARCHIVE_DIR

echo "last 5 files copied: (if there are 5..)"
ls $HOME/$ARCHIVE_DIR | tail -5