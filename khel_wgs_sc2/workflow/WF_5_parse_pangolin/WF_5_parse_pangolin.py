import time
from workflow.WF_5_parse_pangolin.WF_5_helpers import WorkflowObj5

def run_script_5(compiled_fasta_path):
    print("\n================================\nRun Data Import Script\n================================\n\n")

    # import relevant data from json file
    data_obj = WorkflowObj5()
    data_obj.get_json()

    if compiled_fasta_path:
        target_folders = compiled_fasta_path.split("/")
        if len(target_folders) <= 1:
            compiled_fasta_path = data_obj.get_fasta_path()
            target_folders = compiled_fasta_path.split("/")
        target_folder = "/".join(target_folders[:-1])
        try:
            data_obj.send_fasta(compiled_fasta_path)
            data_obj.run_pangolin()
            data_obj.receive_pangolin_df(target_folder)
            data_obj.clean_connections()
        except Exception as e:
            data_obj.clean_connections()
            raise ValueError("Possible Connection error: " + e)
        data_obj.get_pango_dfs(pango_path=target_folder + "/results.csv")
        
    else:
        # open demo path --> pandas dataframe
        data_obj.get_pango_dfs()

    # push results to database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

    

