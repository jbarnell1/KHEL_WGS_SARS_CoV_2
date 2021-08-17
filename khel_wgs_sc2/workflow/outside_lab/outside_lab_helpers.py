from ..workflow_obj import workflow_obj
import time
from ..reader import get_pandas
from tkinter import filedialog
from tkinter import *
import re
import datetime
import pandas as pd
from decimal import *


class outside_lab_obj(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "outside_lab"

    # methods
    def get_json(self):
        #self.logger.info(self.id + ": Acquiring local data from cache")
        super().get_json(-3)
        #self.logger.info(self.id + ": get_json finished!")

    def get_outside_lab_dfs(self):
        print("\nUse the following window to open the excel workbook...")
        xl_path = get_path()
        #self.logger.info(self.id + ": Getting outside lab data from worksheet")
        df = get_pandas(xl_path, 'outside_lab', 'outside_lab', ',')
        all_cols = self.dbo_tbl_1_cols + list(set(self.dbo_tbl_2_cols) - set(self.dbo_tbl_1_cols))
        df.columns = [str(col).strip() for col in list(df.columns)]
        df.rename(columns=self.rename_dict, inplace=True)
        df.insert(0, "pangolin_version", None)
        df.insert(0, "nextclade_version", None)
        pd.set_option('display.max_columns', None)

        # add columns
        print("\nAdding 'path_to_fasta' column...")
        df['path_to_fasta'] = df.apply(lambda row: get_path_to_fasta(row), axis = 1)
        print("\nAdding 'avg_depth' column...")
        df['avg_depth'] = df.apply(lambda row: get_avg_depth(row), axis=1)
        print("\nAdding 'percent_cvg' column...")
        df['percent_cvg'] = df.apply(lambda row: get_percent_cvg(row), axis=1)
        print("\nAdding 'f_name' column...")
        df['f_name'] = df.apply(lambda row: get_name(row, "first"), axis=1)
        print("\nAdding 'l_name' column...")
        df['l_name'] = df.apply(lambda row: get_name(row, "last"), axis=1)
        print("\nAdding 'pango_learn_version' column...")
        df.insert(0, "pango_learn_version", None)
        print("\nAdding 'platform' column...")
        df['platform'] = df.apply(lambda row: parse_seq_id(row, "platform"), axis=1)
        print("\nAdding 'machine_num' column...")
        df['machine_num'] = df.apply(lambda row: parse_seq_id(row, "machine_num"), axis=1)
        print("\nAdding 'position' column...")
        df['position'] = df.apply(lambda row: parse_seq_id(row, "position"), axis=1)
        print("\nAdding 'day_run_num' column...")
        df['day_run_num'] = df.apply(lambda row: parse_seq_id(row, "day_run_num"), axis=1)
        print("\nAdding 'gisaid_num' column...")
        df['gisaid_num'] = df.apply(lambda row: parse_gisaid_num(row), axis=1)
        df['source'] = df.apply(lambda row: format_source(row), axis=1)
        df.replace(to_replace="UNKNOWN", value = None, inplace=True)
        df.replace(to_replace="Unknown", value = None, inplace=True)
        df.replace(to_replace="unknown", value = None, inplace=True)

        # format data
        # dates
        for column in self.date_cols:
            df[column] = df.apply(lambda row: format_date(row, column), axis=1)

        for column in self.str_cols:
            df[column] = df.apply(lambda row: fix_single_quote(row, column), axis=1)

        print(df)

        # sort/remove columns into the two dataframes
        self.df_table1 = pd.DataFrame(df)
        self.df_table2 = pd.DataFrame(df, columns=self.dbo_tbl_2_cols)


        # clean up the indices 
        # dbo.Table_1:
        #   - select best duplicate
        #   - remove letter from HSN
        # 
        # dbo.Table_2:
        #   - keep all hsn duplicates
        #   - remove letter from HSN

        self.df_table1 = remove_dups(self.df_table1)
        self.df_table1 = pd.DataFrame(self.df_table1, columns=self.dbo_tbl_1_cols)
        self.df_table1['hsn'] = self.df_table1.apply(lambda row: drop_letter(row), axis=1)

        self.df_table2['hsn'] = self.df_table2.apply(lambda row: drop_letter(row), axis=1)
        df_2_row_lst = remove_m(self.df_table2)
        self.df_table2 = pd.DataFrame(df_2_row_lst, columns = list(self.df_table2.columns))
        #self.logger.info(self.id + ": get_outside_lab_dfs finished!")
        

    def database_push(self):
        #self.logger.info(self.id + ": Pushing info to database")
        # attempt to connect to database

        # pushing to database....
        super().database_push()
        df_table1_lst = self.df_table1.values.astype(str).tolist()
        self.db_handler(df_lst=df_table1_lst, query=self.write_query_tbl1, full=True, df=self.df_table1)

        df_table2_lst = self.df_table2.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_table2_lst, query=self.write_query_tbl1, full=True, df=self.df_table2)

        #self.logger.info(self.id + ": database_push finished!")




