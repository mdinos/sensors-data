# Sensors data

Records cpu temperatures to JSON in the /data folder. 

# Usage

## bash version

`./run.sh`

failed.log isn't very interesting, and isn't a log

If you want to see data going into the file live, then open up another terminal window and do `tail -f path/to/file`

## Python version

Generic usage:
`python sendat.py [OPTIONS]`

Start:
`python sendat.py -s`

Stop (in a different terminal):
`python sendat.py -e`

# Python migration

I'm moving to a python cli style utility - it will be better - progress is being made.
