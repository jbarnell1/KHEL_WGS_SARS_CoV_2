import time
from workflow.WF_4_parse_nextclade.WF_4_helpers import WorkflowObj4


def run_script_4():
    print("\n================================\nNextclade Data Import Script\n================================\n\n")

    # import relevant data from json file
    data_obj = WorkflowObj4()
    data_obj.get_json()

    # open nextclade path --> pandas dataframe
    data_obj.get_nextclade_dfs()

    # push results to database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

