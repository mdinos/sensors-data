import argparse, json, os, time
from datetime import datetime

# Create argparse instance
parser = argparse.ArgumentParser(description='Collect CPU temp data')

# Create argparse groups
parser_start_group = parser.add_mutually_exclusive_group()

# Options declaration
parser_start_group.add_argument('-s', '--start', help="start cpu temp monitoring", action="store_true")
parser_start_group.add_argument('-e', '--end', help="end monitoring cpu temperatures", action="store_true")
parser_start_group.add_argument('-r', '--reset', help="reset state file; WARNING can destroy currently running \
                                                        process if used while the program is running - use ONLY \
                                                        to fix when errors have occurred.", action="store_true")
parser.add_argument('-S', '--settings', help="list settings defined in config/settings.json", action="store_true")
parser.add_argument('-V', '--version', help="print the version of sendat", action="store_true")
parser.add_argument('-v', '--verbose', help="print more info while running", action="store_true")
parser.add_argument('-t', '--testing', help="test functions", action="store_true")

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

def reset_state():
    with open('config/statefile.json', 'w+') as json_state:
        base_state = {"running": False, "stop": False}
        json.dump(base_state, json_state)

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

        new_entry = '   "{}" : {{ "timestamp" : {}, "cputemps" : [{}, {}, {}, {}] }},'.format(write_id, timestamp, temps[0], temps[1], temps[2], temps[3])
        verbose(new_entry)

        store(new_entry, output_file_name, write_id)

        write_id += 1

        if check_state('stop'):
            verbose("stopping record_data function")
            fixup(output_file_name)
            change_state('stop', False)
            change_state('running', False)
            break

        time.sleep(collection_freq)

def store(new_entry, output_file_name, write_id):
    with open('data/py-data/' + output_file_name, "a+") as data_json:
        if write_id == 0:
            data_json.write("{\n" + new_entry)
        else:
            data_json.write('\n' + new_entry)

def fixup(output_file_name):
    with open('data/py-data/' + output_file_name, "rb+") as data_json:
        verbose('Removing trailing comma')
        data_json.seek(-1, os.SEEK_END)
        data_json.truncate()
    with open('data/py-data/' + output_file_name, "a+") as data_json:
        verbose('Adding JSON closing curly bracket')
        data_json.write('\n}')


# CLI Logic

# -V --version
if args.version:
    versionNumber = open("version.txt", "r").read()
    print("sendat version: {}".format(versionNumber))

# -s --start
if (args.start and not check_state('running')):
    verbose('starting data collection..')
    output_file_name = (str(datetime.now()).replace(':','-').replace('.', '-').replace(' ', '-') + '.json')
    verbose("output file name: " + output_file_name)
    record_data(output_file_name, write_id, collection_freq)
elif (args.start and check_state('running')):
    print('aborting, already running.')

# -e --end
if args.end:
    print("stopping...")
    verbose("setting stop value in config/statefile.json")
    if check_state('running'):
        change_state("stop", True)
    else:
        print('Not running - aborted end')

# -r --reset
if args.reset:
    verbose('Setting "running" state to false.')
    verbose('Setting "stop" state to False')
    try:
        change_state('running', False)
        change_state('stop', False)
    except Exception as e:
        verbose(str(e))
        hard_reset = str(input("Encountered issues with soft reset. Perform hard reset? [y/n]: "))
        if hard_reset == 'y':
            reset_state()
        else:
            print('Not performing hard reset. Reset aborted.')

# -S --settings
if args.settings:
    print('program settings:')
    print('archive-directory: {}'.format(archive_dir))
    print('collection-frequency: {}'.format(str(collection_freq)))
    print('confirm-file-write: {}'.format(str(conf_file_write)))