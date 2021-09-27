from workflow.WF_9_send_fastas.WF_9_helpers import WorkflowObj9
import time


def run_script_9(day):

    print("\n================================\nCompile Qualifying FASTAs\n================================\n\n")

    # import relevant data from json file
    data_obj = WorkflowObj9()
    data_obj.get_json()

    # get paths to files
    data_obj.get_lst_fasta_files(day)

    # build fasta file
    data_obj.build_fasta()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)