# Sensors data

Records cpu temperatures to JSON in the /data folder. 

# Usage

`./run.sh`

failed.log isn't very interesting, and isn't a log

If you want to see data going into the file live, then open up another terminal window and do `tail -f path/to/file`

# Python migration

The python version is better than this.

## Compatability

This has been tested on Linux Mint 19.

Currently assumes 4 cores, you can quite easily change this yourself, but the python version will detect it so you could just use that.
