"""This script fetches for each link indicated in a directory the RTT traces of probes that passes through that link"""
import json
import traceback
import logging
import os
import argparse
import multiprocessing
import time
from collections import defaultdict


def worker(fn, probe_list, v_name):
    """for each trace chunk fn, extract the RTT measurements of probes specified in the probe_list

    Args:
        fn (string): file path to the trace chunk
        probe_list (list of string): probe trace to be extracted within this chunk

    Returns:
        res (dict): {pb:[{epoch: timestamp in epoch seconds, value: the metric to be plotted here is min_rtt},...] for pb in probe_list}
    """
    t3 = time.time()
    try:
        with open(os.path.join(fn), 'r') as fp:
            trace = json.load(fp)
    except IOError as e:
        logging.error(e)
        return dict()

    res = defaultdict(list)
    for pb in probe_list:
        pb_rec = trace.get(pb, None)
        if pb_rec:
            for t, v in zip(pb_rec.get('epoch', []), pb_rec.get(v_name, [])):
                res[pb].append(dict(epoch=t, value=v))
        else:
            logging.error("Probe %s not found in %s" % (pb, fn))

    t4 = time.time()
    logging.info("%d probes in %s handled in %.2f sec." % (len(probe_list), fn, t4-t3))
    return res


def worker_wrapper(args):
    try:
        return worker(*args)
    except Exception:
        logging.critical("Exception in worker.")
        traceback.print_exc()
        raise


def main():
    t1 = time.time()
    # log to queryrtt.log file
    logging.basicConfig(filename='queryrtt.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %z')

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--probeDirectory",
                        help="the directory storing probe IDs grouped by link",
                        action="store")
    parser.add_argument("-t", "--traceDirectory",
                        help="the directory storing all the ping measurements chunks",
                        action="store")
    parser.add_argument("-i", "--indexFile",
                        help="the file that maps probe ID to chunk IDs",
                        action="store")
    parser.add_argument("-s", "--chunckSuffix",
                        help="chunks suffix to distinguish different measurements, say, 1010.json, v4 ping for b-root",
                        action='store')
    parser.add_argument("-v", "--valueName",
                        help="the value name in trace json that you want to extract",
                        action="store")

    args = parser.parse_args()
    args_dict = vars(args)

    if not all(map(bool, args_dict.values())):
        # all the parameters must be set
        print (args.help)
        return

    if not os.path.isdir(args.probeDirectory):
        logging.critical("%s doesn't exist." % args.probeDirectory)
        return

    if not os.path.isdir(args.traceDirectory):
        logging.critical("%s doesn't exist." % args.traceDirectory)
        return

    if not os.path.isfile(args.indexFile):
        logging.critical("%s doesn't exist." % args.traceDirectory)
        return

    # check if the specified chunkSuffix is valid in the given traceDirectory
    try:
        _ = next(iter([i for i in os.listdir(args.traceDirectory) if i.endswith(args.chunckSuffix)]))
    except StopIteration:
        logging.critical("No trace file in %s ends with suffix %s" % (args.traceDirectory, args.chunckSuffix))
        return

    # given a probe id, in which chunk id shall we look for its traces
    probe2chunk = dict()
    try:
        with open(args.indexFile, 'r') as fp:
            for idx, line in enumerate(fp):
                if idx > 0 and len(line.split(';')) == 2:
                    pb, chunk = line.split(';')
                    probe2chunk[pb.strip()] = chunk.strip()
    except IOError as e:
        logging.error(e)
        return

    # each file in probeDirecotry represents the probes that passes that link
    link2probe = defaultdict(list)
    # what are the probes to be retrived per trace chunk
    taskperchunk = defaultdict(list)
    for fn in [i for i in os.listdir(args.probeDirectory) if i.endswith('.txt')]:
        try:
            with open(os.path.join(args.probeDirectory, fn), 'r') as fp:
                for line in fp:
                    # link = fn.split('.')[0]
                    link = fn[:-4]
                    pb = filter(lambda s: s.isdigit(), line.strip())
                    link2probe[link].append(pb)
                    chunkid = probe2chunk.get(pb, None)
                    if chunkid:
                        taskperchunk[os.path.join(args.traceDirectory, chunkid+'_'+args.chunckSuffix)].append(pb)
                    else:
                        logging.error("Probe %s is absent in index file" % pb)
        except IOError as e:
            logging.error(e)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    res = pool.map(worker_wrapper, [(k, v, args.valueName) for k, v in taskperchunk.items()])  # for each chunk trace, retrieve the probes traces
    res = {k: v for d in res for k, v in d.items()}  # merge the resulted list of dictionary

    for l in link2probe:
        out_fn = os.path.join(args.probeDirectory, l + '_' + args.valueName+'.json')
        rtts = {pb: res.get(pb) for pb in link2probe.get(l)}  # for each link file, fetch traces for probes that passes it
        json.dump(rtts, open(out_fn, 'w'))

    t2 = time.time()
    logging.info("RTT trace extraction done in %.2f sec." % (t2-t1))

if __name__ == '__main__':
    main()
