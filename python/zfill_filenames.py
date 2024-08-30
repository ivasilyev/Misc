#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging
from argparse import ArgumentParser


def count_numbers(s: str):
    return len(re.findall("[0-9]+", os.path.basename(s))[0])


def zfill_filenames(dir_name: str):
    files = [j for j in [os.path.join(dir_name, i) for i in sorted(os.listdir(dir_name), key=len)] if os.path.isfile(j)]
    max_length = count_numbers(files[-1])
    logging.info(f"{len(files)} filenames were parsed, the longest filename of {max_length} characters")
    previous_file_length = 0
    zfiller = ""
    for file in files:
        size = count_numbers(file)
        if size != previous_file_length:
            previous_file_length = size
            zfiller = "0" * (max_length - size)
        dst = os.path.join(dir_name, "{}{}".format(zfiller, os.path.basename(file)))
        logging.debug(f"Rename: '{file}' -> '{dst}'")
        os.rename(file, dst)


def parse_args():
    p = ArgumentParser(description="Script to add heading zeros based on longest filenames. \n"
                                   "E.g: '1a', '1b', '02', '003' -> '001a', '001b', '002', '003'. \n"
                                   "Only first met numeric sequence is accounted. \n"
                                   "Any subdirectory will not be processed. ")
    p.add_argument("-d", "--dir_name", metavar="<directory>", required=True, help="Target directory")
    ns = p.parse_args()
    return ns.dir_name


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    input_dir = parse_args()
    logging.info(f"Process '{input_dir}'")
    zfill_filenames(input_dir)
    logging.info("Completed")

