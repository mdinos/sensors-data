# settings descriptions

### archive-directory
The directory in which you want to save your files when performing the `archive` command, set by default to `~/sensors_data_archive/001/`
Makes the directories necessary if it doesn't exist already.

### collection-frequency
The time in seconds between data entries.

Warning: If you set this very low, for instance when I put it to 0.001 seconds, there is a relatively high likelihood that your json will be corrupted and you will have to fix it. This will not be difficult.

### confirm-file-write
Set this to `true` if you want to get an echo every time a line is put into a file.
Will have more options for this in future - ie. you could print every 5 or 10 or whatever you like.

# Python Version

The python version of this program uses the `settings.json` and `statefile.json`. These do not need to be touched manually - they can be updated and changed via the CLI interface as described in the `--help`.