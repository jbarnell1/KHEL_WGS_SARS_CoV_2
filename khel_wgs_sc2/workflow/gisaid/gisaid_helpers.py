from ..workflow_obj import workflow_obj
from ..ui import progressBar
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
        self.id = "gisaid"

    # methods
    def get_json(self):
        self.logger.info(self.id + ': Aquiring local data from cache')
        super().get_json(-2)
        self.logger.info(self.id + ': get_json finished!')

    def scan_db(self):
        # in this function, we need to get the maximum gisaid number
        # so we know how to label future samples
        # we also will scan the database for the last seven days for
        # samples eligible for upload based on the qc cutoffs set
        # in data/static_cache.json
        super().setup_db()
        self.next_gisaid = int(self.db_handler.ss_read(query=self.read_query_tbl1_max_gisaid).iat[0, 0])
        prev_week = (datetime.date.today() - datetime.timedelta(days = 7)).strftime("%Y%m%d")
        self.read_query_tbl1_eligible_hsn = self.read_query_tbl1_eligible_hsn.replace("{prev_week}", prev_week)
        self.hsn_lst = self.db_handler.sub_read(query=self.read_query_tbl1_eligible_hsn)['hsn'].astype(str).tolist()

    def get_gisaid_df(self):
        # use the hsn list from above to get all hsns into single dataframe
        self.gisaid_start = self.db_handler.sub_lst_read(query=self.read_query_tbl1, lst=self.hsn_lst)
        self.user = input("\nPlease input the user for this report\n-->")
        self.hsn_dict = {'hsn':[], 'gisaid':[]}

    def compile_fasta(self):
        # create the file that will hold the completed fasta data
        # make both destination files for metadata and fasta
        self.file_no = 1
        date1 = datetime.datetime.today().strftime("%m%d%y")
        self.folderpath = self.folderpathbase + "\\" + date1 + "\\SQL\\"
        if not os.path.exists(self.folderpath):
            os.makedirs(self.folderpath)
        self.filepath = date1 + "_" + str(self.file_no) + ".fasta"
        while os.path.exists(self.folderpath + self.filepath):
            self.file_no += 1
            self.filepath = date1 + "_" + str(self.file_no) + ".fasta"

        # get list of fasta files
        self.file_lst = self.gisaid_start["path_to_fasta"].values.tolist()


    def compile_gisaid(self):
        # compile the gisaid template
        lab_name = "Kansas Health and Environmental Lab"
        lab_addr = "6810 SE Dwight Street, Topeka, KS 66620"
        self.gisaid_df = pd.DataFrame(self.gisaid_start.rename(columns=self.rename_gisaid_cols_lst))
        self.gisaid_df.sort_values(['wgs_run_date', 'hsn'], inplace=True)
        self.gisaid_df.insert(0, "submitter", self.user)
        self.gisaid_df.insert(0, "fn", self.filepath)
        self.gisaid_df["covv_virus_name"] = self.gisaid_df.apply(lambda row: self.get_virus_name(row), axis=1)
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
        for fasta in self.file_lst:
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

        # # now, open the template workbook, and append the new
        # templatedf = pd.read_excel(self.path_to_template, sheet_name="Submissions", engine='xlrd')
        # self.gisaid_df = templatedf.append(self.gisaid_df)
        
        date2 = datetime.datetime.today().strftime("%Y%m%d")
        #templatefilepath = date2 + "_" + str(self.file_no) + "_EpiCoV_BulkUpload_Template.xls"
        templatefilepath = date2 + "_" + str(self.file_no) + "_sql.csv"

        # write the information to the template
        self.gisaid_df.to_csv(self.folderpath + templatefilepath, index=False, header=True)

        # # write the previous information page to the new workbook
        # rb = open_workbook(self.folderpath + templatefilepath, formatting_info=True)
        # wb = xl_copy(rb)
        # # add sheet 
        # Sheet1 = wb.add_sheet('Instructions')
        # wb.save(self.folderpath + templatefilepath)

    def database_push(self):
        # put the updated gisaid_nums with the correct samples
        gisaid_df_update = pd.DataFrame.from_dict(self.hsn_dict)
        gisaid_df_update_lst = gisaid_df_update.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=gisaid_df_update_lst, query=self.write_query_tbl1)

    def get_virus_name(self, row):
        year = str(row["doc"])[0:4]
        gisaid = int(self.next_gisaid)
        gisaid_str = f'{gisaid:04}'
        self.hsn_dict['hsn'].append(row["hsn"])
        self.hsn_dict['gisaid'].append(gisaid)
        self.next_gisaid += 1
        return "hCoV-19/USA/KS-KHEL-" + gisaid_str + "/" + year


def get_hsn(row):
    hsn = str(row["HSN"])
    if len(hsn) == 7:
        return hsn
    else:
        return hsn[:-2]


