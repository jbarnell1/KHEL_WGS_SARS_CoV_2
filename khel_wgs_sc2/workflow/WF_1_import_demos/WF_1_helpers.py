from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..ui import get_path
from ..formatter import add_cols, format_hsn_col
import datetime
import cx_Oracle as co
import pandas as pd



class WorkflowObj1(workflow_obj):
    # constructor
    def __init__(self, logger):
        self.id = "WF_1"
        self.logger = logger

    # methods
    def get_json(self):
        self.logger.info(f"{self.id}: Acquiring local data from cache")
        super().get_json(1)
        self.logger.info(f"{self.id}: get_json finished!")


    def get_initial_demo_df(self):
        print("\nUse the following window to open the wgs run order worksheet...")
        self.demo_path = get_path()
        self.logger.info(f"{self.id}: Getting demographics from worksheet")
        self.df_right = get_pandas(self.demo_path, 'WF_1', 'run order', ',', self.logger)
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
        
        self.logger.info(f"{self.id}: get_demo_df finished!")


    def format_demo_df(self):
        self.logger.info(f"{self.id}: formatting data inside df.right")
        self.df_right = format_hsn_col(\
            df=self.df_right, \
            hsn_colname='Sample ID', \
            hsn_only=True)
        self.logger.info(f"{self.id}: format_demo_df finished!")
        

    def get_initial_lims_df(self):
        self.logger.info(f"{self.id}: Getting demographics from LIMS")
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
        self.logger.info(f"{self.id}: get_lims_df finished!")


    def format_lims_df(self):
        self.logger.info(f"{self.id}: Formatting demographics from LIMS")
        # manipulate sql database to format accepted by the master EXCEL worksheet
        print("\nManipulating demographics to database format...")
        self.df = self.df.rename(columns = self.demo_names)
        self.df["hsn"] = self.df.apply(lambda row: str(row["hsn"]), axis=1)
        print(" Done!\n")
        self.logger.info(f"{self.id}: get_lims_demos finished!")

    def merge_dfs(self):
        self.logger.info(f"{self.id}: Merging dataframes from LIMS and run order sheet")
        print("\nMerging dataframes...")
        self.df = pd.merge(self.df, self.df_right, how="right", on="hsn")
        print(" Done!\n")
        self.logger.info(f"{self.id}: merge_dfs finished!")

    
    def format_dfs(self):
        self.logger.info(f"{self.id}: Formatting joined dataframes")
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

        self.logger.info(f"{self.id}: format_dfs finished!")
        # sort/remove columns to match list
        self.df = self.df[self.sample_data_col_order]


    def get_initial_hsn_df(self):
        self.logger.info(f"{self.id}: getting HSNs common to database and df")
        # attempt to connect to database
        self.logger.info(f'{self.id}: Querying data from database')
        super().setup_db()
        # What HSNs included in our dataframe already exist in the database?
        hsn_lst = self.df['hsn'].to_list()
        self.hsn_df = self.db_handler.sub_lst_read(query=self.read_query_tbl1, lst=hsn_lst)
        self.qr = self.hsn_df["hsn"].values.astype(str).tolist()
        self.logger.info(f"{self.id}: get_initial_hsn_df finished!")


    def remove_existing_hsns(self):
        self.logger.info(f"{self.id}: removing HSNs from df that are already in database")
        # create new dataframe that excludes hsn's already common to database and dataframe
        lst = list(self.df.columns)
        size = self.df.index
        new_row = []
        self.already_exist = []
        for i in range(len(size)):
            # cell_val = hsn of row we are currently evaluating
            cell_val = str(self.df.iloc[i][lst.index("hsn")])
            currentrow = self.df.iloc[i]
            currentrow = currentrow.values.tolist()
            if cell_val not in self.qr:
                new_row.append(currentrow)
            else:
                self.already_exist.append(cell_val)
        
        # now, transform list of non-common rows back into dataframe
        self.df_new_rows = pd.DataFrame(new_row, columns= list(self.df.columns))
        self.logger.info(f"{self.id}: remove_existing_hsns finished!")
        

    def database_push(self):
        self.logger.info(f"{self.id}: Pushing df to database")
        self.db_handler.to_sql_push(df=self.df_new_rows, tbl_name="Table_1")
        self.logger.info(f"{self.id}: database_push finished!")





