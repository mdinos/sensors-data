# Sensors data

Records cpu temperatures to JSON in the /data folder. 

# Usage

Generic usage:
`python sendat.py [OPTIONS]`

`python sendat.py --help`

Start:
`python sendat.py -s`

Stop (in a different terminal):
`python sendat.py -e`

## Compatability

This has been tested on Linux Mint 19 - does not work on Mac OS.

Requires these:

```
grep
sensors
awk
lscpu
RECOMENDED: pyenv
```
## Issues 
Doesn't work when called from the wrong directory - make relative paths safe
