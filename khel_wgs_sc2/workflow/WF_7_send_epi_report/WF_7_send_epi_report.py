from workflow.WF_7_send_epi_report.WF_7_send_epi_report_helpers import WorkflowObj7
import time


def run_script_7():

    print("\n================================\nSafe file transfer protocol - WGS\n================================\n\n")

    # import relevant data from json file
    data_obj = WorkflowObj7()
    data_obj.get_json()

    # get path to file
    data_obj.get_file_path()

    # make transporter object
    data_obj.make_transporter()

    # send file
    data_obj.send_file()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)