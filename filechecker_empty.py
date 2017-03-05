# -*- coding: utf-8 -*-
# !/usr/bin/python

import os
import getopt
import sys
import multiprocessing


def usage():
    print("Usage: " + sys.argv[0] + " -i/--input <dir> \t\tFolder to scan for empty files" + "\n" +
          "-o/--output <file> \t\tWhere to keep results" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, o]):
        return i, o
    print("The parameters are not yet specified!")
    usage()


def job(string):
    if os.stat(str(string)).st_size > 0:
        return string + "\tOK\n"
    else:
        return string + "\tEMPTY\n"


def list_to_file(header, list_to_write, file_to_write):
    header += "".join(str(i) for i in list_to_write if i if i is not None)
    file = open(file_to_write, 'w')
    file.write(header)
    file.close()


###############################
inputDir, outputFile = main()
inputDir = str(inputDir)
outputFile = os.getcwd() + "/" + outputFile

if not os.path.isdir(inputDir):
    print("\"" + inputDir + "\" is not a directory!")
    sys.exit(2)

queue = sorted(os.listdir(inputDir))
os.chdir(inputDir)

pool = multiprocessing.Pool()
jobTable = pool.map(job, queue)
pool.close()
pool.join()

list_to_file(str("Entry\tStatus\n"), jobTable, outputFile)
