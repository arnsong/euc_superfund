#!/usr/bin/env python

import config
from model import engine, Site, Sample

import os, sys, argparse
import sys

from sqlalchemy.orm import sessionmaker

import yaml
import pandas as pd


##### Load data load config

def load_config(config_file):

    mappings = iter(yaml.load_all(open(config_file), Loader=yaml.FullLoader))
    file_info = next(mappings)

    return file_info, mappings


def load_datafile(datafile, mapping, engine=None, datafile_type='xlsx', if_exists='append', index=False):

    if not engine:
        print("A sqlalchemy engine is required")
        return

    # Start session for queries
    Session = sessionmaker(bind=engine)
    session = Session()

    # TODO -- check if table exists
    
    # TODO -- After loading mapping, make sure that the columns exist, if not add them to the table
    
    # Load csv data into pandas dataframe
    for sheet in mapping['sheets']:
        
        print(f"Loading {sheet} in {datafile}")

        if datafile_type == 'xlsx':
            data_orig = pd.read_excel(datafile, sheet)
        else:
            data_orig = pd.read_csv(datafile)

        for table in mapping['tables']:

            # Make a copy of the data b/c we'd like to keep the column names
            data = data_orig.copy()

            # Rename column headings and drop columns that are not in the mapping
            columns = mapping['tables'][table]['columns']
            for column_name in columns.keys():
                data.rename(columns={columns[column_name]: column_name}, inplace=True)

            drop_cols = [ col_name for col_name in data.columns if col_name not in columns.keys() ]
            data.drop(columns=drop_cols, inplace=True)

            for idx, row in data.iterrows():

                # TODO -- This should be a "find existing record function"
                obj = mapping['tables'][table]['sqlalchemy_obj']
                keys = mapping['tables'][table]['keys']

                eval_string = f'session.query({obj})'

                for key in keys:
                    value = row[key]
                    if isinstance(value, str):
                        value.replace("'", "\\'")
                    eval_string += f'.filter({obj}.{key}=="{value}")'

                eval_string += ".all()"
                query_results = eval(eval_string)

                # If input data row does not match any database rows, then add the row in its entirety
                if len(query_results)==0:
                    # Add row with table specific columns to table
                    pd.DataFrame(row).T.to_sql(table, con=engine, if_exists='append', index=False)
                else:
                    # Update fields
                    for result in query_results: 
                        for col in data.columns:
                            if col=='STREAM_ORDER':
                                if row[col]=='8+':
                                    row[col] = '8'
                            col_update = setattr(result, col, row[col])

                if idx%100==0:
                    print(f"Index: {idx}/{len(data.index)}")
            
            print(f"{datafile}: {table} is finished")


def load_dataset(config_file, datafile_path=''):

    file_info, mappings = load_config(config_file)
    for mapping in mappings:
        load_datafile(os.path.join(datafile_path, file_info['Filename']), mapping, engine)


# ===============================================================

if __name__ == '__main__':

    # Parse arguments
    argparser = argparse.ArgumentParser(description=__file__)
    argparser.add_argument('-p', '--path', help='The path to the directory containing the datafiles')
    argparser.add_argument('-f', '--files', help='Name of data load configuration file(s)', nargs='+', required=True)
    args = argparser.parse_args()

    
    for config_file in args.files:
        load_dataset(config_file, args.path)
