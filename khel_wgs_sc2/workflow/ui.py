import time
import datetime
from tkinter import filedialog
from tkinter import *
import re


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def get_run_data():
    # get seq run id next
    platform = "ClearLabs"
    seq_run_id = ""
    ask = True
    while ask:
        seq_run_id = input("\nPlease copy/paste the seq_run_id value from the ClearLabs website below\nExample: Run BB1L12.2021-06-16.01\n--> ")
        
        # check that input is valid
        if not re.search("Run BB\dL\d{2}.\d{4}-\d{2}-\d{2}.\d{2}", seq_run_id):
            print("Invalid input, try again.")
        else:
            ask = False
    
    # now, pull meaningful information out of supplied data
    machine_num = seq_run_id[8:10]
    run_date = datetime.datetime.strptime(seq_run_id[11:21], '%Y-%m-%d').strftime("%m/%d/%Y")
    day_run_num = int(seq_run_id[-2:])

    # get the run data from clearlabs21
    ask = True
    print("\nPlease copy/paste all run data from the clearlabs website below\n")
    c = 0
    pos_dict = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8}
    run_data = {"hsn":[], "position":[], "avg_depth":[], "percent_cvg":[]}
    while c < 224:
        u_input = input("")
        if c % 7 == 0: # it is a seq_run_position
            # format input first
            pos = (int(u_input[-1])*8 - 8) + pos_dict[u_input[0]]
            run_data["position"].append(pos)
        elif c % 7 == 1: # it is an hsn
            hsn = ""
            if re.search("\d{7}..", u_input):
                hsn = u_input[0:-2]
            else:
                hsn = u_input
            run_data["hsn"].append(hsn)
        elif c % 7 == 3: # it is depth
            depth = u_input.replace("x", "")
            run_data["avg_depth"].append(int(depth))
        elif c % 7 == 4: # it is coverage
            coverage = u_input.replace("%", "")
            coverage = float(coverage)/100
            run_data["percent_cvg"].append(coverage)
        else:
            pass
        c += 1
    
    return run_data, machine_num, run_date, day_run_num, platform ;


def get_path():
    time.sleep(1)
    print("Opening dialog box...")
    time.sleep(1)
    root = Tk()
    root.withdraw()
    path_read = filedialog.askopenfilename()
    return path_read


def get_path_folder():
    time.sleep(1)
    print("Opening dialog box...")
    time.sleep(1)
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    return path

