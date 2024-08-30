#!/usr/bin/python

import getopt
import multiprocessing
import sys
import sh
import re
import pandas


def usage():
    print("\nUsage: " + sys.argv[0] + " -i <file> -o <file>" + "\n\n" +
          "-i/--input <file> \tText file containing KEGG entries one per line" + "\n" +
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


def is_kegg_entry(string):
    try:
        re.search("K[\d]+", string).group(0)
        return True
    except AttributeError:
        return False


def kegg_db_splitter(kegg_db_id, kegg_response):
    try:
        kegg_db_content = re.search(str(kegg_db_id + " (.*)"), kegg_response).group(1)
    except:
        kegg_db_content = "unknown"
    cutoff = kegg_response.replace(str(kegg_db_id + " " + kegg_db_content), "")
    return kegg_db_content, cutoff


def kegg_response_parser(kegg_entry):
    kegg_response = re.sub(' +', ' ', str(sh.curl("http://rest.kegg.jp/get/" + kegg_entry)).replace("\n", "").replace("\t", " "))
    # Note the DB IDs go from bottom to top of the page
    kegg_genes, cutoff = kegg_db_splitter("GENES", kegg_response)
    kegg_dblinks, cutoff = kegg_db_splitter("DBLINKS", cutoff)
    kegg_brite, cutoff = kegg_db_splitter("BRITE", cutoff)
    kegg_disease, cutoff = kegg_db_splitter("DISEASE", cutoff)
    kegg_module, cutoff = kegg_db_splitter("MODULE", cutoff)
    kegg_pathway, cutoff = kegg_db_splitter("PATHWAY", cutoff)
    kegg_definition, cutoff = kegg_db_splitter("DEFINITION", cutoff)
    kegg_name, cutoff = kegg_db_splitter("NAME", cutoff)
    kegg_string = str(kegg_entry + "\t" +
                      kegg_name + "\t" +
                      kegg_definition + "\t" +
                      kegg_pathway + "\t" +
                      kegg_module + "\t" +
                      kegg_disease + "\t" +
                      kegg_brite + "\t" +
                      kegg_dblinks + "\t" +
                      kegg_genes + "\n").replace("///", "")  # Now it's the very bottom
    return kegg_string


def core_job(input_string):
    if is_kegg_entry(input_string):
        print("Processing: " + re.search("\w*", input_string).group(0))
        return kegg_response_parser(input_string)


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    file.close()


######################################
keggListPath, keggParsedFile = main()
rawEntries = file_to_str(keggListPath)
parsedEntries = sorted(pandas.unique(rawEntries.replace(";", "\n").split("\n")))

keggTable = str("ENTRY\tNAME\tDEFINITION\tPATHWAY\tMODULE\tDISEASE\tBRITE\tDBLINKS\tGENES\n")

pool = multiprocessing.Pool()
pool_table = pool.map(core_job, parsedEntries)
pool.close()
pool.join()

keggTable += "".join(str(i) for i in pool_table if i is not None)
var_to_file(keggTable, keggParsedFile)
