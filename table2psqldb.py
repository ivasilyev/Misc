#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2 as adapter
import sys
import argparse
import getpass
import decimal
import re


def parse_args():
    starting_parser = argparse.ArgumentParser(description="This script will upload a text table into SQL database. Note that the header will generated automatically if not present. Please also check the encoding, it must be UTF-8.")
    starting_parser.add_argument("-i", "--input", required=True,
                                 help="Tab-delimited table to upload;")
    starting_parser.add_argument("-d", "--delimiter", default='\t',
                                 help="(Optional) Delimiter with escape if required, tab by default;")
    starting_parser.add_argument("-e", "--header", default=False, action='store_true',
                                 help="(Optional) Force to use the first table row as a header;")
    starting_parser.add_argument("-r", "--repopulate", default=False, action='store_true',
                                 help="(Optional) Overwrite the existing table. WARNING! All existing data in the table will be lost;")
    starting_parser.add_argument("-o", "--online", required=True,
                                 help="Target table in the format: 'user@host:port/database/\"schema\"~\"table\"'.")
    return starting_parser.parse_args()


def split_handler(splitting_string, splitting_char, return_index):
    try:
        output = splitting_string.split(splitting_char)[return_index]
    except IndexError:
        output = ""
    return output


def flanked_with_quotes(string):
    return '"' + string.replace('"', '') + '"'


def parse_pq_address(input_table, address_string):
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
    output_dict['schema'] = split_handler(split_handler(address_string, '/', -1), '~', 0)
    if len(output_dict['schema']) == 0:
        print("The export schema name has not been specified! Using the 'public' schema name...")
        output_dict['schema'] = 'public'
    output_dict['table_name'] = split_handler(split_handler(address_string, '/', -1), '~', -1)
    if len(output_dict['table_name']) == 0:
        print("The export table name has not been specified! Using the source table name...")
        output_dict['table_name'] = filename_only(input_table)
    # Avoid decapitalization
    output_dict['schema'] = flanked_with_quotes(output_dict['schema'])
    output_dict['table_name'] = flanked_with_quotes(output_dict['table_name'])
    print("Connection properties: " + ', '.join([string + ': ' + output_dict[string] for string in output_dict if string != 'user_password']))
    return output_dict


def parse_namespace():
    namespace = parse_args()
    return namespace.input, namespace.delimiter, namespace.header, namespace.repopulate, parse_pq_address(namespace.input, namespace.online)


def filename_only(string):
    return ".".join(string.rsplit("/", 1)[-1].split(".")[:-1])


def check_type(string):
    string = str(string)
    if '.' in string or 'e' in string:
        try:
            string_0 = float(string)
            if 'e' not in string:
                decimals = len(string.split('.')[1])
            else:
                decimals = abs(decimal.Decimal(string).as_tuple().exponent)
            if decimals < 7:
                return 'real'
            if decimals < 16:
                return 'float8'
            if decimals < 16383 and len(string.split('.')[0]) < 131072:
                return 'decimal'
            pass
        except ValueError:
            pass
    if '.' not in string:
        try:
            string = int(string)
            if -32768 < string < 32767:
                return 'int2'
            if -2147483648 < string < 2147483647:
                return 'int4'
            return 'int8'
        except ValueError:
            pass
    return 'varchar'


def get_column_maximal_cell(table_file, delimiter, column_index, is_header):
    table_wrapper = open(table_file, 'rU')
    table_row_count = 0
    maximal_cell_value = '0'
    for table_row in table_wrapper:
        if table_row_count != 0 or not is_header:
            current_cell_value = re.sub('[\r\n]+', '', table_row).split(delimiter)[column_index]
            current_cell_type = check_type(current_cell_value)
            if current_cell_type == 'varchar':
                if len(maximal_cell_value) < len(current_cell_value):
                    maximal_cell_value = current_cell_value
                else:
                    pass
            if 'int' in current_cell_type:
                maximal_cell_value = max([int(maximal_cell_value), int(current_cell_value)])
            if any(float_type == current_cell_type for float_type in ['real', 'float8', 'decimal']):
                maximal_cell_value = max([float(maximal_cell_value), float(current_cell_value)])
        table_row_count += 1
    table_wrapper.close()
    return str(maximal_cell_value)


