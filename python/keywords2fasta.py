#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import subprocess
import multiprocessing


def parse_args():
    starting_parser = argparse.ArgumentParser(description="The script performs a per-header keyword search in one or many FASTA files")
    starting_parser.add_argument("-f", "--fasta", required=True, nargs='+',
                                 help="FASTA file(s)")
    starting_parser.add_argument("-k", "--keyword", required=True, nargs='+',
                                 help="Keyword(s) to search or containing file")
    starting_parser.add_argument("-i", "--ignore_case", default=False, action='store_true',
                                 help="Performs a case insensitive search")
    starting_parser.add_argument("-r", "--reducing", default=False, action='store_true',
                                 help="Performs a search for simultaneous multiple keywords content")
    starting_parser.add_argument("-n", "--negative", default=False, action='store_true',
                                 help="If selected, only headers without the keyword would be found")
    starting_parser.add_argument("-o", "--output", default=None,
                                 help="(Optional) Output file, using the first given file name by default")
    return starting_parser.parse_args()


def parse_namespace():
    namespace = parse_args()
    if not namespace.output:
        namespace.output = namespace.fasta[0] + "_" + namespace.keyword[0] + ".fasta"
    return namespace.fasta, namespace.keyword, namespace.ignore_case, namespace.reducing, namespace.negative, namespace.output


def file_to_list(file):
    file_buffer = open(file, 'rU')
    output_list = [j for j in [re.sub('[\r\n]', '', i) for i in file_buffer] if len(j) > 0]
    file_buffer.close()
    return output_list


def multi_core_queue(function_to_parallelize, queue):
    pool = multiprocessing.Pool()
    output = pool.map(function_to_parallelize, queue)
    pool.close()
    pool.join()
    return output


def process_string(input_string):
    return re.sub('[\r\n]+', "", input_string) + '\n'


def mp_keyword2fasta(keyword):
    recording_bool = False
    file_wrapper = open(inputFile, "rU")
    output_buffer = ""
    for line in file_wrapper:
        # Did I provided enough boolean variables?
        if line.startswith(">"):
            if (not negativeBool and ((keyword in line) or (ignoreCaseBool and keyword.lower() in line.lower()))) or (negativeBool and not ((keyword in line) or (ignoreCaseBool and keyword.lower() in line.lower()))):
                recording_bool = True
                global processedHeadersCounter
                processedHeadersCounter += 1
            else:
                recording_bool = False
        if recording_bool:
            output_buffer += process_string(line)
    file_wrapper.close()
    return output_buffer


def mp_reducing_keyword2fasta(file_name):
    file_rows_list = file_to_list(file_name)
    recording_bool = False
    output_buffer = ""
    for line in file_rows_list:
        if line.startswith(">"):
            if (not negativeBool and (all(i in line for i in inputWordsList) or (ignoreCaseBool and all(i.lower() in line.lower() for i in inputWordsList)))) or (negativeBool and not (all(i in line for i in inputWordsList) or (ignoreCaseBool and all(i.lower() in line.lower() for i in inputWordsList)))):
                recording_bool = True
                global processedHeadersCounter
                processedHeadersCounter += 1
            else:
                recording_bool = False
        if recording_bool:
            output_buffer += process_string(line)
    return output_buffer


def index_sequence_headers(file_name):
    output_dict = {}
    file_wrapper = open(file_name, 'rU')
    recording_header = None
    for line in file_wrapper:
        if line.startswith(">"):
            recording_header = process_string(line)
            output_dict[recording_header] = ""
        elif recording_header:
            output_dict[recording_header] += process_string(line)
    file_wrapper.close()
    return output_dict


def mp_get_matching_sequences(key):
    # Looks like the grep's Boyer–Moore string search algorithm works much faster than the pythonic-only implementation
    matching_headers_list = [process_string(i) for i in subprocess.getoutput("grep -F " + key + " " + inputFile).split("\n") if len(i) > 0]
    try:
        return "".join([i + inputFileDict[i] for i in matching_headers_list])
    except KeyError:
        return ""


if __name__ == '__main__':
    inputFilesList, inputWordsFileOrLisList, ignoreCaseBool, reduceBool, negativeBool, outputFile = parse_namespace()
    if os.path.isfile(inputWordsFileOrLisList[0]):
        inputWordsList = file_to_list(inputWordsFileOrLisList[0])
    else:
        inputWordsList = inputWordsFileOrLisList.copy()
    processedHeadersCounter = 0
    if reduceBool:
        outputBuffer = multi_core_queue(mp_reducing_keyword2fasta, inputFilesList)
    else:
        outputBuffer = []
        for inputFile in inputFilesList:
            inputFileDict = index_sequence_headers(inputFile)
            outputBuffer += multi_core_queue(mp_get_matching_sequences, inputWordsList)
    outputFileWrapper = open(outputFile, 'w')
    outputFileWrapper.write("".join(outputBuffer))
    outputFileWrapper.close()
    print("At least one keyword from the list has been found in " + str(processedHeadersCounter) + " sequence headers for " + str(len(inputFilesList)) + " file(s), check the file: '" + outputFile + "'. \nProvided keywords list: \n" + "\n".join(inputWordsList))
