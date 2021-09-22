import time
from workflow.WF_2_parse_run_data.WF_2_helpers import WorkflowObj2

def run_script_2():
    print("\n================================\nRun Data Import Script\n================================\n\n")

    # import relevant data from json file
    # get relative path to json cache file
    # READER
    data_obj = WorkflowObj2()
    data_obj.get_json()

    # get information from user
    # READER
    data_obj.get_info_from_user()
    
    # format the data, create two versions of dataframe
    # contained in data_obj, qc df and results df
    # FORMATTER
    data_obj.format_dataframe()

    # at this point, dataframes from either workflow will look identical, so we move on
    # DB_HANDLER
    data_obj.database_push()   
    
    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)
    return data_obj.wgs_run_date

