# -*- coding: utf-8 -*-
# !/usr/bin/python

# This script will perform single alignment & postprocessing for every *.csfasta file specified in input file list.
# Paths should be ending at "/". No spaces are allowed.
# It is recommended to use launch command "nohup python SingleBee_mp.py -i fun.txt -d nova -o nova_out > /dev/null 2>&1 & echo $! > run.pid" due to possibly keyboard-caused interruptions.

# [SoftwarePaths]
bowtiePath = "/data/apps/bin/"
samtoolsPath = "/data/apps/bin/"
bedtoolsPath = "/data/apps/bin/"

# [SequencesPaths]
referenceBwtMask = "/data1/bio/kazan_solid_metagenome_data/Malanin/bwt"
referenceFai = "/data1/bio/kazan_solid_metagenome_data/Malanin/nucleotide_fasta_protein_homolog_model.fasta.fai"
referenceGenomeLengths = "/data1/bio/kazan_solid_metagenome_data/Malanin/nucleotide_fasta_protein_homolog_model.fasta.genome"
referenceGenomeTags = "/data1/bio/kazan_solid_metagenome_data/Malanin/annotation.txt"

# [Script begin]
import os
import multiprocessing
import subprocess
import getopt
import sys


def usage():
    print("\nUsage: " + sys.argv[0] + " -i <file> -d <dir> -o <str>" + "\n\n" +
          "-i/--input <file> \tList of *.csfasta files" + "\n" +
          "-d/--directory <dir> \tDirectory to keep results" + "\n"
          "-o/--output <str> \tMask to be added to the resulting files" + "\n")
    sys.exit(2)


def main():
    opts = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:d:o:", ["help", "input=", "directory=", "output="])
    except getopt.GetoptError as arg_err:
        print(str(arg_err))
        usage()
    i = None
    d = None
    o = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--input"):
            i = str(arg)
        elif opt in ("-d", "--directory"):
            d = str(arg)
        elif opt in ("-o", "--output"):
            o = str(arg)
    if not any(var is None for var in [i, d, o]):
        return i, d, o
    print("The parameters are not yet specified!")
    usage()


def file_to_list(file):
    file_parsed = open(file, 'rU')
    file_list = []
    for file_name in file_parsed:
        file_list.append(file_name.replace("\n", ""))
    return sorted(file_list)


def file_append(string, file_to_append):
    file = open(file_to_append, 'a+')
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

# Wrappers


def single_core_queue(function):
    for csfastaPath in sorted(csfastaPaths):
        function(csfastaPath)


def multi_core_queue(function):
    pool = multiprocessing.Pool()
    pool.map(function, csfastaPaths)
    pool.close()
    pool.join()


def external_route(input_direction, output_direction):
    cmd = input_direction.split(" ")
    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for stdout_line in iter(process.stdout.readline, ""):
        file_append(stdout_line, output_direction)
    process.wait()

# Main workflow


def bowtie_it(csfasta_file_path):
    csfasta_file_name = str(csfasta_file_path.rsplit('/', 1)[-1]).replace(".csfasta", "")
    external_route(str(bowtiePath + "bowtie -f -C -S -t -v 3 -k 1 --threads 20 --un Non-mapped_reads/" + csfasta_file_name + "_no_" + outputMask + ".csfasta " + referenceBwtMask + " " + csfasta_file_path + " Mapped_reads/" + csfasta_file_name + "_" + outputMask + ".sam"),
                   str("Statistics/" + csfasta_file_name + "_" + outputMask + "_bowtie.log"))


def sam2bam(csfasta_file_path):
    csfasta_file_name = str(csfasta_file_path.rsplit('/', 1)[-1]).replace(".csfasta", "")
    external_route(str(samtoolsPath + "samtools import " + referenceFai + " Mapped_reads/" + csfasta_file_name + "_" + outputMask + ".sam Mapped_reads/" + csfasta_file_name + "_" + outputMask + ".bam"),
                   str("Statistics/" + csfasta_file_name + "_" + outputMask + "_sam2bam.log"))


def sort_bam(csfasta_file_path):
    csfasta_file_name = str(csfasta_file_path.rsplit('/', 1)[-1]).replace(".csfasta", "")
    external_route(str(samtoolsPath + "samtools sort Mapped_reads/" + csfasta_file_name + "_" + outputMask + ".bam Mapped_reads/" + csfasta_file_name + "_" + outputMask + ".sorted"),
                   str("Statistics/" + csfasta_file_name + "_" + outputMask + "_sort_bam.log"))


def bam2coverage(csfasta_file_path):
    csfasta_file_name = str(csfasta_file_path.rsplit('/', 1)[-1]).replace(".csfasta", "")
    external_route(str(bedtoolsPath + "genomeCoverageBed -ibam Mapped_reads/" + csfasta_file_name + "_" + outputMask + ".sorted.bam -g " + referenceGenomeLengths),
                   str("Statistics/" + csfasta_file_name + "_" + outputMask + "_genomeCoverageBed.txt"))


def coverage_extract(csfasta_file_path):
    csfasta_file_name = str(csfasta_file_path.rsplit('/', 1)[-1]).replace(".csfasta", "")
    list_bp_cov = dict()
    list_pos_cov = dict()
    # get all sequences names
    h_file_bedtools_genome = open(referenceGenomeLengths, 'rU')
    for pline in h_file_bedtools_genome:
        words = pline.split()
        list_bp_cov[words[0]] = 0
        list_pos_cov[words[0]] = 0
    # get coverages for seqs
    h_file_cov_hist = open(str("Statistics/" + csfasta_file_name + "_" + outputMask + "_genomeCoverageBed.txt"), 'rU')
    for pline in h_file_cov_hist:
        words = pline.split()
        if words[0] != 'genome':  # special reserved word of bedtools (for summary coverage)
            list_bp_cov[words[0]] += (int(words[1]) * int(words[2]))
            if words[1] != '0':
                list_pos_cov[words[0]] += int(words[2])
    h_file_out_bp_cov = open(str("Statistics/" + csfasta_file_name + "_" + outputMask + "_bp_coverage.txt"), 'w')
    # zero-covered seqs are omitted in histogram!
    # so fill the lacking and output
    for key in sorted(list_bp_cov.keys()):
        h_file_out_bp_cov.write(key + '\t' + str(list_bp_cov[key]) + '\n')
    h_file_out_bp_cov.close()
    # get pos coverage
    h_file_out_pos_cov = open(str("Statistics/" + csfasta_file_name + "_" + outputMask + "_pos_coverage.txt"), 'w')
    for key in sorted(list_pos_cov.keys()):
        h_file_out_pos_cov.write(key + '\t' + str(list_pos_cov[key]) + '\n')
    h_file_out_pos_cov.close()


##############################################
inputPathsList, outputDir, outputMask = main()
csfastaPaths = file_to_list(inputPathsList)

is_path_exists(outputDir)
os.chdir(outputDir)
file_append(str(os.getpid()), str(os.getpid()) + ".pid")

for newDir in ["Non-mapped_reads", "Mapped_reads", "Statistics"]:
    is_path_exists(newDir)

for pathVar in [bowtiePath, samtoolsPath, bedtoolsPath]:
    pathVar = ends_with_slash(pathVar)

single_core_queue(bowtie_it)
multi_core_queue(sam2bam)
multi_core_queue(sort_bam)
multi_core_queue(bam2coverage)
multi_core_queue(coverage_extract)
