"""
this script converts xlsx file to csv
"""
from openpyxl import load_workbook
import argparse
import os

def convert(file, folder):
    fn = file.split('.')[0]
    wb = load_workbook(filename=os.path.join(folder, file),
                       read_only=True)
    ws = wb[fn]
    with open(os.path.join(folder, fn + '.csv'), 'w') as fp:
        for row in ws.rows:
            fp.write(';'.join([str(i.value) for i in row]) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', action='store',
                        help='convert all the xlsx in the specified direcotry.')
    parser.add_argument('-f', '--file', action='store',
                        help='convert only the specified xlsx file.')
    args = parser.parse_args()

    if args.directory:
        folder = args.directory
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith('.xlsx') and not file.startswith('~'):
                    convert(file, folder)

    if args.file:
        if os.path.isfile(args.file):
            folder = os.path.dirname(args.file)
            file = os.path.basename(args.file)
            if file.endswith('.xlsx') and not file.startswith('~'):
                convert(file, folder)

if __name__ == '__main__':
    main()