import time
from workflow.outside_lab.outside_lab_helpers import outside_lab_obj


def run_outside_lab():
    print("\n================================\nImport Excel file to database\n================================\n\n")

    # import relevant data from json file
    data_obj = outside_lab_obj()
    data_obj.get_json()

    # open outside lab path --> pandas dataframe
    data_obj.get_outside_lab_dfs()

    # push results to database
    data_obj.database_push()
    
    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

