import argparse, json, os, time, glob
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
parser_start_group.add_argument('-a', '--archive', help="archive data from data/py-data/ to the directory specified\
                                                        in config/settings.json", action="store_true")
parser.add_argument('-f', '--frequency', type=int, help="set how frequently data should be collected in seconds\
                                                        in config/settings.json")
parser.add_argument('-A', '--archive-dir', type=str, help="set path to directory in which to archive data in \
                                                        in config/settings.json \
                                                        example: [ -a path/to/dir/ ]")
parser.add_argument('-S', '--settings', help="list settings defined in config/settings.json", action="store_true")
parser.add_argument('-V', '--version', help="print the version of sendat", action="store_true")
parser.add_argument('-v', '--verbose', help="print more info while running", action="store_true")
parser.add_argument('-T', '--testing', help="test functions", action="store_true")

args = parser.parse_args()

# define functions

def verbose(output):
    if args.verbose:
        print(output)

def change_state(filename, field, new_value):
    with open(filename, 'r') as json_file:
        file_to_change = json.load(json_file)
    file_to_change[field] = new_value
    with open(filename, 'w') as json_file:
        json.dump(file_to_change, json_file)

def check_state(filename, field):
    with open(filename, 'r') as json_file:
        file_to_check = json.load(json_file)
        field_value = file_to_check[field]
        return field_value

def reset_statefile():
    with open('config/statefile.json', 'w+') as json_state:
        base_state = {"running": False, "stop": False}
        json.dump(base_state, json_state)

def record_data(output_file_name, write_id, collection_freq):
    print("Recording CPU Temps: ")
    verbose('collection-frequency: {}'.format(collection_freq))
    verbose('setting running state in config/statefile.json')
    change_state('config/statefile.json', 'running', True)
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

        if check_state('config/statefile.json', 'stop'):
            verbose("stopping record_data function")
            fixup(output_file_name)
            change_state('config/statefile.json', 'stop', False)
            change_state('config/statefile.json', 'running', False)
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

# get some settings and define global vars
collection_freq = check_state('config/settings.json', 'collection-frequency')
write_id = 0

# CLI Logic

# -V --version
if args.version:
    versionNumber = open("version.txt", "r").read()
    print("sendat version: {}".format(versionNumber))

# -s --start
if (args.start and not check_state('config/statefile.json', 'running')):
    verbose('starting data collection..')
    output_file_name = (str(datetime.now()).replace(':','-').replace('.', '-').replace(' ', '-') + '.json')
    verbose("output file name: " + output_file_name)
    record_data(output_file_name, write_id, collection_freq)
elif (args.start and check_state('config/statefile.json', 'running')):
    print('aborting, already running.')

# -e --end
if args.end:
    print("stopping...")
    verbose("setting stop value in config/statefile.json")
    if check_state('config/statefile.json', 'running'):
        change_state('config/statefile.json', "stop", True)
    else:
        print('Not running - aborted end')

# -r --reset
if args.reset:
    verbose('Setting "running" state to false.')
    verbose('Setting "stop" state to False')
    try:
        change_state('config/statefile.json', 'running', False)
        change_state('config/statefile.json', 'stop', False)
    except Exception as e:
        verbose(str(e))
        hard_reset = str(input("Encountered issues with soft reset. Perform hard reset? [y/n]: "))
        if hard_reset == 'y':
            reset_statefile()
        else:
            print('Not performing hard reset. Reset aborted.')

# -a --archive
if args.archive:
    archive_dir = check_state('config/settings.json', 'archive-directory')
    verbose('Archiving data to {}.'.format(archive_dir))
    os.makedirs(archive_dir, exist_ok=True)
    data_dir_contents = glob.glob("data/py-data/*.json")
    for _file in data_dir_contents:
        filename = _file.split('/')[len(_file.split('/')) - 1]
        os.rename(_file, archive_dir + '/' + filename)

# -f --frequency
if args.frequency != None:
    verbose('Updating collection_frequency value in config/settings.json')
    change_state('config/settings.json', 'collection-frequency', args.frequency)

# -A --archive-dir
if args.archive_dir != None:
    verbose('Updating archive directory location in config/settings.json')
    change_state('config/settings.json', 'archive-directory', args.archive_dir)

# -S --settings
if args.settings:
    print('program settings:')
    print('archive-directory: {}'.format(archive_dir))
    print('collection-frequency: {}'.format(str(collection_freq)))