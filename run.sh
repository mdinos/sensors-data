#!/bin/bash

# setting variables
PID=$(echo $$)
STOP_VALUE="0"
ARCHIVE_DIR=$(grep 'archive-directory:' config/settings.conf | awk '{print $2}')
LASTCHARS=$(cat config/endref.txt)

# helper function
help() {
    echo "hello, welcome to the sensor data package - your output data will be in ./data - here are your commands:"
    echo "      start 	 - starts monitoring of cpu temps"
    echo "      stop 	 - stops monitoring cpu temps"
    echo "      archive  - archives the generated the data to \$HOME/$ARCHIVE_DIR"
    echo "      purge    - removes all generated data from /data folder - use archive first!"
    echo "      sf       - print latest file"
    echo "      sa       - print all files in /data"
    echo "      cdi      - check data integrity (of latest file)"
    echo "      settings - show settings"
    echo "      help     - shows this dialogue"
    echo "      exit     - exit the program"
    echo "it's not recommended to exit unsafely - background processes will continue to run"
    echo "settings can be changed in config/settings.conf"
}

# checks last file has been properly formatted at the end of the file
# currently broken
checkDataIntegrity() {
    FINALCHARS=$(tail -c5 data/$1)
    if [ "$LASTCHARS" == "$FINALCHARS" ]; then
        echo "data is ok in $1"
        return 1
    else
        echo "data is bad in $1 - manual fix recomended (JSON error most likely)"
        return 0
    fi
}

help

# begin program
while true
do
    if [ "$OUTPUT_FILE" == "" ]; then
        OUTPUT_FILE="logs/failed.log"
    fi

    read command

    # start command
    if [ "$command" == "start" ]; then 
        if [ "$STOP_VALUE" == "0" ]; then
            echo "starting.."
            sleep 2
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
        if [ "$STOP_VALUE" != "1" ]; then
            echo "STOP_VALUE is not 1, why would you stop if you haven't started? :)"
        else
            echo 'stopping safely..'
            sleep 2

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

            echo "checking data integrity.."
            checkDataIntegrity $OUTPUT_FILE
        fi

    # archive data command
    elif [ "$command" == "archive" ]; then
        echo "checking for changes to archive directory..."

        # check that the settings have not been updated since run.sh was called
        if [ $(grep 'archive-directory:' config/settings.conf | awk '{print $2}') != $ARCHIVE_DIR ]; then
            ARCHIVE_DIR=$(grep 'archive-directory:' config/settings.conf | awk '{print $2}')
            echo "archive directory updated to $HOME/$ARCHIVE_DIR"
        else
            echo "archive directory not updated - still $HOME/$ARCHIVE_DIR"
        fi

        echo "Copying data from /data to $HOME/$ARCHIVE_DIR"
        ./child_processes/archive.sh $ARCHIVE_DIR
        echo "Data (probably) copied to $HOME/$ARCHIVE_DIR! (you should probably check)"
    
    # call help function
    elif [ "$command" == "help" ]; then
        help

    # purge /data function
    elif [ "$command" == "purge" ]; then
        echo "are you sure? this will delete everything in the data folder! only 'yes' will be accepted response"
        read verification
        if [ "$verification" == "yes" ]; then
            echo "purging data from /data"
            rm -r data/sensor*
            echo "done!"
        else
            echo "operation cancelled."
        fi

    # exit command, checks STOP_VALUE before exiting
    elif [ "$command" == "exit" ]; then
        if [ "$STOP_VALUE" == "0" ]; then
            echo "exiting.."
            break
        else
            echo "cannot exit: processes still running - use command 'stop' to end data collection."
        fi

    # show last file
    elif [ "$command" == "sf" ]; then
        ls -t data/ | head -1
        cat data/$(ls -t data/ | head -1)

    elif [ "$command" == "sa" ]; then
        ls -lt data/
    
    elif [ "$command" == "settings" ]; then
        cat config/settings.conf

    # no command given
    elif [ "$command" == "" ]; then
        noCommand=""

    # run checkDataIntegrity function
    elif [ "$command" == "cdi" ]; then
        if [ "$OUTPUT_FILE" == 'logs/failed.log' ]; then
            echo "you haven't written any data in this session yet - try collecting some data."
        else
            checkDataIntegrity $OUTPUT_FILE
        fi

    # incorrect command
    else
        echo 'incorrect command, try "help"'
    fi

done