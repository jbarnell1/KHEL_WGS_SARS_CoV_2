from ..workflow_obj import workflow_obj
from ..ui import get_path
from ..reader import get_pandas
import re



class epi_isl_obj(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "epi_isl"


    # methods
    def get_json(self):
        super().get_json(-1)


    def get_epi_isl_dfs(self):
        # open demo path --> pandas dataframe
        print("\nUse the following window to open the epi_isl results workbook...\n")
        epi_isl_path = get_path()
        self.df = get_pandas(epi_isl_path, self.id, self.id, '\t')
        print("Renaming columns...")
        self.df = self.df.rename(columns=self.rename_epi_isl_cols_lst)
        print(" Done!\n")
        # add columns
        self.df["gisaid_num"] = self.df.apply(lambda row: parse_gisaid_num(row), axis=1)
        # remove columns/split dataframes
        self.df = self.df[self.full_lst]
        self.df = self.df[~self.df.gisaid_num.isnull()]


    def database_push(self):
        # self.logger.info("epi_isl: Pushing info to database")
        # # attempt to connect to database
        # #select * from table 2 where hsn in df_qc hsns and has maximum coverage and > 75x depth
        super().setup_db()
        df_epi_isl_lst = self.df.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_epi_isl_lst, query=self.write_query_tbl1)
        #self.logger.info(self.id + ": database_push finished!")


def parse_gisaid_num(row):
    gisaid_num = None
    if re.search("hCoV-19/USA/KS-KHEL-\d{4}/\d{4}", row['Virus name']):
        gisaid_num = int(row['Virus name'][20:24])
    return gisaid_num
