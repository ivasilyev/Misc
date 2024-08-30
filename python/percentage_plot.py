#!/usr/bin/python

# The coverage data file must contain a header with the specified column.
# Other files must not contain a header and have only two columns.

import os
import sys
import getopt
import pandas
import matplotlib
import seaborn


def usage():
    print("Usage: " + sys.argv[0] + " -i <table> -t <table> -s <file> -c <str> -o <dir>" + "\n\n" +
          "-i/--input <file> \t\"Small\" table without a header containing two tab-delimited columns: sample name and absolute path" + "\n" +
          "-t/--tags <file> \t\"Big\" table with a header containing all required data" + "\n" +
          "-s/--sums <file> \tAn optional able containing tab-delimited sample name and pre-counted sum values for percentage count" + "\n" +
          "-c/--colname <str> \tIndexing column containing same data for both input tables" + "\n" +
          "-o/--output <dir> \tDirectory to keep results" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:t:s:c:o:", ["help", "input=", "tags=", "sums=", "colname=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    t = None
    s = None
    c = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-t", "--tags"):
            t = str(arg)
        elif opt in ("-s", "--sums"):
            s = str(arg)
        elif opt in ("-c", "--colname"):
            c = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, t, c, o]):
        return i, t, s, c, o
    print("The parameters are not yet specified!")
    usage()


def ends_with_slash(string):
    if string.endswith("/"):
        return string
    else:
        return str(string + "/")


def is_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        print(exception)


###################################################
inputFile, inputTable, inputSums, mergeColumn, outputDir = main()

sampleNames = list(pandas.read_table(inputFile, sep='\t', header=None)[0].values.tolist())
resultCollectionTable = pandas.read_table(inputTable, sep='\t', header=0, engine='python')

sampleColNames = [mergeColumn] + sampleNames
sampleDF = resultCollectionTable[sampleColNames].copy().set_index(mergeColumn)
sampleDF.columns.name = "Sample"
sampleDF = sampleDF.stack()
sampleDF.name = "Value"
sampleDF = sampleDF.reset_index()
sampleDF = sampleDF.groupby(['Sample', mergeColumn]).agg({"Value": 'sum'})
sampleDF = sampleDF.loc[(sampleDF != 0).any(1)]

meanDF = sampleDF.reset_index().pivot("Sample", mergeColumn, "Value").mean()
meanDF.name = "Mean"
meanDF = meanDF.reset_index().set_index(mergeColumn)
meanDF["Median"] = sampleDF.reset_index().pivot("Sample", mergeColumn, "Value").median()
meanDF["SD"] = sampleDF.reset_index().pivot("Sample", mergeColumn, "Value").std()
meanDF["Variance"] = sampleDF.reset_index().pivot("Sample", mergeColumn, "Value").var()

totalDF = pandas.Series({"Mean" : sampleDF["Value"].mean(), "Median" : sampleDF["Value"].median(), "SD" : sampleDF["Value"].std(), "Variance" : sampleDF["Value"].var()})
totalDF.name = ""

if inputSums is not None:
    sumDF = pandas.read_table(inputSums, sep='\t', header=None)
    sumDF.rename(columns={0: "Sample", 1: "Sum"}, inplace=True)
    sumDF = sumDF.set_index("Sample")
else:
    sumDF = sampleDF.reset_index().pivot(mergeColumn, "Sample", "Value").sum()
    sumDF.name = "Sum"
    sumDF = sumDF.reset_index().set_index("Sample")

sampleDF["Percentage"] = sampleDF["Value"].apply(lambda x: x * 100) / sumDF["Sum"]
sampleDF = sampleDF.reset_index()

# Dataframe export

is_path_exists(outputDir)
sampleDF.pivot(mergeColumn, "Sample", "Percentage").fillna(0).reset_index().to_csv(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_percentage.txt"), sep='\t', index=False)
sampleDF.pivot(mergeColumn, "Sample", "Value").fillna(0).reset_index().to_csv(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_raw_data.txt"), sep='\t', index=False)
meanDF.fillna(0).reset_index().to_csv(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_samples_stat.txt"), sep='\t', index=False)
totalDF.fillna(0).reset_index().to_csv(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_global_stat.txt"), sep='\t', index=False, header=False)

# Dataframe visualization

seaborn.set(font_scale=.05)
fig, ax = matplotlib.pyplot.subplots(1, 1)
cbar_ax = fig.add_axes([.915, .3, .005, .25])
fig.set_size_inches(18.5, 10.5)
seaborn.heatmap(sampleDF.pivot("Sample", mergeColumn, "Value"), ax=ax, cbar_ax=cbar_ax, cbar=True, fmt="d", linewidths=.005)
fig.savefig(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_raw_data.png"), dpi=600)
matplotlib.pyplot.close()

fig, ax = matplotlib.pyplot.subplots(1, 1)
cbar_ax = fig.add_axes([.915, .25, .005, .25])
fig.set_size_inches(18.5, 10.5)
seaborn.heatmap(sampleDF.pivot("Sample", mergeColumn, "Percentage"), ax=ax, cbar_ax=cbar_ax, cbar=True, fmt="d", linewidths=.005)
fig.savefig(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_percentage.png"), dpi=600)
matplotlib.pyplot.close()

seaborn.factorplot(data=sampleDF, x=mergeColumn, y="Value", kind="bar", palette="muted").despine(left=True).set_xticklabels(rotation=90)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig(str(ends_with_slash(outputDir) + '.'.join(inputFile.rsplit('/', 1)[-1].split('.')[:-1]) + "_merged_by_" + mergeColumn + "_barplot.png"), dpi=600)
matplotlib.pyplot.close()
