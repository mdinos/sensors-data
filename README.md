# Sensors data

Records cpu temperatures to JSON in the /data folder. 

# Usage

`./run.sh`

failed.log isn't very interesting, and isn't a log

If you want to see data going into the file live, then open up another terminal window and do `tail -f path/to/file`

## issues
- New output file destination doesn't work all the time. (run.sh) - solved by having an init file -> change to if directory empty then sensors_data_1.json
- New output files can't be generated past the 10th one, without overwriting data -> change to number of files in the directory determines the filename
    - Will eventually use some proper data store -> pssssshhh

## the future
- hook up some graphing thing
- use maybe mongo to store data
- extrapolate more subprocesses - keep run.sh as barebones as possible
    - don't bother doing that for the functions which just run a single command like 'sf'
