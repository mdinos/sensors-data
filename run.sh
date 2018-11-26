#!/bin/bash

# setting variables
PID=$(echo $$)
STOP_VALUE="0"
DIRECTORY=$(grep 'archive-directory:' ../config/settings.conf | awk '{print $2}')

# helper function
help() {
    echo "hello, welcome to the sensor data package - your output data will be in ./data - here are your commands:"
    echo "      start 	- starts monitoring of cpu temps"
    echo "      stop 	- stops monitoring cpu temps"
    echo "      archive - archives the generated the data to \$HOME/$DIRECTORY"
    echo "      exit    - exit the program"
    echo "it's not recommended to exit unsafely - background processes will continue to run"
    echo "settings can be changed in config/settings.conf"
}

help

# begin program
while true 2
do
    if [ "$OUTPUT_FILE" == "" ]; then
        OUTPUT_FILE="logs/failed.log"
    fi

    read command

    # start command
    if [ "$command" == "start" ]; then 
        if [ "$STOP_VALUE" == "0" ]; then
            echo "starting.."
            OUTPUT_FILE="sensors_output_$(expr $(ls -t data | head -1 | tail -c 7 | head -c 1) + 1).json"
            echo "output file: $OUTPUT_FILE"
            echo '{' > data/$OUTPUT_FILE
            ./child_processes/sensors.sh $OUTPUT_FILE &
            STOP_VALUE="1"
        else
            echo "Cannot start, already running!"
        fi

    # stop command
    elif [ "$command" == "stop" ]; then
        echo 'stopping safely..'
        sleep 3
        if [ "$OUTPUT_FILE" == "logs/failed.log" ]; then
            echo "data written to logs/failed.log, check your settings."
        else
            truncate -s-2 data/$OUTPUT_FILE
            echo "" >> data/$OUTPUT_FILE
            echo "}" >> data/$OUTPUT_FILE
        fi
        pkill -TERM -P $PID
        STOP_VALUE="0"
        echo "stopped!"

    # archive data command
    elif [ "$command" == "archive" ]; then
        echo "Copying data from /data to $HOME/$DIRECTORY"
        ./child_processes/archive.sh $DIRECTORY
        echo "Data (probably) copied to $HOME/$DIRECTORY!"
    
    # call help function
    elif [ "$command" == "help" ]; then
        help

    # exit command, checks STOP_VALUE before exiting
    elif [ "$command" == "exit" ]; then
        if [ "$STOP_VALUE" == "0" ]; then
            echo "exiting.."
            break
        else
            echo "cannot exit: processes still running - use command 'stop' to end data collection. "
        fi

    # incorrect command
    else
        echo 'incorrect command, try "help"'
    fi

done