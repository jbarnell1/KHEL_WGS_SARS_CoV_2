from ..workflow_obj import workflow_obj
from ..reader import get_pandas, read_txt
from ..ui import get_path
from ..formatter import add_cols, format_hsn_col
import datetime
import cx_Oracle as co
import pandas as pd



class WorkflowObj1(workflow_obj):
    # constructor
    def __init__(self): #self helps python know its part of that class
        self.id = "WF_1"

    # methods
    def get_json(self):
        super().get_json(1)


    def get_priority(self):
        print("\nGetting list of priority samples...")
        lines = read_txt(self.priority_path)
        self.priority_lst = [line.strip("* \n") for line in lines]
        print(" Done!\n")

    def verify_ctrls(self):
        today = datetime.datetime.today()
        print("\nVerifying control expiration dates...")
        if datetime.datetime.strptime(self.pos_ctrl_exp, "%Y-%m-%d") <= today:
            print("ALERT!! The positive control is out of spec!  Please update in data/private_cache.json")
            raise ValueError("Positive Control is invalid- already expired")
        if datetime.datetime.strptime(self.neg_ctrl_exp, "%Y-%m-%d") <= today:
            print("ALERT!! The negative control is out of spec!  Please update in data/private_cache.json")
            raise ValueError("Positive Control is invalid- already expired")
        print(" Done!\n")


    def get_initial_demo_df(self):
        print("\nUse the following window to open the Sample ID Upload worksheet...")
        self.demo_path = get_path()
        self.df_right = get_pandas(self.demo_path, 'WF_1', 'run order', ',')
        self.df_right = self.df_right.applymap(str)
        # drop controls from index
        neg = False
        pos = False
        for row in range(len(self.df_right.index)):
            if "neg" in self.df_right['Sample ID'][row].lower():
                neg_idx = row
                neg = True
            if "pos" in self.df_right['Sample ID'][row].lower():
                pos_idx = row
                pos = True
            if neg and pos:
                break
        if neg:
            self.df_right.drop([neg_idx], inplace=True)
        if pos:
            self.df_right.drop([pos_idx], inplace=True)


    def format_demo_df(self):
        self.df_right = format_hsn_col(self.df_right, hsn_colname='Sample ID', hsn_only=True)
        

    def get_initial_lims_df(self):
        # establish connection
        print("\nEstablishing database connection...")
        conn = co.connect(self.lims_conn)
        print(" Done!\n")

        # query the database
        print("\nQuerying database...")
        hsn_lst = list(self.df_right['hsn'])
        valid_hsn_lst = []
        for item in hsn_lst:
            try:
                item = int(item)
                valid_hsn_lst.append(str(item))
            except:
                pass
        hsn_lst_query = "(" + ",".join(valid_hsn_lst) + ")"
        query = "select * from wgsdemographics where HSN in " + hsn_lst_query
        self.df = pd.read_sql(query, conn)
        conn.close()
        print(" Done!\n")


    def format_lims_df(self):
        # manipulate sql database to format accepted by the master EXCEL worksheet
        print("\nManipulating demographics to database format...")
        self.df = self.df.rename(columns = self.demo_names)
        self.df["hsn"] = self.df.apply(lambda row: str(row["hsn"]), axis=1)
        print(" Done!\n")

    def merge_dfs(self):
        print("\nMerging dataframes...")
        self.df = pd.merge(self.df, self.df_right, how="right", on="hsn")
        print(" Done!\n")


    def format_dfs(self):
        # get the date for wgs_run_date column
        path_arr = self.demo_path.split("/")
        name = path_arr[-1]
        date_input = name[3:5] + "-" + name[5:7] + "-20" + name[7:9]
        self.wgs_run_date = datetime.datetime.strptime(date_input, '%m-%d-%Y')
        self.wgs_run_date = self.wgs_run_date.strftime("%m/%d/%Y")
        # format columns, insert necessary values
        print("\nAdding/Formatting/Sorting columns...")

        self.df = add_cols(obj=self, \
            df=self.df, \
            col_lst=self.add_col_lst, \
            col_func_map=self.col_func_map)

        # sort/remove columns to match list
        self.df = self.df[self.sample_data_col_order]
        

    def database_push(self):
        super().setup_db()
        df_demo_lst = self.df.values.astype(str).tolist()
        df_table_col_query = "(" + ", ".join(self.df.columns.astype(str).tolist()) + ")"
        self.write_query_tbl1 = self.write_query_tbl1.replace("{df_table_col_query}", df_table_col_query)
        self.db_handler.lst_ptr_push(df_lst=df_demo_lst, query=self.write_query_tbl1)




