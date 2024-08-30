#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import pandas as pd
import numpy as np
import timeit


def parse_args():
    starting_parser = argparse.ArgumentParser(description="This script converts Thermo Fisher Affymetrix™ output data into single PED file")
    starting_parser.add_argument("-a", "--afm", required=True, nargs='+',
                                 help="Affymetrix™ output file(s)")
    starting_parser.add_argument("-p", "--ped",
                                 help="(Optional) Tab-delimited PED file without a header containing 6 columns to join genotypes data. If not presented, it will be filled with the default values ('Sample Name', 'Sample Name', '0', '0', '2', '0')")
    starting_parser.add_argument("-s", "--sampledata",
                                 help="(Optional) Tab-delimited table without a header containing two columns: generic sample names and the corresponding column names from Affymetrix™ output file(s). Note: if specified, only the described samples shall be analyzed with generic names prioritized")
    starting_parser.add_argument("-o", "--output",
                                 help="(Optional) Output file, using input file(s) mask as default")
    return starting_parser.parse_args()


def parse_namespace():
    namespace = parse_args()
    if not namespace.output:
        namespace.output = os.path.abspath(str(namespace.afm[0])).rsplit("/", 1)[0] + '/' + '_'.join(j for j in [str(".".join(i.rsplit("/", 1)[-1].split(".")[:-1])) for i in namespace.afm]) + "_with_genotypes.ped"
    return namespace.afm, namespace.ped, namespace.sampledata, namespace.output


def afm2df(files_list):
    output_df = pd.DataFrame()
    for file_name in files_list:
        file_wrapper = open(file_name, 'rU')
        single_df_buffer = []
        for file_line in file_wrapper:
            if not file_line.startswith('#'):
                single_df_buffer.append(re.sub('[\n\r]', '', file_line).split('\t'))
        file_wrapper.close()
        single_df = pd.DataFrame(data=single_df_buffer[1:], columns=single_df_buffer[0])
        single_df.dbSNP_RS_ID = single_df.dbSNP_RS_ID.replace('', np.nan).combine_first(single_df.Extended_RSID.replace('', np.nan))
        single_df = single_df[single_df.dbSNP_RS_ID.notnull()]
        if len(output_df) < 2:
            output_df = single_df.copy()
        else:
            output_df = pd.merge(output_df, single_df, on='probeset_id', how='left')
    if len(files_list) > 1:
        output_df.rename(columns={[k for k in list(output_df) if 'dbSNP_RS_ID' in k][0]: 'dbSNP_RS_ID', [l for l in list(output_df) if 'Extended_RSID' in l][0]: 'Extended_RSID'}, inplace=True)
    sample_names_list = [j for j in list(output_df) if not any(i in j for i in ['probeset_id', 'dbSNP_RS_ID', 'Extended_RSID', 'BestandRecommended', 'CR', 'FLD'])]
    return output_df.loc[:, ['dbSNP_RS_ID'] + sample_names_list].fillna('---'), sample_names_list


def rename_afm_df(source_df):
    rename_df = pd.read_table(sampleDataFile, sep='\t', header='infer', names=['new_names', 'old_names'], engine='python')
    source_df.rename(columns=rename_df.set_index('old_names')['new_names'], inplace=True)
    return source_df.reset_index().loc[:, ['dbSNP_RS_ID'] + rename_df.loc[:, 'new_names'].values.tolist()], rename_df.loc[:, 'new_names'].values.tolist()


def ped2df():
    ped_fill_dict = {'family_id': sampleNamesList, 'sample_id': sampleNamesList, 'paternal_id': 0, 'maternal_id': 0, 'sex': 2, 'affection': 0}
    if not pedFile:
        ped_df = pd.DataFrame(ped_fill_dict)
        return ped_df.loc[:, list(ped_fill_dict)]
    return pd.read_table(pedFile, sep='\t', header='infer', names=list(ped_fill_dict), engine='python')


def convert_snp(string):
    if (len(string) > 2 and string != '---') or (string[:1] == '-' and string[1:2] != '-'):
        if string[:2] == '--':
            return 'D;D'
        if string[:1] == '-' and string[:2] != '--':
            return 'I;D'
        if string[:1] != '-':
            return 'I;I'
    if string == '---' or string == '--':
        return '0;0'
    return string[:int(len(string) / 2)] + ';' + string[int(len(string) / 2):]


if __name__ == '__main__':
    startBench = timeit.default_timer()
    afmFileList, pedFile, sampleDataFile, outputFileName = parse_namespace()
    afmDF, sampleNamesList = afm2df(afmFileList)
    if sampleDataFile:
        afmDF, sampleNamesList = rename_afm_df(afmDF)
    afmDF = afmDF.set_index('dbSNP_RS_ID').applymap(convert_snp)
    pedDF = ped2df()
    pedExportBuffer = ''
    for pedRow in range(0, len(pedDF)):
        pedExportBuffer += '\t'.join(str(column) for column in pedDF.loc[pedRow, :].values.tolist() + afmDF.loc[:, pedDF.loc[pedRow, :].values.tolist()[0]].values.tolist()).replace(';', '\t') + '\n'
    pedExportWrapper = open(outputFileName, 'w')
    pedExportWrapper.write(pedExportBuffer)
    pedExportWrapper.close()
    stopBench = timeit.default_timer()
    print("Completed in", stopBench - startBench, "s.")