def parse_seq_id(row, arg):
    # if iseq
    if re.search("^KS-M\d{4}-\d{6}$", str(row['seq_run_id'])) or re.search("^\d{6}$", str(row['seq_run_id'])):
        if arg == "platform":
            return "iSeq"
        elif arg == "machine_num":
            return -1
        elif arg == "position":
            return -1
        elif arg == "day_run_num":
            return "01"
        
    # if ClearLabs
    elif re.search("^CL-BHRL\d{2}-\d{6}$", str(row['seq_run_id'])) or re.search("^BHRL\d{2}.\d{4}-\d{2}-\d{2}.\d{2}$", str(row['seq_run_id'])) or re.search("^BB1L\d{2}.\d{4}-\d{2}-\d{2}.\d{2}$", str(row['seq_run_id'])):
        if arg == "platform":
            return "ClearLabs"
        elif arg == "machine_num":
            if re.search("CL-BHRL\d{2}-\d{6}", str(row['seq_run_id'])):
                return str(row['seq_run_id'])[7:9]
            else:
                return str(row['seq_run_id'])[4:6]
        elif arg == "position":
            if re.search("CL-BHRL\d{2}-\d{6}", str(row['seq_run_id'])):
                if str(row['seq_run_order']) != 'nan':
                    return row['seq_run_order'][-2:]
                else:
                    return -2
            else:
                return row['seq_run_order'][-2:]
        elif arg == "day_run_num":
            if re.search("CL-BHRL\d{2}-\d{6}", str(row['seq_run_id'])):
                return '1'
            else:
                return row['seq_run_id'][-2:]
    # outside lab/unknown
    else:
       return "-3"


def get_name(row, arg):
    full_name = str(row["name"]).strip()
    names = full_name.split(" ")
    if arg == "last":
        if names[-1].lower() == "jr" or names[-1].lower() == "sr":
            return names[-2] + ", " + names[-1]
        return names[-1]
    if arg == "first":
        return names[0]


def get_path_to_fasta(row):
    return None


def format_date(row, colName):
    date1 = row[colName]
    if (isinstance(date1, pd.Timestamp)) or\
        (isinstance(date1, datetime.datetime)):
        if (not pd.isna(date1)):
            return date1.strftime("%Y-%m-%d")
        else:
            return None
    else:
        if type(date1) == str:
            date2 = datetime.datetime.strptime(date1, "%m/%d/%Y")
            return datetime.datetime.strftime(date2, "%Y-%m-%d")
        else:
            return None


def get_path():
    time.sleep(1)
    print("Opening dialog box...")
    time.sleep(2)
    root = Tk()
    root.withdraw()
    path_read = filedialog.askopenfilename()
    return path_read


def get_avg_depth(row):
    # remove the 'times' symbol, convert to int and return
    result = str(row["seq_coverage"]).replace("x", "")
    result = result.replace("X", "")
    return result


def get_percent_cvg(row):
    # remove percentage signs
    result = float(str(row['assembly_coverage']).replace("%", ""))
    # convert to decimal percentage
    if result <= 1:
        result *= 100
    return f'{result:.2f}'


def remove_dups(df):
    lst = filter_dups(df)
    df = lst[0]
    removed_lst = lst[1]
    return df


def filter_dups(df):
    # build dictionary of all samples
    dup_dict = build_sample_dict(df)
    # get a list of HSNs of the best run of each sample
    sample_lst = []
    sample_lst = select_best_HSN(df, dup_dict)
    
    # build both dataframes from original list 
    dataframes = []
    dataframes = make_dataframes(df, sample_lst)
    row_list = dataframes[0]
    dup_row_list = dataframes[1]
    
    # convert both lists to dataframes
    df_copy = pd.DataFrame(row_list, columns = list(df.columns))
    dup_df = pd.DataFrame(dup_row_list, columns = list(df.columns))
    
    results = []
    results.append(df_copy)
    results.append(dup_df)
    return results


