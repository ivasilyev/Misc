#!/usr/bin/python

import getopt
import multiprocessing
import sys
import sh
import re
import pandas


def usage():
    print("\nUsage: " + sys.argv[0] + " -i <file> -o <file>" + "\n\n" +
          "-i/--input <file> \tText file containing KEGG entries divided by line or semicolon" + "\n" +
          "-o/--output <file> \tFile to create" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    input_file = None
    output_file = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            input_file = str(arg)
        elif opt in ("-o", "--output"):
            output_file = str(arg)
    if (input_file is not None) and (output_file is not None):
        return input_file, output_file
    print("The parameters are not yet specified!")
    usage()


def file_to_str(file):
    file_parsed = open(file, 'rU').read()
    return file_parsed


def kegg_request(kegg_entry):
    return re.sub(' +', ' ', str(sh.curl("http://rest.kegg.jp/get/" + kegg_entry)).replace("\n", " ").replace("\t", " "))


def kegg_compound2enzymes(kegg_compound):
    try:
        re.match('C[0-9]{5}', kegg_compound).group(0)
    except AttributeError:
        return "unknown", "unknown"
    kegg_enzymes = re.findall('[0-9]*\.[0-9]*\.[0-9]*\.[0-9-]*', kegg_request(kegg_compound))
    try:
        kegg_name = re.search('NAME (.*) FORMULA', kegg_request(kegg_compound)).group(1).split("; ")
    except AttributeError:
        kegg_name = "unknown"
    return kegg_enzymes, kegg_name


def kegg_enzymes2orthologs(kegg_enzymes):
    if kegg_enzymes is "unknown":
        return "unknown"
    kegg_orthologs = []
    for kegg_enzyme in kegg_enzymes:
        if kegg_enzyme.endswith("-"):  # do not search the whole db section
            continue
        else:
            kegg_orthologs.extend(re.findall('(K[0-9]{5})', kegg_request(kegg_enzyme)))
    return kegg_orthologs


def kegg_compound2orthologs(kegg_compound_raw):
    kegg_enzymes_processed, kegg_names_processed = kegg_compound2enzymes(kegg_compound_raw)
    if kegg_enzymes_processed == "unknown":
        return str(kegg_compound_raw + "\t" + "unknown" + "\t" + "unknown" + "\t" + "unknown" + "\n")
    kegg_orthologs_processed = kegg_enzymes2orthologs(kegg_enzymes_processed)
    return str(kegg_compound_raw + "\t" + ", ".join(kegg_names_processed) + "\t" + " ".join(kegg_enzymes_processed) + "\t" + " ".join(kegg_orthologs_processed) + "\n")


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    file.close()


#######################################
keggInputFile, keggOutputFile = main()
rawEntries = file_to_str(keggInputFile)
keggCompounds = sorted(list(filter(None, pandas.unique(rawEntries.replace("\r", "\n").replace(";", "\n").split("\n")))))

keggTable = str("KEGG Compound\tSynonyms\tKEGG Enzymes\tKEGG Orthologs\n")
pool = multiprocessing.Pool()
pool_table = pool.map(kegg_compound2orthologs, keggCompounds)
pool.close()
pool.join()

keggTable += "".join(str(i) for i in pool_table if i is not None)
var_to_file(keggTable, keggOutputFile)
