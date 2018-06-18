""""
this script read the trace in csv and labeled datapoint in txt
and visualize them in an interactive html file
"""
import timetools as tt
import pandas
from bokeh.plotting import figure, output_file, show
import argparse
import os
from bokeh.resources import CDN
from bokeh.embed import file_html
import multiprocessing
import logging
import traceback
import itertools


def plotter(file, verify):
    folder = os.path.dirname(file)
    fn = os.path.basename(file)
    trace_id = fn.split('.')[0]
    out_html = os.path.join(folder, trace_id + '.html')
    out_txt = os.path.join(folder, trace_id + '.txt')

    # prepare the txt file
    if not os.path.exists(out_txt):
        open(out_txt, 'w').close()

    # if the html file exist already and not in verify mode, skip
    if not verify and os.path.exists(out_html):
        return

    try:
        trace = pandas.read_csv(file, sep=';')
    except (IOError, ValueError, TypeError, IndexError) as e:
        logging.critical("Encountered problem when reading initial csv: %r" % e)
        return
    if type(trace['rtt'][0]) is str:
        trace = pandas.read_csv(file, sep=';', decimal=',')

    p = figure(plot_width=1200, plot_height=600,
               tools="pan, xpan, ypan, xwheel_zoom, ywheel_zoom, undo, redo, reset, hover",
               title=trace_id)
    try:
        x = [tt.string_to_datetime(i) for i in trace['epoch']]
    except TypeError:
        x = [tt.epoch_to_datetime(i) for i in trace['epoch']]
    y = trace['rtt']
    cp = [i for i, value in enumerate(trace['cp']) if value == 1]

    p.line(x, y, line_width=.5, alpha=.6)
    p.circle(x, y, size=5, color='olive', alpha=.8)

    # only plot the labeled data if required to
    if len(cp) > 0 and verify:
        logging.info("%s labeled datapoint indexes are %s" % (trace_id, str(cp)))
        p.square_x([x[i] for i in cp], [y[i] for i in cp], color='red', fill_color=None, size=5)

    html = file_html(p, CDN, title=trace_id)
    with open(out_html, 'w') as fp:
        fp.write(html)


def plotter_wrapper(argv):
    try:
        return plotter(*argv)
    except Exception:
        logging.critical("Exception in worker.")
        traceback.print_exc()
        raise


def main():
    # log setting
    logging.basicConfig(filename='visual.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %z')
    # flags
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', action='store',
                        help='the directory containing csv files.')
    parser.add_argument('-v', '--verify', action='store_true',
                        help='when present, plot the cp column in csv file')
    parser.add_argument('-f', '--file', action='store',
                        help='handle only the given csv file.')
    args = parser.parse_args()

    if args.directory:
        if os.path.isdir(args.directory):
            target_file = []  # all the csv file meant to be handled
            for file in os.listdir(args.directory):
                # only care about csv file, ignore temporary file
                if file.endswith('.csv') and not file.startswith('~'):
                    target_file.append(os.path.join(args.directory, file))
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        pool.map(plotter_wrapper, itertools.izip(target_file, itertools.repeat(args.verify)))

    if args.file:
        if os.path.isfile(args.file):
            file = os.path.basename(args.file)
            if file.endswith('.csv') and not file.startswith('~'):
                plotter(args.file, args.verify)

if __name__ == '__main__':
    main()
