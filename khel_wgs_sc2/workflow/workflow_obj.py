from abc import ABC
from workflow.ms_sql_handler import ms_sql_handler
from workflow.reader import read_json
from workflow.ui import get_path
from workflow.writer import write_json
import time
import os


class workflow_obj(ABC):

    def get_json(self, wf):
        print("Importing data from cache...")
        # get relative path to json cache file
        dirname = os.path.dirname(os.path.abspath(__file__))
        folders = dirname.split("\\")
        top_pkg_folder = "\\".join(folders[0:-2])
        path_to_cache = top_pkg_folder + "\\data\\cache.json"

        full_cache = read_json(path_to_cache)
        # with open(path_to_cache, 'r') as json_cache:
        #     full_cache = json.load(json_cache)
        
        # only select today's workflow, check that static data is present
        if wf > 0:
            workflow = "workflow" + str(wf)
        else:
            if wf == -1:
                workflow = 'epi_isl'
            elif wf == -2:
                workflow = 'gisaid'
            elif wf == -3:
                workflow = 'outside_lab'
            elif wf == -4:
                workflow = 'query'
            elif wf == -5:
                workflow = 'refresh'

        working_cache = full_cache[workflow]
        gen_cache = full_cache['all_workflows']
        for k, v in working_cache.items():
            if "query" in str(k):
                if not hasattr(self, k):
                    setattr(self, k, "".join(v))
            else:
                if not hasattr(self, k):
                    setattr(self, k, v)

        # search for dynamic data.  If empty, gather from user (first time use)
        try:
            if wf == 1:
                self.lims_conn = working_cache['lims_conn']
            if wf == -2:
                self.path_to_template = working_cache['path_to_template']
                self.gisaid_path = working_cache['gisaid_path']
                self.folderpathbase = working_cache['folderpathbase']
            if wf == 7:
                self.destination = working_cache['destination']
                self.location = working_cache['location']
                self.port = working_cache['port']
                self.sftp_user = working_cache['sftp_user']
                self.sftp_pwd = working_cache['sftp_pwd']
            if wf == -4:
                self.folder_path_base =working_cache['folder_path']
            self.sql_user = gen_cache['sql_user']
            self.sql_pass = gen_cache['sql_pass']
            self.sql_server = gen_cache['sql_server']
            self.sql_db = gen_cache['sql_db']
            self.avg_depth_cutoff = gen_cache['avg_depth_cutoff']
            self.percent_cvg_cutoff = gen_cache['percent_cvg_cutoff']
            self.neg_percent_cvg_cutoff = gen_cache['neg_percent_cvg_cutoff']
            self.col_func_map = gen_cache['col_func_map']
        except KeyError:
            print("Looks like this is your first time using the script!")
            print("\nPlease fill out the following questions (we'll store \
results on-device so you won't have to enter them again).")
            if wf == 1:
                self.lims_conn = input("Please enter the string for the LIMS connection \
(ie <user>/<password>@<db_tablename>\n-->")
            if wf == -2:
                print("Please enter the path to the template workbook")
                self.path_to_template = get_path()
                print("Please select the path to the gisaid file")
                self.gisaid_path = get_path()
                self.folderpathbase = "\\".join(self.path_to_template.split("\\")[:-1])
            if wf == 7:
                self.destination = input("Type the relative path of the destination folder")
                self.location = input("Type the address of the final location of sftp transfer")
                self.port = input("Type the port to be used in transfer (typically 22)")
                self.sftp_user = input("Type the username for sftp access")
                self.sftp_pwd = input("Type the password for sftp access")
            if wf == -4:
                print("Please select the path to the folder where you would like the \
                    queries to be stored.")
                self.folder_path_base = get_path()
            self.sql_user = input("Please enter the username for the sql database:\n-->")
            self.sql_pass = input("Please enter the password for the sql database:\n-->")
            self.sql_server = input("Please enter the server name for the sql database:\n-->")
            self.sql_db = input("Please enter the name for the sql database:\n-->")

            
            print("\nFinished! If you need to change these values in the \
future for any reason, modify the cache file: daily_workflow/data/cache.json")
            if wf == 1:
                full_cache[workflow]['limsConn'] = self.lims_conn
            if wf == -2:
                full_cache[workflow]['path_to_template'] = self.path_to_template
                full_cache[workflow]['gisaid_path'] = self.gisaid_path
                full_cache[workflow]['folderpathbase'] = self.folderpathbase
            if wf == 7:
                full_cache[workflow]['destination'] = self.destination
                full_cache[workflow]['location'] = self.location
                full_cache[workflow]['port'] = self.port
                full_cache[workflow]['sftp_user'] = self.sftp_user
                full_cache[workflow]['sftp_pwd'] = self.sftp_pwd
            full_cache["all_workflows"]['sqlUser'] = self.sql_user
            full_cache["all_workflows"]['sqlPass'] = self.sql_pass
            full_cache["all_workflows"]['sqlServer'] = self.sql_server
            full_cache["all_workflows"]['sqldb'] = self.sql_db
            print("\nStoring data for future use...")
            res = write_json(path_to_cache, full_cache)
            if res != 0:
                raise ValueError("workflow_obj write to json failed!")
            # with open(path_to_cache, mode='w') as cache_file:
            #     json.dump(full_cache, cache_file, indent=4)
            print("\nContinuing the script in 5 seconds.")
            time.sleep(5)

    def setup_db(self):
        self.db_handler = ms_sql_handler(self)
        self.db_handler.establish_db()