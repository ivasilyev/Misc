#!/usr/bin/python

import sys
import getopt
import multiprocessing
import pandas


def usage():
    print("Usage: " + sys.argv[0] + " -i <table> -c <list> -o <file>" + "\n\n" +
          "-i/--input <table> \tA table without a header containing two tab-delimited columns: sample name and absolute path" + "\n" +
          "-c/--colnumbers <list> \tComma-delimited zero-based list of columns to sum" + "\n" +
          "-o/--output <file> \tFile to keep results" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c:o:", ["help", "input=", "colnumbers=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    c = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-c", "--colnumbers"):
            c = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, c, o]):
        return i, c, o
    print("The parameters are not yet specified!")
    usage()


def file_to_str(file):
    file_parsed = open(file, 'rU').read()
    return file_parsed


def file_append(string, file_to_append):
    file = open(file_to_append, 'a+')
    file.write(string)
    file.close()


def sample2dataframe(string):
    if string:
        sample_name, sample_file = string.split("\t")
        sample_list = pandas.read_table(sample_file, sep='\t', header=None)[sumColumns].sum().values.tolist()
        file_append(str(sample_name + "\t" + "\t".join(str(i) for i in sample_list if i is not None) + "\n"), outputFile)


def multi_core_queue(function, queue):
    pool = multiprocessing.Pool()
    pool.map(function, queue)
    pool.close()
    pool.join()


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    file.close()


###############################
inputFile, inputColumns, outputFile = main()

sumColumns = []
for inputColumn in inputColumns.split(","):
    if inputColumn is not None:
        try:
            sumColumns.append(int(inputColumn))
        except ValueError:
            print("\"" + inputColumn + "\" is not an integer!")
            usage()

inputStrings = file_to_str(inputFile).split("\n")
multi_core_queue(sample2dataframe, inputStrings)
