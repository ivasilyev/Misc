#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import sys
import argparse
import getpass
import decimal
import re
import os


def parse_args():
    starting_parser = argparse.ArgumentParser(description="")
    starting_parser.add_argument("-o", "--online", required=True,
                                 help="Tab-delimited table to upload;")
    starting_parser.add_argument("-b", "--buffer", default=1000, type=int,
                                 help="(Optional) Numbers of row to fetch in time, 1000 by default;")
    starting_parser.add_argument("-r", "--rewrite", default=False,
                                 help="(Optional) Overwrite the existing table file;")
    starting_parser.add_argument("-d", "--download", required=True,
                                 help="Target table in the format: 'user@host:port/database/schema.\"table\"'.")
    return starting_parser.parse_args()


def split_handler(splitting_string, splitting_char, return_index):
    try:
        output = splitting_string.split(splitting_char)[return_index]
    except IndexError:
        output = ""
    return output


def flanked_with_quotes(string):
    return '"' + string.replace('"', '') + '"'


def parse_pq_address(address_string):
    output_dict = {}
    output_dict['user_name'] = split_handler(split_handler(address_string, '@', 0), ':', 0)
    output_dict['user_password'] = split_handler(split_handler(address_string, '@', 0), ':', 1)
    if len(output_dict['user_password']) == 0:
        print("You have not specified the database user's password!")
        output_dict['user_password'] = getpass.getpass()
    output_dict['host_address'] = split_handler(split_handler(address_string, '@', 1), ':', 0)
    output_dict['host_port'] = split_handler(split_handler(split_handler(address_string, '@', 1), ':', 1), '/', 0)
    if len(output_dict['host_port']) == 0:
        output_dict['host_port'] = '5432'
    output_dict['db_name'] = split_handler(address_string, '/', 1)
    if len(split_handler(address_string, '/', -1).split('.')) > 1:
        output_dict['schema'] = split_handler(split_handler(address_string, '/', -1), '.', 0)
    else:
        output_dict['schema'] = 'public'
    output_dict['table_name'] = split_handler(split_handler(address_string, '/', -1), '.', -1)
    if len(output_dict['table_name']) == 0:
        print("Please specify the table name as described! Exiting...")
        sys.exit(2)
    # Avoid decapitalization
    output_dict['schema'] = flanked_with_quotes(output_dict['schema'])
    output_dict['table_name'] = flanked_with_quotes(output_dict['table_name'])
    print("Connection properties: " + ', '.join([string + ': ' + str(output_dict[string]) for string in output_dict if string != 'user_password']))
    return output_dict


def parse_namespace():
    namespace = parse_args()
    return parse_pq_address(namespace.online), namespace.buffer, namespace.rewrite, namespace.download


def filename_only(string):
    return str(".".join(string.rsplit("/", 1)[-1].split(".")[:-1]))


def file_append(string, file_to_append):
    file = open(file_to_append, 'a+')
    file.write(string)
    file.close()


def var_to_file(var_to_write, file_to_write):
    file = open(file_to_write, 'w')
    file.write(var_to_write)
    var_to_write = None
    file.close()


def sql_authenticate(host, port, dbname, user, password):
    attempt_count = 0
    while attempt_count < 3:
        try:
            output_connection = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
            print("Logged as " + user + " in " + dbname + " on " + str(host) + ':' + str(port))
            return output_connection
        except psycopg2.OperationalError:
            print("Wrong database user password!")
            password = getpass.getpass()
            attempt_count += 1
    print("Too much bad login attempts! Exiting...")
    sys.exit(2)


def sql_action(sql_statement):
    result = None
    try:
        pqCursor.execute(sql_statement)
        try:
            result = pqCursor.fetchall()
        except psycopg2.ProgrammingError:
            pass
    except psycopg2.DatabaseError:
        postgreSQLConnection.commit()
        raise
    postgreSQLConnection.commit()
    if result:
        return result


def export_sql_table(online_table):
    table_rows_number = sql_action("SELECT COUNT(*) FROM " + online_table)[0][0]
    header_list = [column_tuple[0] for column_tuple in sql_action("SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = '" + re.sub('[\'\"]', '', online_table.split('.')[-1]) + "'")]
    if overwriteFlag or not os.path.isfile(outputFile):
        var_to_file('\t'.join(str(header) for header in header_list) + '\n', outputFile)
    offset_number = 0
    while offset_number < table_rows_number:
        sql_buffer = sql_action("SELECT * FROM " + online_table + " LIMIT " + str(exportBuffer) + " OFFSET " + str(offset_number))
        output_buffer = ""
        for output_tuple in sql_buffer:
            output_buffer += '\t'.join(str(output_value) for output_value in output_tuple) + '\n'
        file_append(output_buffer, outputFile)
        offset_number += exportBuffer
        if offset_number % 10000 == 0:
            print(str(offset_number) + " rows have been downloaded!")
    print(str(table_rows_number) + " rows have been downloaded!")


if __name__ == '__main__':
    inputDict, exportBuffer, overwriteFlag, outputFile = parse_namespace()
    postgreSQLConnection = sql_authenticate(host=inputDict['host_address'], port=inputDict['host_port'], dbname=inputDict['db_name'], user=inputDict['user_name'], password=inputDict['user_password'])
    pqCursor = postgreSQLConnection.cursor()
    export_sql_table(inputDict['schema'] + '.' + inputDict['table_name'])
    postgreSQLConnection.close()