def is_with_header(table_file, delimiter):
    table_wrapper = open(table_file, 'rU')
    table_row_index = 0
    table_first_rows = []
    for table_row in table_wrapper:
        if table_row_index < 2:
            table_first_rows.append(re.sub('[\n\r]+', '', table_row).split(delimiter))
            table_row_index += 1
    table_wrapper.close()
    header_bool = False
    second_column_data_types_list = [check_type(column_1) for column_1 in table_first_rows[1]]
    for var1, var2 in zip([check_type(column_0) for column_0 in table_first_rows[0]], second_column_data_types_list):
        if var1 != var2:
            header_bool = True
            break
    if (not header_bool) and (not firstRowIsHeader):
        print("The file does not have a header! Creating a simple one...")
        column_number = 0
        columns_list = []
        for column in range(0, len(second_column_data_types_list)):
            columns_list.append("column_" + str(column_number))
            column_number += 1
    else:
        columns_list = table_first_rows[0]
    print("Resulting columns number: " + str(len(columns_list)))
    columns_dict = {}
    column_index = 0
    for column_name in columns_list:
        column_max_value = get_column_maximal_cell(table_file, delimiter, column_index, header_bool)
        column_data_type = check_type(column_max_value)
        columns_dict[column_name] = column_data_type
        if column_data_type == 'varchar':
            columns_dict[column_name] = column_data_type + '(' + str(len(column_max_value) + 1) + ')'
        if column_data_type == 'decimal':
            columns_dict[column_name] = column_data_type + '(' + str(len(column_max_value) + 1) + ', ' + str(len(column_max_value.split('.')[-1])) + ')'
        column_index += 1
    return header_bool, columns_dict


def sql_authenticate(host, port, dbname, user, password):
    attempt_count = 0
    while attempt_count < 3:
        try:
            output_connection = adapter.connect(host=host, port=port, dbname=dbname, user=user, password=password)
            print("Logged as " + user + " in " + dbname + " on " + host + ':' + port)
            return output_connection
        except adapter.OperationalError:
            print("Wrong database user password!")
            password = getpass.getpass()
            attempt_count += 1
    print("Too much bad login attempts! Exiting...")
    sys.exit(2)


def sql_action(sql_statement):
    result = None
    try:
        cursor.execute(sql_statement)
        try:
            result = cursor.fetchall()
        except adapter.ProgrammingError as error:
            if str(error) != "no results to fetch":
                print("adapter.ProgrammingError:", error)
            pass
    except adapter.DatabaseError as error:
        print("adapter.DatabaseError:", error)
        connection.commit()
        raise
    connection.commit()
    if result:
        return result


def create_sql_table(online_table, delimiter):
    header_bool, header_dict = is_with_header(inputTable, delimiter)
    # header_dict format: {col_name: data_type(max_len if required)}
    print("Trying to create the table: " + online_table)
    header_list = []
    for column in header_dict:
        if 'varchar' in header_dict[column]:  # The built-in collatable data types are text, varchar, and char
            header_dict[column] += ' COLLATE "C"'  # The "C" collations are postgreSQL-built-in and OS-independent
        header_list.append('"' + column + '" ' + header_dict[column])
    try:
        sql_action('CREATE TABLE ' + online_table + ' (' + ', '.join(header_list) + ') WITH (OIDS=FALSE);')
    except adapter.ProgrammingError as error:
        if overwriteFlag:
            print("Warning! The table will be replaced: " + online_table)
            sql_action('DROP TABLE IF EXISTS ' + online_table + ';')
            sql_action('CREATE TABLE ' + online_table + ' (' + ', '.join(header_list) + ') WITH (OIDS=FALSE);')
        else:
            print(error)
            print("The relation is seems to be already existing! Trying to append the table " + online_table)
    table_file_wrapper = open(inputTable, 'rU')
    sql_commands_list = []
    table_row_count = 0
    for table_row in table_file_wrapper:
        if table_row_count != 0 or (not header_bool and not firstRowIsHeader):
            row_values_list = []
            table_column_count = 0
            for table_column_value in re.sub('[\r\n]', '', table_row).split(delimiter):
                if 'varchar' in header_list[table_column_count]:
                    table_column_value = "'" + re.escape(table_column_value) + "'"
                row_values_list.append(table_column_value)
                table_column_count += 1
            sql_commands_list.append('INSERT INTO ' + online_table + ' (' + ', '.join(['"' + column + '"' for column in header_dict]) + ') VALUES (N' + ', '.join(row_values_list) + ');')
        table_row_count += 1
        if table_row_count % 10000 == 0:
            print(table_row_count, "rows have been uploaded!")
    table_file_wrapper.close()
    sql_action('\n'.join(sql_statement for sql_statement in sql_commands_list))

    print(table_row_count, "rows including header have been uploaded!")


if __name__ == '__main__':
    inputTable, inputDelimiter, firstRowIsHeader, overwriteFlag, outputDict = parse_namespace()
    connection = sql_authenticate(host=outputDict['host_address'], port=outputDict['host_port'], dbname=outputDict['db_name'], user=outputDict['user_name'], password=outputDict['user_password'])
    cursor = connection.cursor()
    create_sql_table(outputDict['schema'] + '.' + outputDict['table_name'], inputDelimiter)
    connection.close()
