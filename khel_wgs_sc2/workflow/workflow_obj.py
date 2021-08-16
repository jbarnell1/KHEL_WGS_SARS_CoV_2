from abc import ABC
from workflow.ui import get_path_folder
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
        path_to_static_cache = top_pkg_folder + "\\data\\static_cache.json"

        full_static_cache = read_json(path_to_static_cache)
        
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

        working_static_cache = full_static_cache[workflow]
        gen_static_cache = full_static_cache['all_workflows']
        for k, v in working_static_cache.items():
            if "query" in str(k):
                if not hasattr(self, k):
                    setattr(self, k, " ".join(v))
            else:
                if not hasattr(self, k):
                    setattr(self, k, v)

        self.avg_depth_cutoff = gen_static_cache['avg_depth_cutoff']
        self.percent_cvg_cutoff = gen_static_cache['percent_cvg_cutoff']
        self.neg_percent_cvg_cutoff = gen_static_cache['neg_percent_cvg_cutoff']
        self.col_func_map = gen_static_cache['col_func_map']

        # search for private data.  If empty, gather from user (first time use)
        path_to_private_cache = top_pkg_folder + "\\data\\private_cache.json"
        # if the file doesn't exist, create it
        if os.path.isfile(path_to_private_cache) and os.access(path_to_private_cache, os.R_OK):
            pass
        else:
            print("\nPrivate cache does not exist, creating file...")
            private_start_dict = dict.fromkeys(full_static_cache.keys(), {})
            write_json(path_to_private_cache, private_start_dict)
        full_private_cache = read_json(path_to_private_cache)
        working_private_cache = full_private_cache[workflow]
        gen_private_cache = full_private_cache['all_workflows']

        try:
            need_sql=True
            self.sql_user = gen_private_cache['sql_user']
            self.sql_pass = gen_private_cache['sql_pass']
            self.sql_server = gen_private_cache['sql_server']
            self.sql_db = gen_private_cache['sql_db']
            need_sql=False
            if wf == 1:
                self.lims_conn = working_private_cache['lims_conn']
            if wf == -2:
                self.folderpathbase = working_private_cache['folderpathbase']
            if wf == 7:
                self.destination = working_private_cache['destination']
                self.location = working_private_cache['location']
                self.port = working_private_cache['port']
                self.sftp_user = working_private_cache['sftp_user']
                self.sftp_pwd = working_private_cache['sftp_pwd']
            if wf == -4:
                self.folder_path_base = working_private_cache['folder_path_base']
            if wf == 6:
                self.lab = working_private_cache['lab']
                self.p_lab = working_private_cache['p_lab']
            if wf == -5:
                self.base_path = working_private_cache['base_path']
                self.new_base_path = working_private_cache['new_base_path']

        except KeyError:
            print("Looks like this is your first time using the script!")
            print("\nPlease fill out the following questions (we'll store \
results on-device so you won't have to enter them again).")
            if wf == 1:
                self.lims_conn = input("\nPlease enter the string for the LIMS connection \
(ie <user>/<password>@<db_tablename>\n-->")
            if wf == -2:
                print("Please select the folder you'd like to contain the finished file")
                self.folderpathbase = get_path_folder()
            if wf == 7:
                self.destination = input("\nType the relative path of the destination folder\n-->")
                self.location = input("\nType the address of the final location of sftp transfer\n-->")
                self.port = input("\nType the port to be used in transfer (typically 22)\n-->")
                self.sftp_user = input("\nType the username for sftp access\n-->")
                self.sftp_pwd = input("\nType the password for sftp access\n-->")
            if wf == -4:
                print("\nPlease select the path to the folder where you would like the \
                    queries to be stored.")
                self.folder_path_base = get_path()
            if wf == 6:
                self.lab = input("\nType the name of the lab submitting the report\n-->")
                self.p_lab = input("\nType the name of the lab performing the tests to appear on this report\n-->")
            if wf == -5:
                print("\nPlease select the path to the folder where ClearLabs \
                    Downloads used to be stored.")
                self.base_path = get_path()
                print("\nPlease select the path to the folder where ClearLabs \
                    Downloads are now stored.")
                self.new_base_path = get_path()

            if need_sql:
                self.sql_user = input("\nPlease enter the username for the sql database:\n-->")
                self.sql_pass = input("\nPlease enter the password for the sql database:\n-->")
                self.sql_server = input("\nPlease enter the server name for the sql database:\n-->")
                self.sql_db = input("\nPlease enter the name for the sql database:\n-->")

            
            print("\nFinished! If you need to change these values in the \
future for any reason, modify the cache file: daily_workflow/data/private_cache.json")
            if wf == 1:
                full_private_cache[workflow]['lims_conn'] = self.lims_conn
            if wf == -2:
                full_private_cache[workflow]['folderpathbase'] = self.folderpathbase
            if wf == 7:
                full_private_cache[workflow]['destination'] = self.destination
                full_private_cache[workflow]['location'] = self.location
                full_private_cache[workflow]['port'] = self.port
                full_private_cache[workflow]['sftp_user'] = self.sftp_user
                full_private_cache[workflow]['sftp_pwd'] = self.sftp_pwd
            if wf == -4:
                full_private_cache[workflow]['folder_path_base'] = self.folder_path_base
            if wf == 6:
                full_private_cache[workflow]['lab'] = self.lab
                full_private_cache[workflow]['p_lab'] = self.p_lab
            full_private_cache["all_workflows"]['sql_user'] = self.sql_user
            full_private_cache["all_workflows"]['sql_pass'] = self.sql_pass
            full_private_cache["all_workflows"]['sql_server'] = self.sql_server
            full_private_cache["all_workflows"]['sql_db'] = self.sql_db
            print("\nStoring data for future use...")
            res = write_json(path_to_private_cache, full_private_cache)
            if res != 0:
                raise ValueError("workflow_obj write to json failed!")
            # with open(path_to_cache, mode='w') as cache_file:
            #     json.dump(full_cache, cache_file, indent=4)
            print("\nContinuing the script in 5 seconds.")
            time.sleep(5)

    def setup_db(self):
        self.db_handler = ms_sql_handler(self)
        self.db_handler.establish_db()