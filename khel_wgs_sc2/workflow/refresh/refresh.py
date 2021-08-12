import time
from workflow.refresh.refresh_helpers import refresh_obj


def run_refresh(logger):
    print("\n================================\nImport Excel file to database\n================================\n\n")

    # import relevant data from json file
    data_obj = refresh_obj(logger)
    data_obj.get_json()

    # open master path --> pandas dataframe
    data_obj.get_refresh_dfs()

    # clear the database
    data_obj.database_clear()
    
    # push results to database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