def build_sample_dict(df):
    lst = list(df.columns)
    # Set regex pattern
    size = df.index
    # Change type of HSN column
    df["hsn"] = df["hsn"].astype(str)
    dup_dict = {}

    # build the sample dictionary
    for i in range(len(size)):
        if i % 400 == 0:
            print("working... finished row " + str(i) +" out of " + str(len(size)) + ".")
        cell_val = str(df.iloc[i][lst.index("hsn")])
        HSN_arr = cell_val.split(".")
        HSN = HSN_arr[0]
        currentrow = df.iloc[i]
        currentrow = currentrow.values.tolist()

        # grab the relevant info (to choose which duplicate is best)
        rel_info = []
        rel_info.append(df.iloc[i][lst.index("gisaid_num")]) # First element in list is GISAID #
        rel_info.append(df.iloc[i][lst.index("total_ns")]) # Next is Total Ns
        rel_info.append(df.iloc[i][lst.index("seq_coverage")]) # Next is Seq coverage
        rel_info.append(df.iloc[i][lst.index("assembly_coverage")]) # Next is assembly coverage
        rel_info.append(df.iloc[i][lst.index("aligned_bases")]) # Next is Aligned bases (iSeq)
        rel_info.append(df.iloc[i][lst.index("percent_cvg")]) # Next is percent_cvg (iSeq)
        rel_info.append(df.iloc[i][lst.index("mean_depth")]) # Next is mean depth (iSeq)


        # if copy has been created in dictionary tracker already
        if HSN in dup_dict:
            # insert data into secondary dict with full HSN identifier
            dup_dict[HSN][cell_val] = rel_info
        else:
            # create the new dictionary
            new_dict = {}
            new_dict[cell_val] = rel_info
            dup_dict[HSN] = new_dict
    return dup_dict


def select_best_HSN(df, dup_dict):
    # create list of best version of sample
    add_back = [] # will be list of HSNs
    for key in dup_dict:
        # Set/reset initial quality score
        score = 0
        depth_score = 0
        best_HSN = ""
        for key2 in dup_dict[key]:
            if ((str(dup_dict[key][key2][1]) == "nan") and (str(dup_dict[key][key2][2]) == "nan") and (str(dup_dict[key][key2][3]) == "nan")):
                # Sample is from iSeq
                # Set score
                depth_score_curr = float(dup_dict[key][key2][6])
                if depth_score_curr > 0:
                    percent_score = float(dup_dict[key][key2][5])
                    # Check aligned bases
                    if percent_score > score:
                        score = percent_score
                        best_HSN = key2
                    elif percent_score == score:
                        if depth_score_curr > depth_score:
                            depth_score = depth_score_curr
                            best_HSN = key2
                    else:
                        continue
            else:
                # Sample is from clearlabs
                # Set score
                depth_score_curr = float(str(dup_dict[key][key2][2]).lower().replace("x",""))
                if depth_score_curr > 0:
                    cov_score = float(dup_dict[key][key2][3])
                    # test scores against one another
                    if cov_score > score:
                        score = cov_score
                        depth_score = depth_score_curr
                        best_HSN = key2
                    elif cov_score == score:
                        if depth_score_curr > depth_score:
                            depth_score = depth_score_curr
                            best_HSN = key2
                    else:
                        continue
        add_back.append(best_HSN)
    # remove empty strings from list
    add_back[:] = [x for x in add_back if x]
    return add_back


def make_dataframes(df, add_back):
     # generate two lists
    # row_list is all accepted samples
    # dup_row_list is all rejected duplicates
    lst = list(df.columns)
    size = df.index
    row_list = []
    dup_row_list = []
    for i in range(len(size)):
        if i % 400 == 0:
            print("working... finished row " + str(i) + " out of " + str(len(size)) + ".")
        cell_val = str(df.iloc[i][lst.index("hsn")])
        currentrow = df.iloc[i]
        currentrow = currentrow.values.tolist()
        if cell_val in add_back and not re.search(".*M.*", str(cell_val)):
            row_list.append(currentrow)
        else:
            dup_row_list.append(currentrow)
    results = []
    results.append(row_list)
    results.append(dup_row_list)
    return results


def drop_letter(row):
    HSN = str(row["hsn"])
    HSN = HSN[:-2]
    return HSN


def parse_gisaid_num(row):
    try:
        rv = int(row['gisaid_num'][-4:])
    except Exception:
        rv = None
    return rv


def remove_m(df):
    lst = list(df.columns)
    size = df.index
    row_list = []
    for i in range(len(size)):
        cell_val = str(df.iloc[i][lst.index("hsn")])
        currentrow = df.iloc[i]
        currentrow = currentrow.values.tolist()
        if  not re.search(".*M.*", str(cell_val)):
            row_list.append(currentrow)
    return row_list


def fix_single_quote(row, column):
    return str(row[column]).strip().replace("'", "''")


def format_source(row):
    if str(row['source']).lower() == "nasopharygeal":
        return "NP"
    elif str(row['source']).lower() == "nasopharnygeal":
        return "NP"
    elif str(row['source']).lower() == "unknown":
        return "OT"
    elif str(row['source']).lower() == "saliva":
        return "SV"
    else:
        return "OT"