import argparse, json, os, time
from datetime import datetime

# Create argparse instance
parser = argparse.ArgumentParser(description='Collect CPU temp data')

# Options declaration
parser.add_argument('-s', '--start', help="start cpu temp monitoring", action="store_true")
parser.add_argument('-e', '--end', help="end monitoring cpu temperatures", action="store_true")
parser.add_argument('-S', '--settings', help="list settings defined in config/settings.json", action="store_true")
parser.add_argument('-V', '--version', help="print the version of sendat", action="store_true")
parser.add_argument('-v', '--verbose', help="print more info while running", action="store_true")
parser.add_argument('-t', '--testing', help="test functions", action="store_true")
parser.parse_args()

args = parser.parse_args()

# get settings and define global vars

with open('config/settings.json') as json_settings:
    settings = json.load(json_settings)
    archive_dir = settings['archive-directory']
    collection_freq = settings['collection-frequency']
    conf_file_write = settings['confirm-file-write']

write_id = 0

# define functions

def verbose(output):
    if args.verbose:
        print(output)

def change_state(field, new_value):
    with open('config/statefile.json', 'r') as state_json:
        state = json.load(state_json)
    state[field] = new_value
    with open('config/statefile.json', 'w') as state_json:
        json.dump(state, state_json)

def check_state(field):
    with open('config/statefile.json', 'r') as json_state:
        state = json.load(json_state)
        field_value = state[field]
        return field_value

def record_data(output_file_name, write_id, collection_freq):
    print("Recording CPU Temps: ")
    verbose('collection-frequency: {}'.format(collection_freq))
    verbose('setting running state in config/statefile.json')
    change_state('running', True)
    while True:
        i = 1
        temps = []
        sensors_raw = os.popen('sensors | grep \'Core\'').read()
        timestamp = round(datetime.now().timestamp())
        sensors_list = sensors_raw.split('  +')
        while i <= 4:
            temps.append(sensors_list[i][:4])
            i += 1
        new_entry = '{{ "{}" : {{ "timestamp" : {}, "cputemps" : [{}, {}, {}, {}] }}}}'.format(write_id, timestamp, temps[0], temps[1], temps[2], temps[3])
        verbose(new_entry)
        write_id += 1
        if check_state('stop'):
            verbose("stopping record_data function")
            change_state('stop', False)
            change_state('running', False)
            break
        time.sleep(collection_freq)
        
# CLI Logic

if args.version:
    versionNumber = open("version.txt", "r").read()
    print("sendat version: {}".format(versionNumber))

if (args.start and not check_state('running')):
    verbose('starting data collection..')
    output_file_name = (str(datetime.now()).replace(':','-').replace('.', '-').replace(' ', '-') + '.json')
    verbose("output file name: " + output_file_name)
    record_data(output_file_name, write_id, collection_freq)
elif (args.start and check_state('running')):
    print('aborting, already running.')

if args.end:
    print("stopping...")
    verbose("setting stop value in config/statefile.json")
    if check_state('running'):
        change_state("stop", True)
    else:
        verbose('Not running - aborted end')

if args.settings:
    print('program settings:')
    print('archive-directory: {}'.format(archive_dir))
    print('collection-frequency: {}'.format(str(collection_freq)))
    print('confirm-file-write: {}'.format(str(conf_file_write)))