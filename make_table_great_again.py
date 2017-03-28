# -*- coding: utf-8 -*-
# !/usr/bin/python

# The tag file must contain a header with "Gene_name" column.
# Other files must not contain a header and have only two columns.

import os
import sys
import getopt
import pandas


def usage():
    print("Usage: " + sys.argv[0] + " -i <file> -t <file> -c <str> -o <dir>" + "\n\n" +
          "-i/--input <file> \t\"Small\" table without a header containing two tab-delimited columns: sample name and absolute path" + "\n" +
          "-t/--tags <file> \t\"Big\" table with a header containing all required tab-delimited columns to merge" + "\n" +
          "-c/--colname <str> \tIndexing column containing same data for both tables" + "\n" +
          "-o/--output <dir> \tDirectory to keep results" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:t:c:o:", ["help", "input=", "tags=", "colname=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    t = None
    c = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-t", "--tags"):
            t = str(arg)
        elif opt in ("-c", "--colname"):
            c = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, t, c, o]):
        return i, t, c, o
    print("The parameters are not yet specified!")
    usage()


def is_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        print(exception)


def ends_with_slash(string):
    if string.endswith("/"):
        return string
    else:
        return str(string + "/")


###################################################
inputFile, tagFile, mergeColumn, outputDir = main()
is_path_exists(outputDir)
inputDF = pandas.read_table(inputFile, sep='\t', header=None)
mainDF = pandas.read_table(tagFile, sep='\t', header=0, engine='python')

resultCollectionTable = mainDF.copy()

sampleNames = []
for sampleName, samplePath in zip(inputDF[0].values.tolist(), inputDF[1].values.tolist()):
    sampleTable = pandas.read_table(samplePath, sep='\t', header='infer', names=[mergeColumn, sampleName], engine='python')
    resultCollectionTable = pandas.merge(resultCollectionTable, sampleTable, on=mergeColumn, how='left')
    sampleNames.append(sampleName)

resultCollectionTable.to_csv(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_raw_data.txt"), sep='\t', index=False)

sampleColNames = [mergeColumn] + list(sampleNames)
sampleDF = resultCollectionTable[sampleColNames].copy().set_index(mergeColumn)
sampleDF.columns.name = "Sample"
sampleDF = sampleDF.stack()
sampleDF.name = "Value"
sampleDF = sampleDF.reset_index()
sampleDF = sampleDF.groupby(['Sample', mergeColumn]).agg({"Value": 'sum'})
sampleDF = sampleDF.loc[(sampleDF != 0).any(1)]
sampleDF["Percentage"] = sampleDF.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
sampleDF = sampleDF.reset_index()

sampleDF.pivot(mergeColumn, "Sample", "Percentage").fillna(0).reset_index().to_csv(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_percentage.txt"), sep='\t', index=False)
