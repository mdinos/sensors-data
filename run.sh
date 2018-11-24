#!/bin/bash

PID=$(echo $$)
echo "Hello, welcome to the sensor data package. Your output data will be in ./data. Here are your commands:"
echo "	 start 	- starts the service"
echo "   stop 	- stops the service"
echo "It's not recommended to exit unsafely - background processes will continue to run"

while true 
do
    if [ "$OUTPUT_FILE" == "" ]; then
        OUTPUT_FILE='logs/failed.log'
    fi
    read command
    if [ "$command" == "start" ]; then 
        OUTPUT_FILE="sensors_output_$(expr $(ls -t data | head -1 | tail -c 7 | head -c 1) + 1).json"
        echo $OUTPUT_FILE
        echo '{' > data/$OUTPUT_FILE
        ./sensors.sh data/$OUTPUT_FILE &
    elif [ "$command" == "stop" ]; then
        echo 'stopping safely..'
        if [ "$OUTPUT_FILE" == "logs/failed.log" ]; then
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

echo "Bye!"
