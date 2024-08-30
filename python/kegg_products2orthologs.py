#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import multiprocessing
import pandas as pd
import re


def parse_args():
    starting_parser = argparse.ArgumentParser(description="Given KEGG Compound ID(s) (CXXXXX) or containing file(s), writes all found relted proteins to file. \nKEGG API documentation: http://www.kegg.jp/kegg/docs/keggapi.html")
    starting_parser.add_argument("-i", "--input", required=True, nargs='+', help="Space-divided KEGG Compound ID(s) (CXXXXX) or file(s) supplying it one per line")
    starting_parser.add_argument("-n", "--no_intersections", default=False, action="store_true", help="Should identical KEGG Orthology IDs (KXXXXX) be filtered?")
    starting_parser.add_argument("-o", "--output", required=True, help="Mask of files to write")
    return starting_parser.parse_args()


def parse_namespace():
    namespace = parse_args()
    return namespace.input, namespace.no_intersections, namespace.output


def file_to_list(file):
    file_buffer = open(file, 'rU')
    output_list = [j for j in [re.sub('[\r\n]', '', i) for i in file_buffer] if len(j) > 0]
    file_buffer.close()
    return output_list


def files_to_list(files_list):
    output_list = []
    for file_nanme in files_list:
        output_list += file_to_list(file_nanme)
    return [i for i in output_list if len(i) > 0]


def kegg_request(kegg_entry):
    return subprocess.getoutput("curl http://rest.kegg.jp/get/" + kegg_entry)


def get_kegg_field_value(kegg_entry, kegg_field_names_list):
    raw_kegg_response = kegg_request(kegg_entry)
    digested_kegg_response = re.sub('[\n\r ]+', ' ', raw_kegg_response)
    kegg_response_fields_list = [i.strip() for i in re.findall('\n[A-Z]{4,}', raw_kegg_response)]
    output_dict = {}
    for kegg_field_name in kegg_field_names_list:
        try:
            try:
                output_dict[kegg_field_name] = re.findall(kegg_field_name + "(.*)" + kegg_response_fields_list[kegg_response_fields_list.index(kegg_field_name) + 1], digested_kegg_response)[0].strip()
            except IndexError:
                output_dict[kegg_field_name] = re.findall(kegg_field_name + "(.*)", digested_kegg_response)[0].strip()
        except ValueError:
            print("Cannot define the field '" + kegg_field_name + "' for entry '" + kegg_entry + "'")
            output_dict[kegg_field_name] = ""
    return output_dict


def mp_compose_kegg(compound_id):
    output_ds = pd.DataFrame(columns=["compound_id", "compound_names", "enzyme_id", "enzyme_names", "orthology_id", "orthology_name"])
    compound_dict = get_kegg_field_value(compound_id, ["NAME", "ENZYME"])
    enzyme_names_list = []
    orthology_ids_list = []
    for enzyme_id in [i for i in compound_dict["ENZYME"].split(' ') if len(i) > 0 and not i.endswith('-')]:
        enzyme_dict = get_kegg_field_value(enzyme_id, ["NAME", "ORTHOLOGY"])
        enzyme_names_list.append(enzyme_dict["NAME"])
        try:
            for orthology_id, orthology_name in zip(re.findall('K[0-9]{5}', enzyme_dict["ORTHOLOGY"]), [i.strip() for i in re.split('K[0-9]{5}', enzyme_dict["ORTHOLOGY"]) if len(i) > 0]):
                output_ds = output_ds.append(pd.DataFrame(data={"compound_id": [compound_id], "compound_names": [compound_dict["NAME"]], "enzyme_id": [enzyme_id], "enzyme_names": [enzyme_dict["NAME"]], "orthology_id": [orthology_id], "orthology_name": [orthology_name]}), ignore_index=True)
            orthology_ids_list.append(enzyme_dict["ORTHOLOGY"])
        except KeyError:
            pass
    output_df = pd.DataFrame(data={"compound_id": [compound_id], "compound_names": [compound_dict["NAME"]], "enzyme_ids": ["; ".join(compound_dict["ENZYME"].split(' '))], "enzyme_names": ["; ".join(enzyme_names_list)], "orthology_ids": ["; ".join(orthology_ids_list)]})
    return output_ds, output_df


def multi_core_queue(function_to_parallelize, queue):
    pool = multiprocessing.Pool()
    output = pool.map(function_to_parallelize, queue)
    pool.close()
    pool.join()
    return output


def process_intersections():
    ds = outputDataSet.set_index("compound_id")
    unique_per_compound_orthology_ids_list = []
    for processed_compound_id in pd.unique(ds.index.values):
        unique_per_compound_orthology_ids_list += pd.unique(ds.loc[processed_compound_id, "orthology_id"].values).tolist()
    repeating_ids_list = list(set([i for i in unique_per_compound_orthology_ids_list if unique_per_compound_orthology_ids_list.count(i) > 1]))
    if len(repeating_ids_list) > 0:
        filtered_ds = outputDataSet.loc[outputDataSet["orthology_id"].isin(repeating_ids_list)]
        filtered_ds.to_csv(outputFileMask + "_removed_dataset.tsv", sep='\t', index=False)
    return outputDataSet.loc[~outputDataSet["orthology_id"].isin(repeating_ids_list)]


if __name__ == '__main__':
    inputList, noIntersectionsBool, outputFileMask = parse_namespace()
    if all(os.path.isfile(i) for i in inputList):
        inputList = files_to_list(inputList)
    inputList = pd.unique(inputList)
    composedDSsAndDFsBuffer = multi_core_queue(mp_compose_kegg, inputList)
    outputDataSet, outputDataFrame = multi_core_queue(pd.concat, [[i[0] for i in composedDSsAndDFsBuffer], [j[1] for j in composedDSsAndDFsBuffer]])
    if noIntersectionsBool:
        outputDataSet = process_intersections()
    outputDataSet.to_csv(outputFileMask + "_detailed_dataset.tsv", sep='\t', index=False)
    outputDataFrame.to_csv(outputFileMask + "_brief_dataframe.tsv", sep='\t', index=False)
