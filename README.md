# Sensors data

Records cpu temperatures to JSON in the /data folder. 

# Usage

`./run.sh`

failed.log isn't very interesting, and isn't a log

## issues
- New output file destination doesn't work all the time. (run.sh)
- New output files can't be generated past the 10th one, without overwriting data 
    - Will eventually use some proper data store.