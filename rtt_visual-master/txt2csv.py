""""
this script reads the marked index in .txt file and set corresponding row of .csv cpt column to 1
"""
import argparse
import os
import pandas
import logging

def convert(file, folder):
    trace_id, _ = file.split('.')
    csv_file = trace_id + '.csv'

    cp = []
    try:
        with open(os.path.join(folder, file), 'r') as fp:
            for line in fp:
                if line.strip().isdigit():
                    cp.append(int(line))
    except (IOError, TypeError, ValueError) as e:
        logging.critical("Encountered problem when reading txt: %r" % e)
        return

    if len(cp) > 0:
        try:
            trace = pandas.read_csv(os.path.join(folder, csv_file), sep=';')
        except (IOError, ValueError, TypeError, IndexError) as e:
            logging.critical("Encountered problem when reading initial csv: %r" % e)
            return
        trace.at[:, 'cp'] = 0
        trace.at[cp, 'cp'] = 1
        trace.to_csv(os.path.join(folder, csv_file), sep=';', index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', action='store',
                        help='convert all the txt in the specified direcotry.')
    parser.add_argument('-f', '--file', action='store',
                        help='convert only the specified txt file.')
    args = parser.parse_args()

    if args.directory:
        folder = args.directory
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith('.txt') and not file.startswith('~'):
                    convert(file, folder)

    if args.file:
        if os.path.isfile(args.file):
            folder = os.path.dirname(args.file)
            file = os.path.basename(args.file)
            if file.endswith('.txt') and not file.startswith('~'):
                convert(file, folder)

if __name__ == '__main__':
    main()