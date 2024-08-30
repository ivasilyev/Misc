#!/usr/bin/python

import sh
import sys
import getopt


def usage():
    print("Usage: " + sys.argv[0] + " -i <file> -k <str> -o <file>" + "\n\n" +
          "-i/--input <file> \tA table with a header to be filtered" + "\n" +
          "-k/--keyword <str> \tA keyword to filter" + "\n" +
          "-o/--output <file> \tFile to keep results" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:k:o:", ["help", "input=", "keyword=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    k = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-k", "--keyword"):
            k = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, k, o]):
        return i, k, o
    print("The parameters are not yet specified!")
    usage()


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    file.close()


###################################################
inputFile, inputKeyWord, outputFile = main()
output = str(sh.head("-n 1", inputFile)) + str(sh.grep(inputKeyWord, inputFile))
var_to_file(output, outputFile)
