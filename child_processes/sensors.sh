#!/bin/bash

ID_NO=0
OUTPUT_FILE="$1"
OUTPUT_PATH="data/$OUTPUT_FILE"
FREQUENCY=$(grep 'collection-frequency:' config/settings.conf | awk '{print $2}')
echo "$FREQUENCY seconds between data points. this can be adjusting in config/settings.conf"

while true
do
    COUNTER=0
    while [[ $COUNTER -lt 4 ]]; do
        declare CORE_$COUNTER=$(sensors | grep -Po '(?<=Core '$COUNTER':        \+)((?!°C).)*')
        COUNTER=$(expr $COUNTER + 1)
    done

    JSON=""'"'$ID_NO'"'": {"'"timestamp"'" : $(date +%s), "'"cputemps"'" : {"'"core_0"'": $CORE_0,"'"core_1"'": $CORE_1,"'"core_2"'": $CORE_2,"'"core_3"'": $CORE_3}},"

    echo $JSON >> $OUTPUT_PATH
    echo "Written to file with ID_NO: '$ID_NO'"
    ID_NO=$(expr $ID_NO + 1)
    sleep "$FREQUENCY"
done