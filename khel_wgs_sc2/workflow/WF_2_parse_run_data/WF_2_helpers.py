from ..workflow_obj import workflow_obj
from ..ui import get_run_data
from ..formatter import add_cols, remove_blanks, remove_pools
import pandas as pd


class WorkflowObj2(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_2"

    # methods
    def get_json(self):
        super().get_json(2)


    def get_info_from_user(self):
        run_data, self.machine_num, self.wgs_run_date, \
            self.day_run_num, self.platform = get_run_data()

        if self.include_controls:
            neg = False
            pos = False
            # store away the control values for the run
            for sample_num in range(len(run_data['hsn'])):
                if "neg" in run_data['hsn'][sample_num].lower():
                    self.neg_ctrl_pass = (run_data['percent_cvg'][sample_num] <= self.neg_percent_cvg_cutoff)
                    self.neg_name = "1" + self.wgs_run_date[:-4].replace("/", "") + self.wgs_run_date[-2:] + str(self.machine_num) + str(self.day_run_num)
                    run_data['hsn'][sample_num] = self.neg_name
                    neg = True
                if "pos" in run_data['hsn'][sample_num].lower():
                    self.pos_ctrl_pass = (run_data['percent_cvg'][sample_num] >= self.percent_cvg_cutoff)
                    self.pos_name = "2" + self.wgs_run_date[:-4].replace("/", "") + self.wgs_run_date[-2:] + str(self.machine_num) + str(self.day_run_num)
                    run_data['hsn'][sample_num] = self.pos_name
                    pos = True
                if neg and pos:
                    break
        
        # create dataframe for QC/Research table
        self.df_qc = pd.DataFrame.from_dict(run_data)


    def format_dataframe(self):
        self.df_qc = remove_pools(self.df_qc, 'hsn')
        self.df_qc = remove_blanks(self.df_qc, 'hsn')
        # add columns

        self.df_qc = add_cols(obj=self, \
            df=self.df_qc, \
            col_lst=self.add_col_lst, \
            col_func_map=self.col_func_map)
        self.df_qc = self.df_qc.astype({"wgs_run_date": str})

        if self.include_controls:
            self.df_qc=add_cols(obj=self, \
            df=self.df_qc, \
            col_lst=self.add_col_lst_ctrl, \
            col_func_map=self.col_func_map)
        else:
            self.df_qc['pos_pass'] = 0
            self.df_qc['neg_pass'] = 0
            self.df_qc['reportable'] = 0
        
        # create dataframe for results table
        self.df_results = self.df_qc.copy()
        # sort/remove columns to match table 1
        # sort/remove columns to match table 2
        self.df_results = pd.DataFrame(self.df_results[self.df_results_cols])
        self.df_qc = pd.DataFrame(self.df_qc[self.df_qc_cols])
        if self.include_controls:
            neg_idx = self.df_results.index[self.df_results['hsn'] == self.neg_name][0]
            pos_idx = self.df_results.index[self.df_results['hsn'] == self.pos_name][0]
            self.df_results.drop([pos_idx, neg_idx], inplace=True)


    def database_push(self):
        super().setup_db()
        # query for updating results table (only update table1 if qc is better)
        # update table 2 regardless
        
        df_results_lst = self.df_results.values.astype(str).tolist()
        self.write_query_tbl1 = self.write_query_tbl1.replace("{avg_depth_cutoff}", str(self.avg_depth_cutoff))
        self.write_query_tbl1 = self.write_query_tbl1.replace("{percent_cvg_cutoff}", str(self.percent_cvg_cutoff))
        self.db_handler.lst_ptr_push(df_lst=df_results_lst, query=self.write_query_tbl1)

        
        #TYPE: LST
        df_qc_lst = self.df_qc.values.astype(str).tolist()
        df_qc_cols_query = "(" + ", ".join(self.df_qc_cols) + ")"
        try:
            self.db_handler.lst_push(df_lst=df_qc_lst, df_cols=df_qc_cols_query)
        except Exception as e:
            print(e)
            raise ValueError("\n-------------------------------------------------------------------------------------------------------------------\
                \nEntry already exists in the database! The clearlabs data for this run has likely already been added to the database\
                \n-------------------------------------------------------------------------------------------------------------------")