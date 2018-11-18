#!/bin/bash

#COUNTER=1

#while true
#do
#    TIME=$(date +%T)
#    echo "Reading $COUNTER @ $TIME" >> cpu.data
#    sensors | grep 'Core *:'* >> cpu.data
#    echo "-------------------------------" >> cpu.data
#    COUNTER=$(expr $COUNTER + 1)
#    sleep 5
#done
ID_NO=0
while true
do
    TIME=$(date +%s)
    COUNTER=0
    while [[ $COUNTER < 4 ]]; do
        declare CORE_$COUNTER=$(sensors | grep -Po '(?<=Core '$COUNTER':        \+)((?!°C).)*')
        COUNTER=$(expr $COUNTER + 1)
    done

    JSON="{"'"'$ID_NO'"'": {"'"timestamp"'" : $(date +%s), "'"cputemps"'" : {"'"core_0"'": $CORE_0,"'"core_1"'": $CORE_1,"'"core_2"'": $CORE_2,"'"core_3"'": $CORE_3}}}"

    echo $JSON >> output_data.json
    echo "Written to file with ID_NO: '$ID_NO'"
    ID_NO=$(expr $ID_NO + 1)
    sleep 5
done