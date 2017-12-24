#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os


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
    import re
    file_buffer = open(file, 'rU')
    output_list = [j for j in [re.sub('[\r\n]', '', i) for i in file_buffer] if len(j) > 0]
    file_buffer.close()
    return output_list


if __name__ == '__main__':
    inputFileList, inputWordsFileOrLisList, ignoreCaseBool, reduceBool, negativeBool, outputFile = parse_namespace()
    if os.path.isfile(inputWordsFileOrLisList[0]):
        inputWordList = file_to_list(inputWordsFileOrLisList[0])
    else:
        inputWordList = inputWordsFileOrLisList.copy()
    outputBuffer = ""
    processedHeadersCounter = 0
    for inputFile in inputFileList:
        recordingBool = False
        inputFileWrapper = open(inputFile, 'rU')
        for inputFileRow in inputFileWrapper:
            if inputFileRow.startswith(">"):
                if (not negativeBool and ((not reduceBool and (any(i in inputFileRow for i in inputWordList) or (ignoreCaseBool and any(j.lower() in inputFileRow.lower() for j in inputWordList)))) or (reduceBool and (all(i in inputFileRow for i in inputWordList) or (ignoreCaseBool and all(j.lower() in inputFileRow.lower() for j in inputWordList)))))) \
                        or (negativeBool and not ((not reduceBool and (any(i in inputFileRow for i in inputWordList) or (ignoreCaseBool and any(j.lower() in inputFileRow.lower() for j in inputWordList)))) or (reduceBool and (all(i in inputFileRow for i in inputWordList) or (ignoreCaseBool and all(j.lower() in inputFileRow.lower() for j in inputWordList)))))):
                    recordingBool = True
                    processedHeadersCounter += 1
                else:
                    recordingBool = False
            if recordingBool:
                outputBuffer += re.sub('[\r\n]*', "", inputFileRow) + '\n'
        inputFileWrapper.close()
    outputBuffer = re.sub('[\n]+', '\n', outputBuffer)
    outputFileWrapper = open(outputFile, 'w')
    outputFileWrapper.write(outputBuffer)
    outputFileWrapper.close()
    print("At least one keyword from the list '" + "', '".join(inputWordList) + "' has been found in " + str(processedHeadersCounter) + " sequence headers for " + str(len(inputFileList)) + " file(s), check the file: '" + outputFile + "'")
