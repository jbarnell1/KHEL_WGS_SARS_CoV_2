from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..ui import get_path
from ..formatter import add_cols, remove_blanks, remove_pools, merge_dataframes

class WorkflowObj4(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_4"

    # methods
    def get_json(self):
        super().get_json(4)

    def get_nextclade_dfs(self, nc_path=False):
        # open nextclade path --> pandas dataframe
        if not nc_path:
            print("\nUse the following window to open the nextclade results workbook...")
            nc_path = get_path()
        splt = nc_path.split("/")
        parent_folder = splt[-2]
        data = parent_folder.split(".")
        neg_name = "1" + "".join(data)
        pos_name = "2" + "".join(data)
        df = get_pandas(nc_path, "WF_4", "nextclade", '\t')
        df = df.rename(columns=self.rename_nc_cols_lst)
        
        # remove pooled samples from the run
        df = remove_pools(df, 'seqName')

        # remove any blanks from the run
        df = remove_blanks(df, 'seqName')

        # rename controls to appropriate format for database
        neg = False
        pos = False
        for index in range(len(df.index)):
            if "neg" in df['seqName'][index].lower():
                neg_splt = df.at[index, 'seqName'].split("/")
                neg_name = neg_name + "/" + "/".join(neg_splt[1:])
                df.at[index, 'seqName'] = neg_name
                neg = True
            if "pos" in df['seqName'][index].lower():
                pos_splt = df.at[index, 'seqName'].split("/")
                pos_name = pos_name + "/" + "/".join(pos_splt[1:])
                df.at[index, 'seqName'] = pos_name
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
        self.df_qc = df[self.nc_qc_cols_lst]
        self.df_results = df[self.nc_results_cols_lst]

    def database_push(self):
        # attempt to connect to database
        # db = establish_db(self, 'WF_4')

        super().setup_db()
        df_qc_update_lst = self.df_qc.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_qc_update_lst, query=self.write_query_tbl2)
        all_time_df_qc = self.db_handler.sub_read(query=self.read_query_tbl2)
        
        
        df_results_final = merge_dataframes(\
            df1=all_time_df_qc, \
            df2=self.df_results, \
            df1_drop=['ID_Table_2', 'percent_cvg', 'avg_depth', 'total_ns'], \
            df_final_drop=['wgs_run_date', 'machine_num', 'position', 'day_run_num'], \
            join_lst=["hsn", "wgs_run_date", "machine_num", "position", "day_run_num"], \
            join_type='inner')

        df_results_final_lst = df_results_final.values.astype(str).tolist()
        if len(df_results_final_lst) == 0:
            raise ValueError("\n-------------------------------------------------------------------------------------------------------------------\
                \nNextclade data from this run has likely already been pushed to the database!\
                \n-------------------------------------------------------------------------------------------------------------------")
        print("Updating rows in the results table...")

        self.db_handler.lst_ptr_push(df_lst=df_results_final_lst, query=self.write_query_tbl1)


    def get_fasta_path(self):
        print("\nUse the following window to open the fasta file you'd like to send for nextclade analysis...")
        return get_path()


    def send_fasta(self, compiled_fasta_path):
        # establish connection to server
        super().setup_ssh()
        # send the fasta file to the server, at the specified location
        self.ssh_handler.ssh_send_file(compiled_fasta_path)


    def run_nextclade(self):
        # connection to the server has already been established
        # check for updates and update if needed
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""curl -fsSL "https://github.com/nextstrain/nextclade/releases/latest/download/nextclade-Linux-x86_64" -o "nextclade" && chmod +x nextclade""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)



        # env activation REQUIRED??? -see wf5 helpers and documentation



        # execute command
        stdin, stdout, stderr = self.ssh_handler.ssh_exec("""nextclade --in-order --input-fasta=data/sars-cov-2/<file_name> --output-tsv=output/nextclade.tsv""")
        lines = stdout.readlines()
        errors = stderr.readlines()
        for e in errors:
            print('\n\nerror: ', e)
        for l in lines:
            print('\nline: ', l)

    
    def receive_nextclade_df(self, nc_local_path):
        self.ssh_handler.ssh_receive_file(nc_local_path + "/nextclade.tsv")


    def clean_connections(self):
        self.ssh_handler.close_connections()