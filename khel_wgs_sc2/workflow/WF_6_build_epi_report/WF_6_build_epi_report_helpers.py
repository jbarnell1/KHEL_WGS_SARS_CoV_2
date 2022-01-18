from ..workflow_obj import workflow_obj
from ..writer import save_epi_csv, save_csv
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
        self.bad = False
        if not self.reportable:
            print("\n==========================================",
                    "\nALERT! You are generating a report for",
                    "\n------------------"
                    "\nSURVEILLANCE ONLY."
                    "\n------------------",
                    "\nIf you wish to report the results to",
                    "\nHORIZON, please change the 'reportable' variable",
                    "\nin the static_cache.json file to a 1.",
                    "\n==========================================\n")
        while True:
            self.user_selection = input("Would you like to select all data (type 'a'), a range (type 'r'),\
                \na single date (type 'd'), samples submitted from a given lab (type 's'),\
                \nall samples submitted by a given date (type 'sd'), or all samples from a given facility (type 'f')?\n--> ")
            if self.user_selection.lower() == 'd':
                date_start = input('Enter the date in YYYY-MM-DD format (include dashes):\n--> ')
                year, month, day = map(int, date_start.split('-'))
                date_start = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                date_end = date_start

                self.read_date_query_tbl1 = self.read_date_query_tbl1.replace("{start}", date_start)
                self.query = self.read_date_query_tbl1.replace("{end}", date_end)
                self.query = self.query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                if not self.reportable:
                    self.query = self.query.replace("{reportable}", "in (0,1)")
                    pass
                else:
                    self.query = self.query.replace("{reportable}", " = " + str(self.reportable))

                self.bad_query = self.read_bad_date_query_tbl1.replace("{start}", date_start)
                self.bad_query = self.bad_query.replace("{end}", date_end)
                self.bad_query = self.bad_query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                # we want the bad report as well
                self.bad = True
                break
            elif self.user_selection.lower() == 'sd':
                date_start = input('Enter the submitted date you\'d like to search for in YYYY-MM-DD format (include dashes):\n--> ')
                year, month, day = map(int, date_start.split('-'))
                date_start = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                date_end = date_start

                self.read_sdate_query_tbl1 = self.read_sdate_query_tbl1.replace("{start}", date_start)
                self.query = self.read_sdate_query_tbl1.replace("{end}", date_end)
                self.query = self.query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                self.query = self.query.replace("{reportable}", str(self.reportable))
                self.ui_lab = "sub_date_query"
                self.bad = False
                break

            elif self.user_selection.lower() == 'r':
                date_start = input('Enter the start date in YYYY-MM-DD format (include dashes):\n--> ')
                year, month, day = map(int, date_start.split('-'))
                date_start = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                
                date_end = input('Enter the end date in YYYY-MM-DD format (include dashes):\n--> ')
                year, month, day = map(int, date_start.split('-'))
                date_end = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                
                self.read_date_query_tbl1 = self.read_date_query_tbl1.replace("{start}", date_start)
                self.query = self.read_date_query_tbl1.replace("{end}", date_end)
                self.query = self.query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                self.query = self.query.replace("{reportable}", str(self.reportable))

                self.bad_query = self.read_bad_date_query_tbl1.replace("{start}", date_start)
                self.bad_query = self.bad_query.replace("{end}", date_end)
                self.bad_query = self.bad_query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                # we want the bad report as well
                self.bad = True
                break
            elif self.user_selection.lower() == 'a':
                self.ui_lab = self.user_selection.lower()
                self.query = self.read_all_query_tbl1
                self.bad_query = self.read_bad_all_query_tbl1
                self.a = True
                break
            elif self.user_selection.lower() == 'f':
                self.ui_lab = input("Please enter the facility to filter samples by:\n--> ")
                self.query = self.read_facility_query_tbl1.replace("{facility}", self.ui_lab)
                self.query = self.query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                self.query = self.query.replace("{reportable}", str(self.reportable))

                break
            elif self.user_selection.lower() == 's':
                self.ui_lab = input("Please enter the submitting facility to filter samples by:\n--> ")
                self.query = self.read_sfacility_query_tbl1.replace("{sub_lab}", self.ui_lab)
                self.query = self.query.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
                self.query = self.query.replace("{reportable}", str(self.reportable))
                self.p_lab = self.ui_lab
                
                break
            else:
                continue

    def get_df(self):
        super().setup_db()
        self.df = self.db_handler.ss_read(query=self.query)
        if self.bad:
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
        if self.bad:
            self.bad_df = add_cols(obj=self, \
                df = self.bad_df, \
                col_lst = self.csv_headers, \
                col_func_map= self.col_func_map)
            self.bad_df = self.bad_df[self.bad_df_headers]
            if not self.bad_df.empty:
                self.bad_df = clean_df(self.bad_df)

    
    def write_epi_report(self):
        # save both files to csv
        today = datetime.datetime.today().strftime("%m%d%y")
        path = self.folderpathbase + "\\" + today
        if self.bad:
            save_epi_csv(self.df, self.bad_df, path)
        else:
            save_csv(self.df, path, self.user_selection, self.ui_lab)


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