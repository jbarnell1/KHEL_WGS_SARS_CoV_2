from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from xlrd import open_workbook
from xlutils.copy import copy as xl_copy
import os
import datetime
import pandas as pd



class gisaid_obj(workflow_obj):
    # constructor
    def __init__(self, logger):
        self.logger = logger
        self.write_query_tbl1 = None
        self.read_query_tbl1 = None
        self.read_query_tbl1_gisaid = None
        self.id = "gisaid"
        self.db_handler = None
        self.rename_gisaid_cols_lst = None
        self.full_gisaid_cols_lst = None
        self.sql_user = None
        self.sql_pass = None
        self.sql_server = None
        self.sql_db = None
        self.filepath = None
        self.folderpath = None
        self.db = None
        self.gisaid_df = None
        self.df = None
        self.gisaid_path = None
        self.folderpathbase = None
        self.path_to_template = None

    # methods
    def get_json(self):
        self.logger.info(self.id + ': Aquiring local data from cache')
        super().get_json(-2)
        self.logger.info(self.id + ': get_json finished!')

    def get_gisaid_dfs(self):
        self.logger.info(self.id + ': Getting gisaid data from worksheet')
        
        self.df = get_pandas(self.gisaid_path, self.id, self.id, ',', self.logger)

        # extract user, "plain" HSNs (no extension ".A, .B, etc")
        self.df = pd.DataFrame(self.df)
        print(self.df)
        user = str(self.df.iloc[0, 1])
        self.df.drop(labels=["User"], axis=1, inplace=True)
        print(self.df)
        self.df["hsn"] = self.df.apply(lambda row: get_hsn(row), axis=1)
        self.df.drop(labels=["HSN"], axis=1, inplace=True)
        print(self.df)

    def get_db_info(self):
        # attempt to connect to database
        # self.db = establish_db(self, 'gisaid')
        super().database_push()
        hsn_lst = self.df['hsn'].to_list()
        self.gisaid_df = self.db_handler.sub_read(query=self.read_query_tbl1, lst=hsn_lst)

        # find the max gisaid number
        max_gisaid_df = self.db_handler.ss_read(query=self.read_query_tbl1_gisaid)
        gisaid_num = max_gisaid_df.iloc[0,0] + 1

    def compile_fasta(self):
        # compile the fasta file

        # make both destination files for metadata and fasta
        file_no = 1
        date1 = datetime.datetime.today().strftime("%m%d%y")
        #self.folderpath = "\\\\kdhe\\dfs\\DHEL Shared\\Diagnostic Microbiology\\WGS\\SARS-CoV-2\\GISAID\\" + date1 + "\\SQL\\"
        self.folderpath = self.folderpathbase + date1 + "\\SQL\\"
        #folderpath = "C:\\Users\\jonathan.barnell\\Documents\\Bioinformatics\\Mid-development (SQL database)\\update - 061621\\GISAID\\" + date1 + "\\"
        if not os.path.exists(self.folderpath):
            os.makedirs(self.folderpath)
        self.filepath = date1 + "_" + str(file_no) + ".fasta"
        while os.path.exists(self.folderpath + self.filepath):
            file_no += 1
            self.filepath = date1 + "_" + str(file_no) + ".fasta"

        # get list of fasta files
        file_lst = self.gisaid_df["path_to_fasta"].values.tolist()

    def compile_gisaid(self):
        # compile the gisaid template
        lab_name = "Kansas Health and Environmental Lab"
        lab_addr = "6810 SE Dwight Street, Topeka, KS 66620"
        self.gisaid_df = pd.DataFrame(self.gisaid_df.rename(columns=self.rename_gisaid_cols_lst))
        self.gisaid_df.sort_values(['wgs_run_date', 'hsn'], inplace=True)
        self.gisaid_df.insert(0, "submitter", user)
        self.gisaid_df.insert(0, "fn", self.filepath)
        self.gisaid_df["covv_virus_name"] = self.gisaid_df.apply(lambda row: get_virus_name(row), axis=1)
        self.gisaid_df.insert(0, "covv_type", "betacoronavirus")
        self.gisaid_df.insert(0, "covv_passage", "Original")
        self.gisaid_df["covv_collection_date"] = self.gisaid_df.apply(lambda row: str(row["doc"]), axis=1)
        self.gisaid_df["covv_location"] = self.gisaid_df.apply(lambda row: "North America / USA / " + str(row["state"]) if str(row["state"]) != "unknown" else "North America / USA / Kansas", axis=1)
        self.gisaid_df.insert(0, "covv_add_location", "unknown")
        self.gisaid_df.insert(0, "covv_host", "Human")
        self.gisaid_df.insert(0, "covv_add_host_info", "unknown")
        self.gisaid_df["covv_gender"] = self.gisaid_df.apply(lambda row: str(row["sex"]).lower(), axis=1)
        self.gisaid_df.insert(0, "covv_patient_status", "unknown")
        self.gisaid_df.insert(0, "covv_specimen", "unknown")
        self.gisaid_df.insert(0, "covv_outbreak", "unknown")
        self.gisaid_df.insert(0, "covv_last_vaccinated", "unknown")
        self.gisaid_df.insert(0, "covv_treatment", "unknown")
        self.gisaid_df.insert(0, "covv_seq_technology", "ClearLabs")
        self.gisaid_df.insert(0, "covv_assembly_method", "ClearLabs")
        #TODO make variable lab names and lab addresses
        self.gisaid_df.insert(0, "covv_orig_lab", lab_name)
        self.gisaid_df.insert(0, "covv_orig_lab_addr", lab_addr)
        self.gisaid_df.insert(0, "covv_provider_sample_id", "unknown")
        self.gisaid_df.insert(0, "covv_subm_lab", lab_name)
        self.gisaid_df.insert(0, "covv_subm_lab_addr", lab_addr)
        self.gisaid_df.insert(0, "covv_subm_sample_id", "unknown")
        self.gisaid_df.insert(0, "covv_authors", "Mike Grose, Katherine Wiggins, Jonathan Barnell, Ben Olsen, and Phil Adam")
        self.gisaid_df.insert(0, "comment_type", None)
        self.gisaid_df.insert(0, "covv_comment", None)

    def make_fasta_file(self):
        # make the fasta file
        s = ""
        f = open(self.folderpath + self.filepath, "w")
        for fasta in file_lst:
            curr_file = open(fasta, "r")
            file_contents = curr_file.readlines()
            curr_file.close()
            s += "\n\n"
            for line in progressBar(file_contents, prefix='Progress', suffix='Complete', length=50):
                if line[0] != ">":
                    s += line
                else:
                    seq_hsn = line[1:8]
                    index = self.gisaid_df[self.gisaid_df['hsn'] == int(seq_hsn)].index.values.tolist()
                    index = index[0]
                    v_name = ">" + self.gisaid_df.iloc[int(index)]['covv_virus_name'] + "\n"
                    s += v_name
            f.write(s)
            s = ""
        f.close()

    def make_gisaid_file(self):
        # order columns/remove unnecessary columns
        self.gisaid_df = self.gisaid_df[self.full_gisaid_cols_lst]

        # now, open the template workbook, and append the new
        templatedf = pd.read_excel(self.path_to_template, sheet_name="Submissions", engine='xlrd')
        self.gisaid_df = templatedf.append(self.gisaid_df)
        
        date2 = datetime.datetime.today().strftime("%Y%m%d")
        templatefilepath = date2 + "_" + str(file_no) + "_EpiCoV_BulkUpload_Template.xls"

        # write the information to the template
        self.gisaid_df.to_excel(self.folderpath + templatefilepath, index=False, header=True, sheet_name = "Submissions", engine = 'xlwt')

        # write the previous information page to the new workbook
        rb = open_workbook(self.folderpath + templatefilepath, formatting_info=True)
        wb = xl_copy(rb)
        # add sheet 
        Sheet1 = wb.add_sheet('Instructions')
        wb.save(self.folderpath + templatefilepath)

    def database_push(self):
        ######################################GET INFO FROM DATABASE#################################################
        # put the updated gisaid_nums with the correct samples
        gisaid_df_update = pd.DataFrame.from_dict(hsn_dict)
        gisaid_df_update_lst = gisaid_df_update.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=gisaid_df_update_lst, query=self.write_query_tbl1)


gisaid_num = None
hsn_dict = {'hsn':[], 'gisaid':[]}


def get_hsn(row):
    return str(row["HSN"])[0:7]


def get_virus_name(row):
    global gisaid_num
    global hsn_dict
    year = str(row["doc"])[0:4]
    gisaid = int(gisaid_num)
    gisaid_str = f'{gisaid:04}'
    hsn_dict['hsn'].append(row["hsn"])
    hsn_dict['gisaid'].append(gisaid)
    gisaid_num += 1
    return "hCoV-19/USA/KS-KHEL-" + gisaid_str + "/" + year