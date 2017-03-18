# -*- coding: utf-8 -*-
# !/usr/bin/python

import getopt
import sys
import re
import numpy


def usage():
    print("\nUsage: " + sys.argv[0] + " -i <file> -n <int> -p <regex>" + "\n\n" +
          "-i/--input <file> \tA text  file" + "\n" +
          "-n/--number <int> \tNumber of chunks to chop" + "\n" +
          "-p/--pattern <regex> \tA pattern or regular expression to split" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:n:p:", ["help", "input=", "number=", "pattern="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    n = None
    p = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-n", "--number"):
            n = str(arg)
        elif opt in ("-p", "--pattern"):
            p = str(arg)
    if not any(var is None for var in [i, n]):
        return i, n, p
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


def chop(string, number_of_chunks, pattern):
    number_of_chunks = int(number_of_chunks)
    if pattern is None:
        pattern = "\n"
    max_chunks = len(re.findall(pattern, string))
    if max_chunks < number_of_chunks:
        print("Cannot make " + str(number_of_chunks) + " chunks! \n" +
              "Will make " + str(max_chunks) + " chunks.")
        number_of_chunks = max_chunks
    list_to_join = list(filter(None, re.split("(" + str(pattern).decode(coding_python_version_check()) + ")", string)))
    output = []
    for numpy_array in numpy.array_split(numpy.array([i + j for i, j in zip(list_to_join[::2], list_to_join[1::2])]), int(number_of_chunks)):
        output.append(numpy_array.tolist())
    return output


def export_two_dimensional_array(array):
    chunk = 1
    for dim in array:
        list_to_file("", dim, str('.'.join(inputFile.split('.')[:-1]) + '_chunk_' + str(chunk) + '.' + inputFile.split('.')[-1]))
        chunk += 1


def list_to_file(header, list_to_write, file_to_write):
    header += "".join(str(i) for i in list_to_write if i if i is not None)
    file = open(file_to_write, 'w')
    file.write(header)
    file.close()


########################################################
inputFile, chunksNumber, inputPattern = main()
rawStrings = file_to_str(inputFile)
processedArray = chop(rawStrings, chunksNumber, inputPattern)
export_two_dimensional_array(processedArray)
