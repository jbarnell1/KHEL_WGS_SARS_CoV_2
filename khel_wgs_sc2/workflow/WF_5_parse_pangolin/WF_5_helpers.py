from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..ui import get_path
from ..formatter import add_cols, remove_pools, remove_blanks, merge_dataframes


class WorkflowObj5(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_5"

    # methods
    def get_json(self):
        super().get_json(5)


    def get_pango_dfs(self, po_path=False):
        # open pangolin path --> pandas dataframe
        if not po_path:
            print("\nUse the following window to open the pangolin results workbook...")
            pango_path = get_path()
        splt = pango_path.split("/")
        parent_folder = splt[-2]
        data = parent_folder.split(".")
        neg_name = "1" + "".join(data)
        pos_name = "2" + "".join(data)
        df = get_pandas(pango_path, 'WF_5', 'pangolin', ',')
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


    def send_fasta(self, compiled_fasta_path):
        # establish connection to server
        super().setup_ssh()
        # send the fasta file to the server, at the specified location
        self.ssh_handler.ssh_send_file(compiled_fasta_path)


    def run_pangolin(self):
        # connection to the server has already been established
        # check for updates and update if needed
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""cd <path to pangolin file>""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)

        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""conda activate pangolin""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)
        
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""git pull""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)
        
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""conda env update -f environment.yml""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)
        
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""pip install .""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)
        
        # execute command
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""pangolin <fasta path>""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)
        
    
    def receive_pangolin_df(self, po_local_path):
        self.ssh_handler.ssh_receive_file(po_local_path + "")