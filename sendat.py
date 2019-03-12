import argparse, json
from datetime import datetime

# Get current state
stop_value = 0

# Create argparse instance
parser = argparse.ArgumentParser(description='Collect CPU temp data')

# Options declaration
parser.add_argument('-s', '--start', help="start cpu temp monitoring", action="store_true")
parser.add_argument('-S', '--settings', help="list settings defined in config/settings.json", action="store_true")
parser.add_argument('-V', '--version', help="print the version of sendat", action="store_true")
parser.add_argument('-v', '--verbose', help="print more info while running", action="store_true")
parser.parse_args()

args = parser.parse_args()

# define functions

with open('config/settings.json') as json_data:
    settings = json.load(json_data)
    archive_dir = settings['archive-directory']
    collection_freq = settings['collection-frequency']
    conf_file_write = settings['confirm-file-write']

def verbose(output):
    if args.verbose:
        print(output)

def record(output_file_name):
    print('making records!')

# CLI Logic

if args.version:
    versionNumber = open("version.txt", "r").read()
    print("sendat version: %s" % (versionNumber))

if (args.start and stop_value == 0):
    verbose('starting data collection..')
    output_file_name = (str(datetime.now()).replace(':','-').replace('.', '-').replace(' ', '-') + '.json')
    verbose("output file name: " + output_file_name)
    record(output_file_name)
elif (args.start and stop_value != 0):
    print('aborting due to non-zero stop value')

if args.settings:
    print('program settings:')
    print('archive-directory: ' + archive_dir)
    print('collection-frequency: ' + str(collection_freq))
    print('confirm-file-write: ' + str(conf_file_write))