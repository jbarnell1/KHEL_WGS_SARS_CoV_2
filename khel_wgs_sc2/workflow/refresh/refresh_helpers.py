from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..ui import progressBar
from ..formatter import remove_pools
import time
from tkinter import filedialog
from tkinter import *
import os
import re
import datetime
import pandas as pd
from decimal import *


class refresh_obj(workflow_obj):
    # constructor
    def __init__(self, logger):
        self.logger = logger
        self.id = "refresh"
    
    # methods
    def get_json(self):
        self.logger.info(self.id + ": Acquiring local data from cache")
        super().get_json(-5)
        self.logger.info(self.id + ": get_json finished!")

    def get_refresh_dfs(self):
        print("\nUse the following window to open the excel workbook...")
        xl_path = get_path()
        self.logger.info(self.id + ": Getting outside lab data from worksheet")
        df = get_pandas(xl_path, 'refresh', 'refresh', ',', self.logger)
        df.rename(columns=self.rename_dict, inplace=True)


        neg_ctrl_lst = []
        pos_ctrl_lst = []
        panel_lst = []
        # rename controls to appropriate format for database
        for index in range(len(df.index)):
            if "neg" in str(df['hsn'][index]).lower():
                neg_ctrl_lst.append(index)
            if "pos" in str(df['hsn'][index]).lower():
                pos_ctrl_lst.append(index)
            if "panel" in str(df['hsn'][index]).lower():
                panel_lst.append(index)
        df.drop(neg_ctrl_lst, inplace=True)
        df.drop(pos_ctrl_lst, inplace=True)
        df.drop(panel_lst, inplace=True)

        # add columns
        df = remove_pools(df, 'hsn')
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
        df['platform'] = df.apply(lambda row: parse_seq_id_refresh(row, "platform"), axis=1)
        print("\nAdding 'machine_num' column...")
        df['machine_num'] = df.apply(lambda row: parse_seq_id_refresh(row, "machine_num"), axis=1)
        print("\nAdding 'position' column...")
        df['position'] = df.apply(lambda row: parse_seq_id_refresh(row, "position"), axis=1)
        print("\nAdding 'day_run_num' column...")
        df['day_run_num'] = df.apply(lambda row: parse_seq_id_refresh(row, "day_run_num"), axis=1)
        print("\nAdding 'gisaid_num' column...")
        df['gisaid_num'] = df.apply(lambda row: parse_gisaid_num(row), axis=1)
        df.replace(to_replace="UNKNOWN", value = None, inplace=True)
        df.replace(to_replace="Unknown", value = None, inplace=True)
        df.replace(to_replace="unknown", value = None, inplace=True)

        # format data
        # dates
        for column in self.date_cols:
            df[column] = df.apply(lambda row: format_date(row, column), axis=1)
        
        # sex
        df['sex'] = df.apply(lambda row: format_sex(row), axis=1)

        # name
        df['f_name'] = df.apply(lambda row: format_name(row, 'f_name'), axis=1)
        df['l_name'] = df.apply(lambda row: format_name(row, 'l_name'), axis=1)

        # facility
        df['facility'] = df.apply(lambda row: format_facility(row), axis=1)
        df['facility_category'] = df.apply(lambda row: parse_category(row), axis=1)

        # source
        df['source'] = df.apply(lambda row: format_source(row), axis=1)

        # race
        df['race'] = df.apply(lambda row: format_race(row), axis=1)

        for column in self.str_cols:
            df[column] = df.apply(lambda row: fix_single_quote(row, column), axis=1)

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
        self.logger.info(self.id + ": get_refresh_dfs finished!")

    def database_clear(self):
        super().setup_db()
        self.db_handler.clear_db()


    def database_push(self):
        self.logger.info(self.id + ": Pushing info to database")
        # pushing to database....
        df_table1_lst = self.df_table1.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_table1_lst, query=self.write_query_tbl1, full=True, df=self.df_table1)

        df_table2_lst = self.df_table2.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_table2_lst, query=self.write_query_tbl2, full=True, df=self.df_table2)
        
        self.logger.info(self.id + ": database_push finished!")



