from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..ui import get_path
from ..formatter import add_cols, format_hsn_col
import datetime
import cx_Oracle as co
import pandas as pd



class WorkflowObj1(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_1"

    # methods
    def get_json(self):
        super().get_json(1)


    def get_initial_demo_df(self):
        print("\nUse the following window to open the wgs run order worksheet...")
        self.demo_path = get_path()
        self.df_right = get_pandas(self.demo_path, 'WF_1', 'run order', ',')
        # drop controls from index
        neg = False
        pos = False
        for index in range(len(self.df_right.index)):
            if "neg" in self.df_right['Sample ID'][index].lower():
                neg_idx = index
                neg = True
            if "pos" in self.df_right['Sample ID'][index].lower():
                pos_idx = index
                pos = True
            if neg and pos:
                break
        self.df_right.drop([pos_idx, neg_idx], inplace=True)


    def format_demo_df(self):
        self.df_right = format_hsn_col(\
            df=self.df_right, \
            hsn_colname='Sample ID', \
            hsn_only=True)
        

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


    # def get_initial_hsn_df(self):
    #     # attempt to connect to database
    #     super().setup_db()
    #     # What HSNs included in our dataframe already exist in the database?
    #     hsn_lst = self.df['hsn'].to_list()
    #     self.hsn_df = self.db_handler.sub_lst_read(query=self.read_query_tbl1, lst=hsn_lst)
    #     self.qr = self.hsn_df["hsn"].values.astype(str).tolist()


    # def remove_existing_hsns(self):
    #     # create new dataframe that excludes hsn's already common to database and dataframe
    #     lst = list(self.df.columns)
    #     size = self.df.index
    #     new_row = []
    #     self.already_exist = []
    #     for i in range(len(size)):
    #         # cell_val = hsn of row we are currently evaluating
    #         cell_val = str(self.df.iloc[i][lst.index("hsn")])
    #         currentrow = self.df.iloc[i]
    #         currentrow = currentrow.values.tolist()
    #         if cell_val not in self.qr:
    #             new_row.append(currentrow)
    #         else:
    #             self.already_exist.append(cell_val)
        
        # # now, transform list of non-common rows back into dataframe
        # self.df_new_rows = pd.DataFrame(new_row, columns= list(self.df.columns))
        

    def database_push(self):
        super().setup_db()
        df_demo_lst = self.df.values.astype(str).tolist()
        df_table_col_query = "(" + ", ".join(self.df.columns.astype(str).tolist()) + ")"
        self.write_query_tbl1 = self.write_query_tbl1.replace("{df_table_col_query}", df_table_col_query)
        self.db_handler.lst_ptr_push(df_lst=df_demo_lst, query=self.write_query_tbl1)
        #self.db_handler.to_sql_push(df=self.df_new_rows, tbl_name="Table_1")





