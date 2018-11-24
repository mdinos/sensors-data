#!/bin/bash

PID=$(echo $$)
echo 'Hello, welcome to the sensor data package. Here are your commands:\n start - starts the service\n stop - stops the service'

while true 
do
    if [ "$OUTPUT_FILE" == "" ]; then
        OUTPUT_FILE='failed.log'
    fi
    read command
    if [ "$command" == "start" ]; then 
        OUTPUT_FILE="sensors_output_$(expr $(ls -t data | head -1 | tail -c 7 | head -c 1) + 1).json"
        echo $OUTPUT_FILE
        echo '{' > data/$OUTPUT_FILE
        ./sensors.sh data/$OUTPUT_FILE &
        tail -f $OUPUT_FILE &
    elif [ "$command" == "stop" ]; then
        echo 'stopping..'
        if [ "$OUTPUT_FILE" == "failed.log" ]; then
            truncate -s-2 $OUTPUT_FILE
            echo "" >> $OUTPUT_FILE
            echo "}" >> $OUTPUT_FILE
        else
            truncate -s-2 data/$OUTPUT_FILE
            echo "" >> data/$OUTPUT_FILE
            echo "}" >> data/$OUTPUT_FILE
        fi
        sleep 3
        pkill -TERM -P $PID
        break
    else
        echo 'incorrect command, try "start" or "stop"'
    fi
done