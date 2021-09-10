import time
from workflow.WF_1_import_demos.WF_1_helpers import WorkflowObj1

def run_script_1():
    print("\n================================\nDemographics Import Script\n================================\n\n")

    # import relevant data from json file
    # READER
    data_obj = WorkflowObj1()
    data_obj.get_json()

    # verify that controls are valid
    data_obj.get_priority()
    data_obj.verify_ctrls()

    # open demo path --> pandas dataframe
    # READER
    data_obj.get_initial_demo_df()

    # clean up data
    # FORMATTER
    data_obj.format_demo_df()

    # grab demographics from LIMS
    # READER
    data_obj.get_initial_lims_df()

    # clean up data
    # FORMATTER
    data_obj.format_lims_df()

    # merge the two dataframes together
    # inner join on hsn
    # FORMATTER
    data_obj.merge_dfs()
    data_obj.format_dfs()

    # get info into database
    # DB_HANDLER
    data_obj.database_push()

    # print("\nThe following HSN's already existed in the database, and were not added:")
    # print(data_obj.already_exist)
    # print("^^ " + str(len(data_obj.already_exist)) + " total samples^^\n")

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)
        