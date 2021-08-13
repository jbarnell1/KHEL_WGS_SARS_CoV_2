import json
import datetime
import os
from workflow.ui import get_path


def write_json(path, py_dict):
    try:
        with open(path, mode='w') as cache_file:
            json.dump(py_dict, cache_file, indent=4)
        return 0
    except:
        return 1
    

def save_csv(df):
    # get today's date to produce file names
    today = datetime.datetime.today().strftime("%m%d%y")
    filename_df = "KHEL_Variant_" + today + "sql_test" + ".csv"
    filename_baddf = "KHEL_Variant_" + today + "_bad.csv"

    # make new folder to save to
    path = get_path()
    if not os.path.isdir(path):
        os.makedirs(path)
    
    # save files
    try:
        df.to_csv(path + filename_df, index = False)
        #bad_df.to_csv(path + filename_baddf, index = False)
        print("The program will close automatically in 5 seconds")
    except PermissionError as e:
        print(e ,"\n This can happen when the file is already open.  Make sure the epi excel files are closed!")
        print("The program will close automatically in 5 seconds")
    return


def save_facility_csv(df, facility):
    today = datetime.today().strftime("%m%d%y")
    filename_df = facility + "_" + today + ".csv"

    # make new folder to save to
    path = get_path()
    if not os.path.isdir(path):
        os.makedirs(path)
    
    # save files
    try:
        df.to_csv(path + filename_df, index = False)
        print("The program will close automatically in 5 seconds")
    except PermissionError as e:
        print(e ,"\n This can happen when the file is already open.  Make sure the epi excel files are closed!")
        print("The program will close automatically in 5 seconds")
    return