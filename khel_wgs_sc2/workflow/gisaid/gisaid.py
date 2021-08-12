import time
from workflow.gisaid.gisaid_helpers import gisaid_obj


def run_gisaid(logger):
    print("\n================================\nGISAID Report Script\n================================\n\n")
    print("Importing data from cache...")

    # import relevant data from json file
    data_obj = gisaid_obj(logger)
    data_obj.get_json()

    data_obj.get_gisaid_dfs()
    data_obj.get_db_info()
    data_obj.compile_fasta()
    data_obj.compile_gisaid()
    data_obj.make_fasta_file()
    data_obj.make_gisaid_file()

    # push information to the database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

