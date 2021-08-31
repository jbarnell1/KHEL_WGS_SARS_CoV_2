import time
from workflow.WF_3_compile_fasta.WF_3_helpers import WorkflowObj3

def run_script_3():
    print("\n================================\nall.fasta script\n================================\n\n")
    # import relevant data from json file
    data_obj = WorkflowObj3()
    data_obj.get_json()


    # create master FASTA file
    compiled_fasta_path = data_obj.compile_fasta()

    # create dataframe identifying paths to each fasta file
    data_obj.get_fasta_path_df()

    # push the path pointers to the qc table
    #NOTE the path_to_fasta will be sent over to the results_table in the nextclade_parser
    data_obj.database_push()

    print("\n================================\nSuccess! Script Finished.\n================================\n\n")
    time.sleep(2)

    return compiled_fasta_path

    