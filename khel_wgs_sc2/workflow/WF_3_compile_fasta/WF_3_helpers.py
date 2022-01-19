from ..workflow_obj import workflow_obj
from ..ui import get_path_folder
from ..formatter import add_cols, remove_pools, remove_blanks, replace_shortcut
import os
import pandas as pd
import datetime


class WorkflowObj3(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_3"
    
    # methods
    def get_json(self):
        super().get_json(3)

    def compile_fasta(self):
        print("Use the following dialog box to select the folder with all FASTA files in the Run Data folder")
        self.path = get_path_folder()
        self.path = replace_shortcut(self.path)
        # make new folder/file to save to
        splt = self.path.split("/")
        if splt[-1] != "FAST files":
            raise ValueError("\n-------------------------------------------------------------------------------------------------------------------\
                \nThe selected folder is unexpected!  Select a folder with the name 'FAST files'\
                \n-------------------------------------------------------------------------------------------------------------------")
        folder_name = splt[-2]
        date = datetime.datetime.strptime(folder_name.split(".")[0], "%m%d%y").strftime("%m%d%y")
        machinenum = folder_name[-4:-2]
        filename = "all_" + date + "_" + machinenum + ".fasta"

        # make file to save to
        if splt[-3] == "ClearLabs" or splt[-3] == "ClearLabs downloads":
            path_write = "/".join(splt[:-1]) + "/" + filename
        else:
            path_write = "DOES NOT EXIST"
        extension = ".fasta"
        
        # initialize string that will hold all the sequence data
        # and write to file f
        self.seqName_lst = []
        s = ""
        ctr = 0
        f = open(path_write, "w")
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(extension):
                    curr_file = open(self.path + "/" + file, "r")
                    file_contents = curr_file.readlines()
                    curr_file.close()
                    s += "\n\n"
                    for line in file_contents:
                        s += line
                    f.write(s)
                    s = ""
                    print("finished with file ", ctr)
                    ctr += 1
                    self.seqName_lst.append(file)
        f.close()
        if self.analysis_pathway == "cli":
            return path_write
        else:
            return ""

    def get_fasta_path_df(self):
        # transform dictionary of hsn/path into dataframe
        self.df = pd.DataFrame(self.seqName_lst, columns=['seqName'])
        # remove pooled samples from dataframe
        self.df = remove_pools(self.df, 'seqName')
        
        # remove any blanks from the run
        self.df = remove_blanks(self.df, 'seqName')

        #drop controls from index
        if self.include_controls:
            neg = False
            pos = False
            to_drop = []
            for index in range(len(self.df.index)):
                if "neg" in self.df['seqName'][index].lower():
                    #neg_idx = index
                    to_drop.append(index)
                    neg = True

                if "pos" in self.df['seqName'][index].lower():
                    #pos_idx = index
                    to_drop.append(index)
                    pos = True
                if neg and pos:
                    break
            #self.df.drop([pos_idx, neg_idx], inplace=True)
            self.df.drop(to_drop, inplace=True)

        # add columns
        add_cols(obj=self, \
            df=self.df, \
            col_lst=self.add_col_lst, \
            col_func_map=self.col_func_map)
        self.df.drop(labels=['seqName'], axis=1, inplace=True)
        self.df.rename(columns={"day_run_num_var":"day_run_num", \
            "wgs_run_date_var":"wgs_run_date"}, inplace=True)


    def database_push(self):
        # attempt to connect to database
        super().setup_db()
        df_lst = self.df.values.astype(str).tolist()
        self.db_handler.lst_ptr_push(df_lst=df_lst, query=self.write_query_tbl2)


