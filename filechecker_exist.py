# -*- coding: utf-8 -*-
# !/usr/bin/python

import os
import sys
import getopt
import re


def usage():
    print("Usage: " + sys.argv[0] + " -a <str> -b <str> -z <regexp> -y <regexp> -o <str>" + "\n\n" +
          "-a/--item1 <str> \t\tFirst file or folder" + "\n" +
          "-b/--item2 <str> \t\tSecond file or folder" + "\n" +
          "-z/--perl1 <regexp> \t\tRegular expression to search in each filename of the first file" + "\n" +
          "-y/--perl2 <regexp> \t\tRegular expression to search in each filename of the second file" + "\n" +
          "-o/--output <str> \t\tMask to name output files" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:b:z:y:o:", ["help", "item1=", "item2=", "perl1=", "perl2=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    a = None
    b = None
    z = None
    y = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-a", "--item1"):
            a = str(arg)
        elif opt in ("-b", "--item2"):
            b = str(arg)
        elif opt in ("-z", "--perl1"):
            z = str(arg)
        elif opt in ("-y", "--perl2"):
            y = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [a, b, z, y, o]):
        return a, b, z, y, o
    print("The parameters are not yet specified!")
    usage()


def get_file_list(directory):
    file_list = []
    for file_name in sorted(os.listdir(directory)):
        file_list.append(file_name)
    return sorted(file_list)


def file_to_list(file):
    file_parsed = open(file, 'rU')
    file_list = []
    for file_name in file_parsed:
        file_list.append(file_name.replace("\n", ""))
    return sorted(file_list)


def parse_some(file_or_dir):
    if os.path.isdir(file_or_dir):
        return get_file_list(file_or_dir)
    return file_to_list(file_or_dir)


def strings_process(str_list, regexp):
    processed_list = []
    for processing_str in str_list:
        try:
            processed_list.append(re.search(regexp, processing_str).group(1))
        except (AttributeError, IndexError) as exception:
            processed_list.append(processing_str)
    return processed_list


def compare_lists(list_to_check, main_list, check_regexp):
    comparison_table = "Entry\tStatus\n"
    for raw_string in list_to_check:
        try:
            string_to_check = re.search(check_regexp, raw_string).group(1)
        except (AttributeError, IndexError) as exception:
            string_to_check = raw_string
        if any(string_to_check in i for i in main_list):
            comparison_table += str(raw_string + "\tOK\n")
        else:
            comparison_table += str(raw_string + "\tMISSING\n")
    return comparison_table


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    file.close()


######################################################
object1, object2, regexp1, regexp2, outputMask = main()

list1 = parse_some(object1)
list2 = parse_some(object2)

straight_comparison = compare_lists(list1, list2, regexp1)
reversed_comparison = compare_lists(list2, list1, regexp2)

var_to_file(straight_comparison, str(outputMask + "_straight.txt"))
var_to_file(reversed_comparison, str(outputMask + "_reversed.txt"))
