import argparse, json, os, time, glob
from datetime import datetime

# define global vars
settings_loc = 'config/settings.json'
state_loc = 'config/statefile.json'
write_id = 0

# Create argparse instance
parser = argparse.ArgumentParser(description='Collects CPU temperature data (by core)')

# Create argparse groups
parser_start_group = parser.add_mutually_exclusive_group()

# Options declaration
parser_start_group.add_argument('-s', '--start', help="start cpu temp monitoring", action="store_true")
parser_start_group.add_argument('-e', '--end', help="end monitoring cpu temperatures", action="store_true")
parser_start_group.add_argument('-r', '--reset', help="reset state file; WARNING can destroy currently running \
                                                        process if used while the program is running - use ONLY \
                                                        to fix when errors have occurred.", action="store_true")
parser_start_group.add_argument('-a', '--archive', help="archive data from py-data/ to the directory specified\
                                                        in " + settings_loc, action="store_true")
parser.add_argument('-f', '--frequency', type=int, help="set how frequently data should be collected in seconds\
                                                        in " + settings_loc)
parser.add_argument('-A', '--archive-dir', type=str, help="set path to directory in which to archive data in \
                                                        in " + settings_loc + " \
                                                        example: [ -a path/to/dir/ ]")
parser.add_argument('-S', '--settings', help="list settings defined in " + settings_loc, action="store_true")
parser.add_argument('-V', '--version', help="print the version of sendat", action="store_true")
parser.add_argument('-v', '--verbose', help="print more info while running", action="store_true")

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

def reset(state_loc):
    try:
        change_state(state_loc, 'running', False)
        change_state(state_loc, 'stop', False)
    except Exception as e:
        verbose(str(e))
        hard_reset = str(input("Encountered issues with soft reset. Perform hard reset? [y/n]: "))
        if hard_reset == 'y':
            with open(state_loc, 'w+') as json_state:
                base_state = {"running": False, "stop": False}
                json.dump(base_state, json_state)
        else:
            print('Not performing hard reset. Reset aborted.')

def record_data(output_file_name, write_id, collection_freq, state_loc):
    print("Recording CPU Temps: ")
    verbose('collection-frequency: {}'.format(collection_freq))
    verbose('setting running state in ' + state_loc)
    change_state(state_loc, 'running', True)
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

        if check_state(state_loc, 'stop'):
            verbose("stopping record_data function")
            fixup(output_file_name)
            change_state(state_loc, 'stop', False)
            change_state(state_loc, 'running', False)
            break

        time.sleep(collection_freq)

def store(new_entry, output_file_name, write_id):
    with open('py-data/' + output_file_name, "a+") as data_json:
        if write_id == 0:
            data_json.write("{\n" + new_entry)
        else:
            data_json.write('\n' + new_entry)

def fixup(output_file_name):
    with open('py-data/' + output_file_name, "rb+") as data_json:
        verbose('Removing trailing comma')
        data_json.seek(-1, os.SEEK_END)
        data_json.truncate()
    with open('py-data/' + output_file_name, "a+") as data_json:
        verbose('Adding JSON closing curly bracket')
        data_json.write('\n}')
        
def archive(archive_dir):
    os.makedirs(archive_dir, exist_ok=True)
    data_dir_contents = glob.glob("py-data/*.json")
    for _file in data_dir_contents:
        path_list = _file.split('/')
        filename = path_list[-1]
        os.rename(_file, archive_dir + '/' + filename)

# CLI Logic

# -V --version
if args.version:
    versionNumber = open("version.txt", "r").read()
    print("sendat version: {}".format(versionNumber))

# -s --start
if (args.start and not check_state(state_loc, 'running')):
    verbose('starting data collection..')
    output_file_name = (str(datetime.now()).replace(':','-').replace('.', '-').replace(' ', '-') + '.json')
    collection_freq = check_state(settings_loc, 'collection-frequency')
    verbose("output file name: " + output_file_name)
    record_data(output_file_name, write_id, collection_freq, state_loc)
elif (args.start and check_state(state_loc, 'running')):
    print('aborting, already running.')

# -e --end
if args.end:
    print("stopping...")
    verbose("setting stop value in " + state_loc)
    if check_state(state_loc, 'running'):
        change_state(state_loc, "stop", True)
    else:
        print('Not running; aborted.')

# -r --reset
if args.reset:
    verbose('Setting "running" state to false.')
    verbose('Setting "stop" state to False')
    reset(state_loc)

# -a --archive
if args.archive:
    archive_dir = check_state(settings_loc, 'archive-directory')
    verbose('Archiving data to {}.'.format(archive_dir))
    try:
        archive(archive_dir)
        verbose('Success!')
    except Exception as e:
        print("Oops - something went wrong while archiving:")
        print(str(e))

# -f --frequency
if args.frequency != None:
    verbose('Updating collection_frequency value in ' + settings_loc)
    if args.frequency > 0:
        change_state(settings_loc, 'collection-frequency', args.frequency)
    else:
        print("Value must be positive and non-zero; aborting.")

# -A --archive-dir
if args.archive_dir != None:
    verbose('Updating archive directory location in ' + settings_loc)
    change_state(settings_loc, 'archive-directory', args.archive_dir)

# -S --settings
if args.settings:
    archive_dir = check_state(settings_loc, 'archive-directory')
    collection_freq = check_state(settings_loc, 'collection-frequency')
    print('program settings:')
    print('archive-directory: {}'.format(archive_dir))
    print('collection-frequency: {}'.format(str(collection_freq)))