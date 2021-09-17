import time
from workflow.plotter.plotter_helpers import plotter_obj


def run_plotter():
    print("\n================================\nPlotter Script\n================================\n\n")

    # import relevant data from json file
    data_obj = plotter_obj()
    data_obj.get_json()

    # open outside lab path --> pandas dataframe
    data_obj.get_plots()

    # push results to database
    #data_obj.save_plots()
    
    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)