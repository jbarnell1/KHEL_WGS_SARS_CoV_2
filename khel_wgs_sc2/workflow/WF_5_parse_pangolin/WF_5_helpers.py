from ..workflow_obj import workflow_obj
from ..processor import *
from ..reader import *
from ..writer import *
from ..ui import *
from ..formatter import *


class WorkflowObj5(workflow_obj):
    # constructor
    def __init__(self, logger):
        self.logger = logger
        self.id = "WF_5"

    # methods
    def get_json(self):
        self.logger.info(self.id + ": Acquiring local data from cache")
        super().get_json(5)
        self.logger.info(self.id + ": get_json finished!")


    def get_pango_dfs(self):
        print("\nUse the following window to open the pangolin results workbook...")
        pango_path = get_path()
        splt = pango_path.split("/")
        parent_folder = splt[-2]
        data = parent_folder.split(".")
        neg_name = "1" + "".join(data)
        pos_name = "2" + "".join(data)
        self.logger.info(self.id + ": Getting pangolin data from worksheet")
        df = get_pandas(pango_path, 'WF_5', 'pangolin', ',', self.logger)
        df = df.rename(columns=self.rename_po_cols_lst)

        # remove pooled samples from the run
        df = remove_pools(df, 'Sequence name')

        # remove any blanks from the run
        df = remove_blanks(df, 'Sequence name')

        # rename controls to appropriate format for database
        neg = False
        pos = False
        for index in range(len(df.index)):
            if "neg" in df['Sequence name'][index].lower():
                neg_splt = df.at[index, 'Sequence name'].split("/")
                neg_name = neg_name + "/" + "/".join(neg_splt[1:])
                df.at[index, 'Sequence name'] = neg_name
                neg = True
            if "pos" in df['Sequence name'][index].lower():
                pos_splt = df.at[index, 'Sequence name'].split("/")
                pos_name = pos_name + "/" + "/".join(pos_splt[1:])
                df.at[index, 'Sequence name'] = pos_name
                pos = True
            if neg and pos:
                break

        # add columns
        df = add_cols(obj=self,
            df=df,
            col_lst=self.add_col_lst,
            col_func_map=self.col_func_map)
        df.rename(columns={"day_run_num_var":"day_run_num",
            "wgs_run_date_var":"wgs_run_date",
            "machine_num_var":"machine_num"}, inplace=True)
        
        # remove columns/split dataframes
        self.df_qc = df[self.full_lst]
        self.df_results = df[self.full_lst]
        self.logger.info(self.id + ": get_pango_dfs finished!")

    def database_push(self):
        super().setup_db()
        all_time_df_qc = self.db_handler.sub_read(query=self.read_query_tbl2)
        df_results_final = merge_dataframes(
            df1=all_time_df_qc,
            df2=self.df_results,
            df1_drop=['ID_Table_2', 'platform', 'percent_cvg', 'avg_depth',
            'total_ns', 'qc_snpclusters_status', 'qc_overall_status', 'path_to_fasta'],
            df_final_drop=['wgs_run_date', 'machine_num', 'position', 'day_run_num'],
            join_lst=["hsn", "wgs_run_date", "machine_num", "position", "day_run_num"],
            join_type='inner')

        df_results_final_lst = df_results_final.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_results_final_lst, query=self.write_query_tbl1)
        self.logger.info(self.id + ": database_push finished!")