def parse_seq_id_refresh(row, arg):
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
    # if iseq
    if re.search("KS-M\d{4}-\d{6}", str(row['seq_run_id'])) or re.search("\d{6}", str(row['seq_run_id'])):
        #TODO
        return None

    # if ClearLabs
    elif re.search("CL-BHRL\d{2}-\d{6}", str(row['seq_run_id'])) or re.search("BHRL\d{2}.\d{4}-\d{2}-\d{2}.\d{2}", str(row['seq_run_id'])) or re.search("BB1L\d{2}.\d{4}-\d{2}-\d{2}.\d{2}", str(row['seq_run_id'])):
        base_path = "\\\\kdhe\\dfs\\DHEL Shared\\Diagnostic Microbiology\\WGS\\SARS-CoV-2\\ClearLabs downloads\\"
        if re.search("CL-BHRL\d{2}-\d{6}", str(row['seq_run_id'])):
            run_date = str(row['seq_run_id'])[12:14] + str(row['seq_run_id'])[14:] + str(row['seq_run_id'])[10:12]
            machine_num = str(row['seq_run_id'])[7:9]
        else:
            run_date = str(row['seq_run_id'])[12:14] + str(row['seq_run_id'])[15:17] + str(row['seq_run_id'])[9:11]
            machine_num = str(row['seq_run_id'])[4:6]
            day_run_num = str(int(str(row['seq_run_id'])[-2:]))
        
        position = str(row['seq_run_order'])[-2:]
        # after this date, we include day run number in the folder name
        if int(run_date[-2:] + run_date[:2] + run_date[2:4]) > 210729:
            folder = run_date + "." + machine_num + day_run_num + "\\"
        else:
            folder = run_date + "." + machine_num + "\\"
        
        # find out the folder structure
        if os.path.exists(base_path + folder + "FAST files"):
            if (int(folder[4:6] + folder[0:2] + folder[2:4]) >= int("210405") or folder == "030221.12\\" or folder == "040121.11\\" or folder == "031221.12\\" or folder == "022621.12\\" or folder == "032321.11\\" or folder == "022521.11\\" or folder == "030921.12\\" or folder == "032421.11\\" or folder == "031621.12\\") and not (folder == "041521.12\\" or folder == "040821.12\\"):
                # new file structure includes .A designations
                path = base_path + folder + "FAST files\\" + str(row['hsn']) + "." + str(row['seq_run_id']) + ".barcode" + str(position) + ".fasta"
            else:
                path = base_path + folder + "FAST files\\" + str(row['hsn'])[0:7] + "." + str(row['seq_run_id']) + ".barcode" + str(position) + ".fasta"
        else:
            folder2 = str(row['hsn'])[0:7] + "." + str(row['seq_run_id'])
            # old file structure
            if int(folder[4:6] + folder[0:2] + folder[2:4]) == int("210222"):
                path = base_path + folder + folder2 + ".fasta\\" + folder2 + ".barcode" + str(position) + ".fasta"
            else:
                path = base_path + folder + folder2 + ".fasta\\barcode" + str(position) + ".fasta"

        return path
 

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


def format_race(row):
    if pd.isna(row['race']):
        return "Unknown"
    elif row['race'] == "":
        return "Unknown"
    elif str(row['race']).upper() == "W":
        return "White"
    else:
        return str(row['race'])


def format_name(row, arg):
    if pd.isna(row[arg]):
        return None
    elif row[arg] == "":
        return None
    else:
        return str(row[arg]).capitalize()


def format_facility(row):
    if pd.isna(row['facility']):
        return None
    elif row['facility'] == "":
        return None
    else:
        facility = facility = str(row['facility']).lower()
        facility = facility.replace("community health center", "CHC")
        facility = facility.replace("comm hlth ctr", "CHC")
        facility = facility.replace("comm health ctr", "CHC")
        facility = facility.replace("comm health center", "CHC")
        facility = facility.replace("health department", "HD")
        facility = facility.replace("health dept", "HD")
        facility = facility.replace("hlth dept", "HD")
        facility = facility.replace("health clinic", "Hlth Clinic")
        facility = facility.replace("medical center", "Med Ctr")
        facility = facility.replace("med center", "Med Ctr")
        facility = facility.replace("medical ctr", "Med Ctr")
        facility = facility.replace("health center", "Hlth Ctr")
        facility = facility.replace("health ctr", "Hlth Ctr")
        facility = facility.replace("hlth center", "Hlth Ctr")
        facility = facility.replace("correctional facility", "Corr Fac")
        facility = facility.replace("corr facility", "Corr Fac")
        facility = facility.replace("correctional fac", "Corr Fac")
        facility = facility.replace("memorial hospital", "Mem Hosp")
        facility = facility.replace("mem hospital", "Mem Hosp")
        facility = facility.replace("memorial hosp", "Mem Hosp")
        facility = facility.replace("community", "Comm")
        facility = facility.replace("county", "Co")
        facility = facility.replace("hospital", "Hosp")
        facility = facility.replace("regional", "Reg")
        facility = facility.replace("medical", "Med")
        facility = facility.replace("kansas juvenile correctional complex", "kjcc")
        return facility.lower()


def parse_category(row):
    facility = str(row['facility']).lower()
    if re.search("hosp", facility) or re.search("med ctr", facility):
        return "Hospital"
    elif re.search("corr fac", facility) or re.search("detention unit", facility) or re.search("jail", facility) or facility == "kjcc":
        return "Correctional Facility"
    elif re.search("hd", facility):
        return "Health Department"
    elif re.search("school", facility):
        return "School"
    elif re.search("hlth ctr", facility) or re.search(" chc", facility):
        return "Health Center"
    elif re.search("clinic", facility):
        return "Clinic"
    elif re.search("lab", facility):
        return "Laboratory"
    elif re.search("fire dept", facility):
        return "Fire Department"
    elif re.search("resort", facility):
        return "Resort"
    else:
        return None


def format_source(row):
    source = str(row['source']).lower()
    if len(source) > 2:
        if source == "nasopharyngeal":
            return "NP"
        elif source == "sputum/saliva":
            return "SV"
        else:
            return "OT"
    else:
        return row['source']


def format_sex(row):
    if pd.isna(row['sex']) or str(row['sex']).upper() == "" or str(row['sex']).upper() == "UNKOWN":
        return "Unknown"
    elif str(row['sex']).upper() == "M":
        return "Male"
    elif str(row['sex']).upper() == "F":
        return "Female"
    else:
        val = str(row['sex']).capitalize().strip()
        return val


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
    print("\nBuilding list of every sample's runs...")
    for i in progressBar(range(len(size)), prefix='Progress:', suffix='Complete', length=50):
        #if i % 400 == 0:
            #print("working... finished row " + str(i) +" out of " + str(len(size)) + ".")
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
    print("\nSeparating good runs from bad runs...")
    for i in progressBar(range(len(size)), prefix='Progress:', suffix='Complete', length=50):
        #if i % 400 == 0:
            #print("working... finished row " + str(i) + " out of " + str(len(size)) + ".")
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
    if len(str(HSN)) > 7:
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