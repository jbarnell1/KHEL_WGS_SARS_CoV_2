from ..workflow_obj import workflow_obj
from ..processor import *
import time
import os
import re
import sys
import datetime
import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine


class query_obj(workflow_obj):
    # constructor
    def __init__(self, logger):
        self.logger = logger
        self.id = 'query'

    # methods
    def get_json(self):
        self.logger.info(self.id + ": Acquiring local data from cache")
        super().get_json(-4)
        self.logger.info(self.id + ": get_json finished!")

    def get_ui(self):
        self.logger.info(self.id + ": getting dataframes from user input")
        print("\n================================\nSnapshot Generator\n================================\n\n")

        self.uniquefilename = ""
        ask = True
        ask2 = True
        while ask:
            # get the user's input to determine what to do
            user_input = input("\nHow would you like to query the database?\n\
By all                              -type 'all'\n\
By all samples passing qc           -type 'all_valid'\n\
By date of collection               -type 'doc'\n\
By WGS run date                     -type 'wgs_run_date'\n\
By date of birth                    -type 'dob'\n\
By date of receipt                  -type 'date_recd'\n\
By hsn                              -type 'hsn'\n\
By clade                            -type 'clade'\n\
By lineage                          -type 'lineage_id'\n\
By minimum avg_depth or percent_cvg -type 'min'\n\
By race                             -type 'race'\n\
By facility                         -type 'facility'\n\
By county                           -type 'county'\n\
By source                           -type 'source'\n\
\n\
Or, to get a list of unique values for a given category, type 'unique'\n\
--> ")
            
            if user_input.lower() in self.valid_lst:
                if user_input.lower() == "min":
                    # get and format min value correctly
                    while ask2:
                        user_input2 = input("\nWould you like to search by average depth (type 'avg_depth') or percent coverage (type 'percent_cvg')\n--> ")
                        if user_input2 == "percent_cvg":
                            ask3 = True
                            while ask3:
                                user_input3 = input("\nPlease enter the cutoff coverage value (i.e. 85.33)\n--> ")
                                if float(user_input3) <= 100 and float(user_input3) >= 0:
                                    self.uniquefilename = "min_cvg_" + str(user_input3) + "_snapshot"
                                    user_input3 = float(user_input3)/100
                                    ask3 = False
                                else:
                                    print("\nInvalid input, please enter a number between 0 and 100.\n")
                            ask2 = False
                        elif user_input2 == "avg_depth":
                            ask3 = True
                            while ask3:
                                user_input3 = input("\nPlease enter the cutoff depth value (i.e. 150)\n--> ")
                                if float(user_input3) >= 0:
                                    ask3 = False
                                    self.uniquefilename = "min_depth_" + str(user_input3) + "_snapshot"
                                else:
                                    print("\nInvalid input, please enter a number that is non-negative.\n")
                            ask2 = False
                        else:
                            print("\nInvalid input, please try again.\n")
                    # get the snapshot
                    lst =  [user_input, user_input2, user_input3]
                    #self.df = get_snapshot_by_input(user_input, user_input2, user_input3)


                elif user_input.lower() in self.date_options:
                    # get and format date correctly
                    while ask2:
                        user_input2 = input("\nWould you like to select a single date (type 's') or a range of dates (type 'r')?\n--> ")
                            
                        if user_input2 =='s':
                            ask3 = True
                            while ask3:
                                user_input2 = input("\nPlease input the date for the search (yyyy-mm-dd format)\n--> ")
                                if re.search("\d{4}-\d{2}-\d{2}", user_input2):
                                    self.uniquefilename = "date_" + user_input2 + "_snapshot"
                                    ask3 = False
                                    ask2 = False
                                else:
                                    print("Invalid input! Try again.")
                            # get the snapshot
                            lst =  [user_input, user_input2, user_input3]
                            #self.df = get_snapshot_by_input(user_input, user_input2, user_input2)
                        
                        elif user_input2 == 'r':
                            # get and format both dates correctly
                            ask3 = True
                            while ask3:
                                user_input2 = input("\nPlease input the starting date for the search (yyyy-mm-dd format)\n--> ")
                                if re.search("\d{4}-\d{2}-\d{2}", user_input2):
                                    ask3 = False
                                    ask2 = False
                                else:
                                    print("Invalid input! Try again.")
                            ask3 = True
                            while ask3:
                                user_input3 = input("\nPlease input the ending date for the search (yyyy-mm-dd format)\n--> ")
                                if re.search("\d{4}-\d{2}-\d{2}", user_input2):
                                    self.uniquefilename = "from_" + user_input2 + "_to_" + user_input3 + "_snapshot"
                                    ask3 = False
                                    ask2 = False
                                else:
                                    print("Invalid input! Try again.")
                            # get the snapshot
                            lst =  [user_input, user_input2, user_input3]
                            #self.df = get_snapshot_by_input(user_input, user_input2, user_input3)
                        
                        else:
                            print("\nInvalid input! Please try again.\n")
                        
                    # get the snapshot
                    lst =  [user_input, user_input2, user_input3]
                    #self.df = get_snapshot_by_input(user_input, user_input2, user_input3)
                
                elif user_input.lower() == "unique":
                    while ask2:
                        user_input2 = input("\nWhat category would you like to query?\n\
By date of collection               -type 'doc'\n\
By WGS run date                     -type 'wgs_run_date'\n\
By date of birth                    -type 'dob'\n\
By date of receipt                  -type 'date_recd'\n\
By hsn                              -type 'hsn'\n\
By clade                            -type 'clade'\n\
By lineage                          -type 'lineage_id'\n\
By minimum avg_depth or percent_cvg -type 'min'\n\
By race                             -type 'race'\n\
By facility                         -type 'facility'\n\
By county                           -type 'county'\n\
By source                           -type 'source'\n\
--> ")
                        if user_input2 in self.valid_lst:
                            self.uniquefilename = "unique_" + user_input2 + "_snapshot"
                            ask2 = False
                        else:
                            print("Invalid input! Try again.")
                    lst =  [user_input, user_input2, None]
                    #self.df = get_snapshot_by_input(user_input, user_input2, None)
                
                elif user_input.lower() == "all":
                    #self.df = get_snapshot_by_input(user_input, None, None)
                    self.uniquefilename = "full_database_snapshot"
                    lst =  [user_input, None, None]
                
                elif user_input.lower() == "all_valid":
                    #self.df = get_snapshot_by_input(user_input, None, None)
                    self.uniquefilename = "full_database_snapshot_valid"
                    lst =  [user_input, None, None]

                else:
                    ask2 = True
                    while ask2:
                        user_input2 = input(f"\nPlease input the {user_input} to search for.\n--> ")
                        self.uniquefilename = user_input + "=" + str(user_input2) + "_snapshot"
                        ask2 = False
                    
                    # get the snapshot
                    lst = [user_input, user_input2, None]
                    #self.df = get_snapshot_by_input(user_input, user_input2, None)
                ask = False
            else:
                print("\nInvalid input! Please try again.\n")
                pass
        self.logger.info(self.id + ": get_query_dfs_from_ui finished!")
        lst.append(self.percent_cvg_cutoff)
        lst.append(self.avg_depth_cutoff)
        return lst
        

    def write_df_to_excel(self):
        self.logger.info(self.id + ": writing the dataframe to excel file")
        # Now that we have dataframe, we can convert it to an excel file
        datetoday = datetime.datetime.today().strftime("%m%d%y")
        folder_path = self.folder_path_base + datetoday + "\\"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_no = 1
        filepath = self.uniquefilename + "_" + str(file_no) + ".xlsx"
        while os.path.exists(folder_path + filepath):
            file_no += 1
            filepath = self.uniquefilename + "_" + str(file_no) + ".xlsx"

        self.df.to_excel(folder_path + filepath)
        self.logger.info(self.id + ": write_df_to_excel finished!")

    def database_push(self):
        pass

    def get_snapshot_by_input(self, lst):
        do_merge = True
        query_all = False
        super().database_query()


    ###############################################################################
        # min query will act differently than the others   
        
        if input.lower() == "min":
            query = format_query(query=self.read_query_min, lst=lst)
    #         query = self.read_query_min
    #         query = """\
    # SELECT * FROM dbo.Table_1 \
    # WHERE {} >= {} And avg_depth >= 75\
    # """\
    #         .format(lst[1], lst[2])
    ###############################################################################
        elif input.lower() in self.date_options:
            query_all = True
            query = format_query(query=self.read_query_date, lst=lst)
    #         query = """\
    # SELECT * FROM dbo.Table_1 \
    # WHERE {} >= CAST('{}' AS DATE) And {} <= CAST('{}' AS DATE)\
    # """\
    #         .format(input, lst[1], input, lst[2])
    ###############################################################################
        elif input.lower() in self.strtype:
            query = format_query(query=self.read_query_str, lst=lst)
    #         # everything but non-str will follow this code
    #         query = """\
    # SELECT * FROM dbo.Table_1 \
    # WHERE UPPER({}) LIKE UPPER('%{}%')\
    # """\
    #         .format(input, lst[1])
    ###############################################################################
        elif input.lower() == 'unique':
            do_merge = False
            query = format_query(query=self.read_query_unique, lst=lst)
    #         query = """\
    # SELECT {}, count(*) \
    # FROM dbo.Table_1
    # WHERE {} IS NOT NULL
    # GROUP BY {}
    # """\
    #         .format(lst[1], lst[1], lst[1])
    ###############################################################################
        elif input.lower() == "all":
            query_all = True
            query = format_query(query=self.read_query_all, lst=lst)
    #         query = """\
    # SELECT * FROM dbo.Table_1\
    # """
    ###############################################################################
        elif input.lower() == "all_valid":
            query = format_query(query=self.read_query_all_valid, lst=lst)
    #         query = """\
    # SELECT * FROM dbo.Table_1 \
    # WHERE percent_cvg > 77\
    # """
    ###############################################################################
        # everything else
        else:
            query = format_query(query=self.read_query_else, lst=lst)
    #         query = """\
    # SELECT * FROM dbo.Table_1 \
    # WHERE {} = {}\
    # """\
    #         .format(input, lst[1])
    ###############################################################################
        # now, query the database
        #self.df = pd.read_sql(query, con=self.db)
        self.df = self.db_handler.ss_read(query)

        # merge if not searching for unique values
        if do_merge:
            if not query_all:
                query = self.read_query_merge
    #             query = """\
    # SELECT row.* \
    # FROM dbo.Table_2 row \
    # INNER JOIN \
    #     (SELECT hsn, MAX(percent_cvg) AS MaxPercentCoverage \
    #     FROM dbo.Table_2 \
    #     GROUP BY hsn) grouped_row \
    # ON row.hsn = grouped_row.hsn \
    # AND row.percent_cvg = grouped_row.MaxPercentCoverage \
    # WHERE row.avg_depth >= 75\
    # """     
            else:
                query = self.read_query_merge_all
    #             query = """\
    # SELECT row.* \
    # FROM dbo.Table_2 row \
    # INNER JOIN \
    #     (SELECT hsn, MAX(percent_cvg) AS MaxPercentCoverage \
    #     FROM dbo.Table_2 \
    #     GROUP BY hsn) grouped_row \
    # ON row.hsn = grouped_row.hsn \
    # AND row.percent_cvg = grouped_row.MaxPercentCoverage \
    # """      
            #all_time_df_qc = pd.read_sql(query, con=self.db_handler.engine)
            all_time_df_qc = self.db_handler.ss_read(query)
            all_time_df_qc.drop(labels=['ID_Table_2', 'total_ns', 'percent_cvg', 'avg_depth', 'path_to_fasta'], axis=1, inplace=True)

            join_lst = ['hsn', 'wgs_run_date']
            self.df = self.df.merge(all_time_df_qc, how='inner', on=join_lst)
            self.df.drop(labels=['ID_Table_1'], axis=1, inplace=True)
            self.df = self.df[self.final_col_order]
            self.df['gisaid_num'] = self.df.apply(lambda row: get_gisaid(row), axis=1)
            self.df['facility'] = self.df.apply(lambda row: format_facility(row), axis=1)
            self.df.sort_values('wgs_run_date', inplace=True, ignore_index=True)



def get_gisaid(row):
    if not pd.isna(row['gisaid_num']):
        num = int(row['gisaid_num'])
        return f"KS-KHEL-{num:04}"
    else:
        return None


def format_facility(row):
    formatted = ""
    for x in str(row['facility']).split(" "):
        formatted += x.capitalize() + " "
    formatted = formatted.strip()
    formatted = formatted.replace("Hd", "HD")
    formatted = formatted.replace("Kjcc", "KJCC")
    formatted = formatted.replace("Llc", "LLC")
    formatted = formatted.replace("Chc", "CHC")
    formatted = formatted.replace("Sek", "SEK")
    return formatted


def format_query(query, lst):
    query_track = list(set(re.findall("{(.*?)}", query)))
    new_query = query
    for item in query_track:
        new_query = new_query.replace(item, lst[int(item[0])])


