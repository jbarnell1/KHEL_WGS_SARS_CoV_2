from ..workflow_obj import workflow_obj
from ..writer import save_epi_csv
from ..formatter import add_cols, cap_all, format_sex, unkwn
import datetime



class WorkflowObj6(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_6"

    # methods
    def get_json(self):
        super().get_json(6)


    def get_ui(self):
        while True:
            user_selection = input("Would you like to select all data (type 'a'), a range (type 'r'),\
                \na single date (type 'd'), samples submitted from a given lab (type 's'),\
                \nor all samples from a given facility (type 'f')?    ")
            if user_selection.lower() == 'r':
                date_start = input('Enter the start date in YYYY-MM-DD format (include dashes):    ')
                year, month, day = map(int, date_start.split('-'))
                date_start = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                date_end = input('Enter the end date in YYYY-MM-DD format (include dashes):    ')
                year, month, day = map(int, date_end.split('-'))
                date_end = datetime.datetime(year, month, day).strftime("%Y-%m-%d")

                self.read_date_query_tbl1 = self.read_date_query_tbl1.replace("{start}", date_start)
                self.query = self.read_date_query_tbl1.replace("{end}", date_end)
                break
            elif user_selection.lower() == 'd':
                date_start = input('Enter the date in YYYY-MM-DD format (include dashes):   ')
                year, month, day = map(int, date_start.split('-'))
                date_start = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                date_end = date_start

                self.read_date_query_tbl1 = self.read_date_query_tbl1.replace("{start}", date_start)
                self.query = self.read_date_query_tbl1.replace("{end}", date_end)
                self.query = self.query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))

                self.bad_query = self.read_bad_date_query_tbl1.replace("{start}", date_start)
                self.bad_query = self.bad_query.replace("{end}", date_end)
                self.bad_query = self.bad_query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                break
            elif user_selection.lower() == 'a':
                self.a = True
                break
            elif user_selection.lower() == 'f':
                user_selection = input("Please enter the facility to filter samples by:    ")
                self.query = self.read_facility_query_tbl1.replace("{facility}", user_selection)
                break
            elif user_selection.lower() == 's':
                user_selection = input("Please enter the submitting facility to filter samples by:    ")
                self.query = self.read_sfacility_query_tbl1.replace("{sub_facility}", user_selection)
                break
            else:
                continue



    def get_df(self):
        super().setup_db()
        self.df = self.db_handler.ss_read(query=self.query)
        self.bad_df = self.db_handler.ss_read(query=self.bad_query)
        #TODO fill out rest of functionality

    def format_df(self):
        # rename/drop/add/sort appropriate columns
        self.df = self.df.rename(columns = self.rename_col_lst)
        self.df = add_cols(obj=self, \
            df = self.df, \
            col_lst = self.csv_headers, \
            col_func_map = self.col_func_map)
        
        self.df = self.df[self.csv_headers]
        # format values appropriately
        self.df = clean_df(self.df)

        # format bad df
        self.bad_df = add_cols(obj=self, \
            df = self.bad_df, \
            col_lst = self.csv_headers, \
            col_func_map= self.col_func_map)
        self.bad_df = self.bad_df[self.bad_df_headers]
        self.bad_df = clean_df(self.bad_df)

    
    def write_epi_report(self):
        # save both files to csv
        today = datetime.datetime.today().strftime("%m%d%y")
        path = self.folderpathbase + "\\" + today
        save_epi_csv(self.df, self.bad_df, path)


def clean_df(df):
    for col in df.columns:
        #switch unkwns to "" and nans to "";
        # format all dates as mm/dd/yyyy
        if col == "Patient_Gender":
            # Patient Gender needed?
            df[col] = df.apply(lambda row: format_sex(row, ber=True), axis=1)
        elif col == "Ordering_Facility":
            df[col] = df.apply(lambda row: cap_all(row, col), axis=1)
        else:
            df[col] = df.apply(lambda row: unkwn(row, col), axis=1)
    return df