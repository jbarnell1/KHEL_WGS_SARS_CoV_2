from workflow.WF_6_build_epi_report.WF_6_build_epi_report_helpers import WorkflowObj6
import time

def run_script_6():
    # Print welcome message
    print("\n================================\nReport Generator\n================================\n\n")
    
    # import relevant data from json file
    data_obj = WorkflowObj6()
    data_obj.get_json()

    # open sql database --> pandas dataframe
    data_obj.get_ui()

    # get user input (should we format df by facility or date?)
    data_obj.get_df()

    # format the data, create the dataframe
    data_obj.format_df()

    # write out the dataframe to excel file
    data_obj.write_epi_report()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)
