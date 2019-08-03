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

## Installation

If for some unknown reason, you want to install this..

Append this to your bash profile or whatever yours is called:
```shell
export SENDAT_HOME=<the directory in which sendat.py sits>
alias sendat='${SENDAT_HOME}/sendat.py'
```

## Compatability

This has been tested on Linux Mint 19, and Ubuntu 19.04 - does not work on Mac OS.

Requires these:

```
grep
sensors
awk
lscpu
RECOMENDED: pyenv
```
