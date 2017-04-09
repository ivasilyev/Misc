#!/usr/bin/python

import os
import re
import sys
import getopt
import multiprocessing
import subprocess


def usage():
    print("\nUsage: " + sys.argv[0] + " -i <file> -s <int> -t <int> -o <dir>" + "\n\n" +
          "-i/--input <file> \tReference nucleotide FASTA" + "\n" +
          "-s/--size <int> \tChunk size, Gb, 2 by default" + "\n"
          "-t/--threads <int> \tNumber of the CPU cores to use, maximal by default" + "\n"
          "-o/--output <dir> \tDirectory to keep results" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:s:t:o:", ["help", "input=", "size=", "threads=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    s = 2
    t = int(multiprocessing.cpu_count())
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-s", "--size"):
            s = int(arg)
        elif opt in ("-t", "--threads"):
            t = int(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, s, t, o]):
        return i, s * 10 ** 9, t, o  # looks better than 2**30
    print("The parameters are not yet specified!")
    usage()


def file_to_str(file):
    file_parsed = open(file, "rU").read()
    return file_parsed


def file_append(string, file_to_append):
    file = open(file_to_append, "a+")
    file.write(string)
    file.close()


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


def filename_only(string):
    return str(".".join(string.rsplit("/", 1)[-1].split(".")[:-1]))


def string_chop(input_file, number_of_chunks):
    string = file_to_str(input_file)
    list_to_join = list(filter(None, re.split(">", string)))
    chunks_length = int(len(list_to_join) / number_of_chunks)
    if sys.version_info >= (3, 0):
        chunks_list = [list_to_join[i:i + chunks_length] for i in range(0, len(list_to_join), chunks_length)]
    else:
        chunks_list = [list_to_join[i:i + chunks_length] for i in xrange(0, len(list_to_join), chunks_length)]
    chunk_names = []
    chunk_index = 1
    for strings_list in chunks_list:
        list_to_fasta(list(map(lambda x: ">" + x, strings_list)), outputDir + filename_only(inputFile) + "_chunk_" + str(chunk_index) + "." + inputFile.split(".")[-1])
        chunk_names.append(outputDir + filename_only(inputFile) + "_chunk_" + str(chunk_index) + "." + inputFile.split(".")[-1])
        chunk_index += 1
    return chunk_names


def list_to_fasta(list_to_write, file_to_write):
    file = open(file_to_write, "w")
    file.write("".join(str(i) for i in list_to_write if i if i is not None))
    file.close()


def string_process(string):
    string = string.replace("\r", "").replace("\n", "")
    if string:
        columns = []
        for column in [0, 1]:
            if column is not None:
                try:
                    columns.append(string.strip().split("\t")[column])
                except IndexError:
                    print("The table string \"" + string + "\" does not contain the column with index " + str(column) + "!")
        out = "\t".join(str(i) for i in columns) + str("\n")
        return out


def multi_core_queue(function):
    pool = multiprocessing.Pool(threadsNumber)
    pool.map(function, chunks)
    pool.close()
    pool.join()


def external_route(input_direction, output_direction):
    cmd = input_direction.split(" ")
    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output, error) = process.communicate()
    file_append(output.decode("utf-8"), output_direction)
    process.wait()


# Main workflow

def bowtie_build(chunk):
    external_route("bowtie-build -C " + chunk + " " + outputDir + filename_only(chunk) + "_colorspace",
                   outputDir + filename_only(chunk) + "_bowtie-build.log")


def bowtie2_build(chunk):
    external_route("bowtie2-build " + chunk + " " + outputDir + filename_only(chunk) + "_bowtie2",
                   outputDir + filename_only(chunk) + "_bowtie2-build.log")


def samtools_faidx(chunk):
    external_route("samtools faidx " + chunk,
                   outputDir + filename_only(chunk) + "_samtools_faidx.log")
    os.rename(chunk + ".fai", outputDir + filename_only(chunk) + "_samtools.fai")


def fai2genome(chunk):
    strings = list(filter(None, file_to_str(outputDir + filename_only(chunk) + "_samtools.fai").replace("\r", "\n").split("\n")))
    strings_processed = []
    for string in strings:
        strings_processed.append(string_process(string))
    output = "".join(str(i) for i in strings_processed if i is not None)
    file_append(output, outputDir + filename_only(chunk) + "_samtools.genome")
    if not os.path.isfile(outputDir + filename_only(chunk) + "_annotation.txt"):
        file_append("Gene_name\tGene_length\n", outputDir + filename_only(chunk) + "_annotation.txt")
    file_append(output, outputDir + filename_only(inputFile) + "_annotation.txt")


########################################################
inputFile, chunkSize, threadsNumber, outputDir = main()

is_path_exists(outputDir)
outputDir = ends_with_slash(outputDir)

if os.path.getsize(inputFile) > chunkSize:
    chunks = string_chop(inputFile, int(os.path.getsize(inputFile) / chunkSize))
else:
    chunks = [inputFile]

multi_core_queue(bowtie_build)
multi_core_queue(bowtie2_build)
multi_core_queue(samtools_faidx)
multi_core_queue(fai2genome)

if len(chunks) == 1:
    from shutil import copyfile
    copyfile(inputFile, outputDir + filename_only(inputFile) + "." + inputFile.split(".")[-1])

print("COMPLETED")
