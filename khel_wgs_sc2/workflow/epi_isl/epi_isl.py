from workflow.epi_isl.epi_isl_helpers import epi_isl_obj
import time


def run_epi_isl():
    print("\n================================\nEPI_ISL Import Script\n================================\n\n")
    print("Importing data from cache...")

    # import relevant data from json file
    data_obj = epi_isl_obj()
    data_obj.get_json()

    # open epi_isl workbook path --> pandas dataframe
    data_obj.get_epi_isl_dfs()

    # push information to the database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

