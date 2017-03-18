# -*- coding: utf-8 -*-
# !/usr/bin/python

import getopt
import multiprocessing
import sys


def usage():
    print("\nUsage: " + sys.argv[0] + " -i <file> -d <symbol> -c <list>" + "\n\n" +
          "-i/--input <file> \tText table file" + "\n" +
          "-d/--delimiter <symbol> \tColumn delimiter without quotes" + "\n" +
          "-c/--columns <list> \tComma-separated zero-beginning list of columns to export" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:d:c:", ["help", "input=", "delimiter=", "columns="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    d = None
    c = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-d", "--delimiter"):
            d = str(arg)
        elif opt in ("-c", "--columns"):
            c = str(arg)
    if not any(var is None for var in [i, c]):
        return i, d, c
    print("The parameters are not yet specified!")
    usage()


def file_to_str(file):
    file_parsed = open(file, 'rU').read()
    return file_parsed


def coding_python_version_check():
    if sys.version_info >= (3, 3):
        return "unicode-escape"  # for python 3.3+ try "unicode-escape"
    else:
        return "string-escape"


def string_process(string, delimiter, column_list):
    string = string.replace('\n', '')
    if delimiter is None:
        delimiter = "\t"
    delimiter = delimiter.decode(coding_python_version_check())
    if string:  # is not empty
        columns = []
        for column in column_list.split(','):
            if column is not None:
                try:
                    columns.append(string.strip().split(delimiter)[int(column)])
                except IndexError:
                    print("The table string \"" + string + "\" does not contain the column with index " + column + "!")
        out = delimiter.join(str(i) for i in columns) + str('\n')
        return out


def string_process_wrapper(args):
    return string_process(*args)


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    file.close()


###############################################
inputFile, theDelimiter, columnsList = main()
inputTable = file_to_str(inputFile).split('\n')

core_jobs = [(string, theDelimiter, columnsList) for string in inputTable]
pool = multiprocessing.Pool()
pool_table = pool.map(string_process_wrapper, core_jobs)
pool.close()
pool.join()
outTable = "".join(str(string) for string in pool_table if string is not None)

var_to_file(outTable, str('.'.join(inputFile.split('.')[:-1]) + '_columns_' + str(columnsList) + '.' + inputFile.split('.')[-1]))
