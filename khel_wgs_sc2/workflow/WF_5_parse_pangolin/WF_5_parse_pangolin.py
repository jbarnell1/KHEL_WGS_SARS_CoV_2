import time
from workflow.WF_5_parse_pangolin.WF_5_helpers import WorkflowObj5

def run_script_5(logger):
    print("\n================================\nRun Data Import Script\n================================\n\n")

    # import relevant data from json file
    data_obj = WorkflowObj5(logger)
    data_obj.get_json()

    # open demo path --> pandas dataframe
    data_obj.get_pango_dfs()

    # push results to database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

    

