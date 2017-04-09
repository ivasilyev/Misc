#!/usr/bin/python

import sys
import os
import getopt
import multiprocessing
import logging


def usage():
    print("Usage: " + sys.argv[0] + " -i <file> -o <dir> -c <int> -m <str>" + "\n\n" +
          "-i/--input <file> \tA table without a header containing absolute path" + "\n" +
          "-o/--output <dir> \tDirectory to keep results" + "\n" +
          "-c/--cores <int> \tNumber of the CPU cores to use, maximal by default" + "\n" +
          "-m/--misc <str> \tCustom launch parameters in quotes, \"--threads 1 --gap-fill on --search-mode uniref90 --memory-use minimum\" by default" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:c:m:", ["help", "input=", "output=", "cores=", "misc="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    o = None
    c = int(multiprocessing.cpu_count())
    m = "--threads 1 --gap-fill on --search-mode uniref90 --memory-use minimum"
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
        elif opt in ("-c", "--cores"):
            try:
                c = int(arg)
            except TypeError:
                print("Incorrect cores number, using default!")
        elif opt in ("-m", "--misc"):
            m = str(arg)
    if not any(var is None for var in [i, o, c, m]):
        return i, o, c, m
    print("The parameters are not yet specified!")
    usage()


def file_to_list(file):
    file_parsed = open(file, 'rU')
    file_list = []
    for file_name in file_parsed:
        if file_name:
            file_list.append(file_name.replace("\n", ""))
    return sorted(file_list)


def humann2_launch(input_string):
    logging.info("Created process for \"" + input_string + "\" with ID: " + str(os.getpid()))
    try:
        os.system("humann2 --input " + input_string + " --output " + outputDir + " " + miscCommand)
    except MemoryError:
        logging.critical("Cannot allocate memory for processing: " + input_string)
        return
    input_file = '.'.join(input_string.rsplit('/', 1)[-1].split('.')[:-1])
    try:
        os.rename(str(outputDir + input_file + "_humann2_temp/" + input_file + ".log"), str(outputDir + input_file + ".log"))
    except FileNotFoundError as exception:
        logging.warning(str(exception))
    logging.info("Successfully processed: " + input_string)


def multi_core_queue(function):
    pool = multiprocessing.Pool(coresNumber)
    logging.info("Using " + str(coresNumber) + " cores")
    pool.map(function, inputStrings)
    pool.close()
    pool.join()


def ends_with_slash(string):
    if string.endswith("/"):
        return string
    else:
        return str(string + "/")


def is_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        logging.warning(str(exception))


#######################################################
inputFile, outputDir, coresNumber, miscCommand = main()
outputDir = ends_with_slash(outputDir)

is_path_exists(outputDir)
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=str(outputDir + '.'.join(sys.argv[0].rsplit('/', 1)[-1].split('.')[:-1]) + ".log"))
logging.info("Launching command: " + " ".join(str(i) for i in sys.argv))
logging.info("Main process ID: " + str(os.getpid()))

inputStrings = file_to_list(inputFile)

multi_core_queue(humann2_launch)
logging.info("COMPLETED")
