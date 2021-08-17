import time
from workflow.query.query_helpers import query_obj


def run_query():
    print("\n================================\nSnapshot Generator\n================================\n\n")
    print("Importing data from cache...")

    # import relevant data from json file
    data_obj = query_obj()
    data_obj.get_json()

    # get df's from user input
    lst = data_obj.get_ui()
    data_obj.get_snapshot_by_input(lst)

    # write results to excel file
    data_obj.write_df_to_excel()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

