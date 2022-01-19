from ..workflow_obj import workflow_obj
from ..formatter import format_facility
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
        df.columns = [str(col).strip().lower() for col in list(df.columns)]
        df.rename(columns=self.rename_dict, inplace=True)

        # add columns
        print("\nAdding 'path_to_fasta' column...")
        df['path_to_fasta'] = None
        print("\nAdding 'avg_depth' column...")
        df['avg_depth'] = df.apply(lambda row: get_avg_depth(row), axis=1)
        print("\nAdding 'percent_cvg' column...")
        df['percent_cvg'] = df.apply(lambda row: get_percent_cvg(row), axis=1)
        print("\nAdding 'f_name' column...")
        df['f_name'] = df.apply(lambda row: get_name(row, "first"), axis=1)
        print("\nAdding 'l_name' column...")
        df['l_name'] = df.apply(lambda row: get_name(row, "last"), axis=1)
        print("\nAdding 'platform' column...")
        df['platform'] = df.apply(lambda row: parse_seq_id(row), axis=1)
        print("\nAdding 'machine_num' column...")
        df['machine_num'] = df.apply(lambda row: parse_seq_id(row), axis=1)
        print("\nAdding 'position' column...")
        df['position'] = df.apply(lambda row: parse_seq_id(row), axis=1)
        print("\nAdding 'day_run_num' column...")
        df['day_run_num'] = df.apply(lambda row: parse_seq_id(row), axis=1)
        print("\nAdding 'gisaid_num' column...")
        df['gisaid_num'] = df.apply(lambda row: parse_gisaid_num(row), axis=1)
        df['source'] = df.apply(lambda row: format_source(row), axis=1)
        df['age'] = df.apply(lambda row: get_age(row), axis=1)
        df['sex'] = df.apply(lambda row: row['sex'].capitalize(), axis=1)
        df['state'] = df.apply(lambda row: format_state(row), axis=1)
        df['facility'] = df.apply(lambda row: row['facility'].lower(), axis=1)
        df.replace(to_replace="UNKNOWN", value = None, inplace=True)
        df.replace(to_replace="Unknown", value = None, inplace=True)
        df.replace(to_replace="unknown", value = None, inplace=True)

        # format data
        # dates
        for column in self.date_cols:
            df[column] = df.apply(lambda row: format_date(row, column), axis=1)

        for column in self.str_cols:
            df[column] = df.apply(lambda row: fix_single_quote(row, column), axis=1)
            # also strip any hiding spaces from the cells
            df[column] = df.apply(lambda row: str(row[column]).strip(), axis=1)


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
        print(self.df_table1)
        df_2_row_lst = remove_m(self.df_table2)
        self.df_table2 = pd.DataFrame(df_2_row_lst, columns = list(self.df_table2.columns))
        print(self.df_table2)
        #self.logger.info(self.id + ": get_outside_lab_dfs finished!")
        

    def database_push(self):
        #self.logger.info(self.id + ": Pushing info to database")
        # attempt to connect to database

        # pushing to database....
        super().setup_db()
        df_table1_lst = self.df_table1.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_table1_lst, query=self.write_query_tbl1, full=True, df=self.df_table1)

        df_table2_lst = self.df_table2.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_table2_lst, query=self.write_query_tbl2, full=True, df=self.df_table2)

        #self.logger.info(self.id + ": database_push finished!")




def parse_seq_id(row):
       return "-3"


def get_name(row, arg):
    names = [str(row["f_name"]).strip(), str(row["l_name"]).strip()]
    if arg == "last":
        if names[-1].lower() == "jr" or names[-1].lower() == "sr":
            return names[-2] + ", " + names[-1]
        return names[-1].capitalize()
    if arg == "first":
        return names[0].capitalize()


def format_state(row):
    if not pd.isna(row['state']):
        if row['state'].lower() == 'ks':
            return "Kansas"
        else:
            return row['state']

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
            return date2.strftime("%Y-%m-%d")
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
    result = str(row["avg_depth"]).replace("x", "")
    result = result.replace("X", "")
    return result


def get_percent_cvg(row):
    # remove percentage signs
    result = float(str(row['percent_cvg']).replace("%", ""))
    # convert to decimal percentage
    if result > 1:
        result /= 100
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
        rel_info.append(df.iloc[i][lst.index("avg_depth")]) # Next is Seq coverage
        rel_info.append(df.iloc[i][lst.index("percent_cvg")]) # Next is assembly coverage

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
            # if ((str(dup_dict[key][key2][1]) == "nan") and (str(dup_dict[key][key2][2]) == "nan") and (str(dup_dict[key][key2][3]) == "nan")):
            #     # Sample is from iSeq
            #     # Set score
            #     depth_score_curr = float(dup_dict[key][key2][6])
            #     if depth_score_curr > 0:
            #         percent_score = float(dup_dict[key][key2][5])
            #         # Check aligned bases
            #         if percent_score > score:
            #             score = percent_score
            #             best_HSN = key2
            #         elif percent_score == score:
            #             if depth_score_curr > depth_score:
            #                 depth_score = depth_score_curr
            #                 best_HSN = key2
            #         else:
            #             continue
            # else:
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
    if len(str(row['source'])) == 2:
        return str(row['source'])
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


def get_age(row):
    try:
        return int(row['age'])
    except Exception:
        try:
            born = datetime.datetime.strptime(row["dob"], "%m/%d/%Y").date()
        except Exception:
            born = row["dob"].to_pydatetime().date()

        tested = row['doc']
        if type(tested) != datetime.datetime:
            try:
                tested = tested.to_pydatetime().date()
            except Exception:
                tested = datetime.datetime.strptime(tested, "%m/%d/%Y").date()
        else:
            tested = tested.date()
        if pd.isnull(born) or pd.isnull(tested):
            return -1
        days_in_year = 365.2425   
        age = int((tested - born).days / days_in_year)
        return age