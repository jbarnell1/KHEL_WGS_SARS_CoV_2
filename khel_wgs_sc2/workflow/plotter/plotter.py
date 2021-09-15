from workflow.plotter.plotter_helpers import plotter_obj
import time


def run_plotter():
    print("\n================================\nEPI_ISL Import Script\n================================\n\n")
    print("Importing data from cache...")

    # import relevant data from json file
    data_obj = plotter_obj()
    data_obj.get_json()

    # query full database --> pandas dataframe
    data_obj.get_plotter_dfs()

    # placeholder for future
    data_obj.do_stuff()
    
    # write to HTML file for observation
    data_obj.write_data()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)