#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd
from json import loads
from datetime import timedelta
from subprocess import getoutput


VALID_EXTENSIONS = ("mp3", "wma", "ogg", "wav", "flac")


def parse_args():
    p = argparse.ArgumentParser(
        description="The script generates a descriptive tracklist based on ffprobe output")
    p.add_argument("-f", "--ffprobe_path", required=True, type=str, help="Path to ffprobe")
    p.add_argument("-d", "--directory", default=os.getcwd(),
                   help="(Optional) A directory to scan & save the tracklist, using the current "
                        "script launch directory by default")
    namespace = p.parse_args()
    return namespace.ffprobe_path, namespace.directory


def multi_core_queue(func, queue):
    import multiprocessing
    pool = multiprocessing.Pool()
    result = pool.map_async(func, queue)
    result.wait()
    pool.close()
    pool.join()
    return result.get()


def run_ffprobe(kwargs: dict):
    j = loads(getoutput(
        '"{}" "{}" -v quiet -print_format json -show_format -show_streams'.format(
            kwargs["ffprobe"], kwargs["file_name"])))
    first_stream = j["streams"][0]
    td = timedelta(milliseconds=float(first_stream["duration"]) * 1000)
    return {
        "File Name": os.path.basename(kwargs["file_name"]),
        "Duration": str(td)[:-3],
        "Channels": int(first_stream["channels"]),
        "Sample Rate (kHz)": round(float(first_stream["sample_rate"]) / 1000),
        "Bit Rate (kbps)": round(float(first_stream["bit_rate"]) / 1000)}


if __name__ == '__main__':
    ffprobe_path, output_dir = parse_args()
    valid_files = [j for j in [os.path.join(output_dir, i) for i in os.listdir(output_dir)]
                   if os.path.isfile(j) and os.path.splitext(j)[-1].strip(".") in VALID_EXTENSIONS]
    log = multi_core_queue(run_ffprobe, [{"file_name": i, "ffprobe": ffprobe_path}
                                         for i in valid_files])
    df = pd.DataFrame(log).set_index("File Name").sort_index()

    out_file = os.path.join(output_dir, "track_list.csv")
    df.to_csv(out_file, sep=",", header=True, index=True)
    print("The tracklist was saved to: '{}'".format(out_file))
