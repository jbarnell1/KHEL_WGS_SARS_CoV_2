import json
import datetime
import os
import pandas as pd
from workflow.ui import get_path_folder


def write_json(path, py_dict):
    try:
        with open(path, mode='w') as cache_file:
            json.dump(py_dict, cache_file, indent=4)
        return 0
    except:
        return 1

def save_csv(df, path, user_selection, lab):
    # get today's date to produce file names
    today = datetime.datetime.today().strftime("%m%d%y")
    filename_df = "KHEL_Variant_" + today + "sql_test" + ".csv"

    if not os.path.isdir(path):
        os.makedirs(path)
    
    if user_selection == 'a':
        filename_df = "whole_db_" + today + ".csv"
    elif user_selection == 's' or user_selection == 'sd':
        filename_df = "submitted_" + lab + "_" + today + ".csv"
    elif user_selection == 'f':
        filename_df = lab + "_" + today + ".csv"
    else:
        pass
    # save files
    try:
        df.to_csv(path + "\\" + filename_df, index = False)
        #bad_df.to_csv(path + filename_baddf, index = False)
    except PermissionError as e:
        print(e ,"\n This can happen when the file is already open.  Make sure the epi excel files are closed!")
    return


def save_epi_csv(df, bad_df, path):
    # get today's date to produce file names
    today = datetime.datetime.today().strftime("%m%d%y")
    filename_df = "KHEL_Variant_" + today + ".csv"
    filename_bad_df = "KHEL_Variant_" + today + "_bad.csv"

    # make new folder to save to
    if not os.path.isdir(path):
        os.makedirs(path)
    
    # save files
    try:
        df.to_csv(path + "\\" + filename_df, index = False)
        bad_df.to_csv(path + "\\" + filename_bad_df, index=False)
        #bad_df.to_csv(path + filename_baddf, index = False)
    except PermissionError as e:
        print(e ,"\n This can happen when the file is already open.  Make sure the epi excel files are closed!")
    return


def save_facility_csv(df, facility):
    today = datetime.today().strftime("%m%d%y")
    filename_df = facility + "_" + today + ".csv"

    # make new folder to save to
    path = get_path_folder()
    if not os.path.isdir(path):
        os.makedirs(path)
    
    # save files
    try:
        df.to_csv(path + filename_df, index = False)
    except PermissionError as e:
        print(e ,"\n This can happen when the file is already open.  Make sure the epi excel files are closed!")
    return