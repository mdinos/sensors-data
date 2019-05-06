# Sensors data

Records cpu temperatures to JSON in the /data folder. 

# Usage

Generic usage:
`python sendat.py [OPTIONS]`

Start:
`python sendat.py -s`

Stop (in a different terminal):
`python sendat.py -e`

## Compatability

This has been tested on Linux Mint 19.

Requires these:

```
grep
sensors
awk
lscpu
RECOMENDED: pyenv
```
## Issues \nDoesn't work when called from the wrong directory - make relative paths safe by settings a /home/marcus/git/me/sensors-data
