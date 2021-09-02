import time
from workflow.WF_4_parse_nextclade.WF_4_helpers import WorkflowObj4


def run_script_4(compiled_fasta_path):
    print("\n================================\nNextclade Data Import Script\n================================\n\n")
    # import relevant data from json file
    data_obj = WorkflowObj4()
    data_obj.get_json()

    if compiled_fasta_path:
        target_folders = compiled_fasta_path.split("/")
        if len(target_folders) <= 1:
            compiled_fasta_path = data_obj.get_fasta_path()
            target_folders = compiled_fasta_path.split("/")
        target_folder = "/".join(target_folders[:-1])
        try:
            data_obj.send_fasta(compiled_fasta_path)
            data_obj.run_nextclade()
            data_obj.receive_nextclade_df(target_folder)
            data_obj.clean_connections()
        except Exception as e:
            data_obj.clean_connections()
            raise ValueError("Possible connection error: " + e)
        data_obj.get_nextclade_dfs(nc_path=target_folder + "/nextclade.tsv")

    else:
        # open nextclade path --> pandas dataframe
        data_obj.get_nextclade_dfs()

    # push results to database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

