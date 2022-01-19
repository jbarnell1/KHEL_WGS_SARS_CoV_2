from abc import ABC
from workflow.ui import get_path_folder
from workflow.ms_sql_handler import ms_sql_handler
from workflow.ssh_handler import ssh_handler
from workflow.reader import read_json
from workflow.ui import get_path
from workflow.ui import get_path_folder
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
            elif wf == -6:
                workflow = 'plotter'

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
        try:
            working_private_cache = full_private_cache[workflow]
        except KeyError:
            full_private_cache[workflow] = {}
            write_json(path_to_private_cache, full_private_cache)
            working_private_cache = full_private_cache[workflow]
        gen_private_cache = full_private_cache['all_workflows']

        try:
            need_sql=True
            self.sql_user = gen_private_cache['sql_user']
            self.sql_pass = gen_private_cache['sql_pass']
            self.sql_server = gen_private_cache['sql_server']
            self.sql_db = gen_private_cache['sql_db']
            need_sql=False

            need_reportable = True
            self.reportable = gen_private_cache['reportable']
            need_reportable = False

            include_controls = True
            self.include_controls = gen_private_cache['include_controls']
            include_controls = False

            need_analysis_pathway = True
            need_ssh = True
            self.analysis_pathway = gen_private_cache['analysis_pathway']
            need_analysis_pathway = False
            if self.analysis_pathway == "cli":
                self.ssh_ip = gen_private_cache['ssh_ip']
                self.ssh_user = gen_private_cache['ssh_user']
                self.ssh_pwd = gen_private_cache['ssh_pwd']
                self.ssh_port = gen_private_cache['ssh_port']
                self.ssh_dest = gen_private_cache['ssh_dest']
                need_ssh = False
            
            need_ctrls = True
            self.neg_ctrl_lot = gen_private_cache['neg_ctrl_lot']
            self.neg_ctrl_exp = gen_private_cache['neg_ctrl_exp']
            self.pos_ctrl_lot = gen_private_cache['pos_ctrl_lot']
            self.pos_ctrl_exp = gen_private_cache['pos_ctrl_exp']
            need_ctrls = False

            if wf == 1:
                self.priority_path = working_private_cache['priority_path']
                self.lims_conn = working_private_cache['lims_conn']
            if wf == -2:
                self.default_state = working_private_cache['default_state']
                self.folderpathbase = working_private_cache['folderpathbase']
                self.authors = working_private_cache['authors']
                self.lab_name = working_private_cache['lab_name']
                self.lab_addr = working_private_cache['lab_addr']
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
                self.folderpathbase = working_private_cache['folderpathbase']
            if wf == -5:
                self.base_path = working_private_cache['base_path']
                self.new_base_path = working_private_cache['new_base_path']
            if wf == -6:
                self.base_path = working_private_cache['base_path']
            if wf == 9:
                self.base_path = working_private_cache['base_path']

        except KeyError:
            print("Looks like this is your first time using the script!")
            print("\nPlease fill out the following questions (we'll store \
results on-device so you won't have to enter them again).")
            if wf == 1:
                print("Please select the path to the .txt document containing the list of priority samples")
                self.priority_path = get_path()
                self.lims_conn = input("\nPlease enter the string for the LIMS connection \
(ie <user>/<password>@<db_tablename>\n-->")
            if wf == -2:
                print("Please select the folder you'd like to contain the finished file")
                self.folderpathbase = get_path_folder()
                self.default_state = input("\nPlease type the state you'd like unknown sample locations to default to \
on reports.\n--> ")
                self.authors = input("\nPlease type the authors of the document\n--> ")
                self.lab_name = input("\nPlease type the name of the lab submitting the report\n--> ")
                self.lab_addr = input("\nPlease type the address of the lab submitting the report\n--> ")
            if wf == 7:
                self.destination = input("\nType the relative path of the destination folder\n--> ")
                self.location = input("\nType the address of the final location of sftp transfer\n--> ")
                self.port = input("\nType the port to be used in transfer (typically 22)\n--> ")
                self.sftp_user = input("\nType the username for sftp access\n--> ")
                self.sftp_pwd = input("\nType the password for sftp access\n--> ")
            if wf == -4:
                print("\nPlease select the path to the folder where you would like the \
queries to be stored.")
                self.folder_path_base = get_path()
            if wf == 6:
                self.lab = input("\nType the name of the lab submitting the report\n--> ")
                self.p_lab = input("\nType the name of the lab performing the tests to appear on this report\n-->")
                print("\nPlease select the path to the Results folder where the reports should be saved.")
                self.folderpathbase = get_path_folder()
            if wf == -5:
                print("\nPlease select the path to the folder where ClearLabs \
Downloads used to be stored.")
                self.base_path = get_path_folder()
                print("\nPlease select the path to the folder where ClearLabs \
Downloads are now stored.")
                self.new_base_path = get_path_folder()
            if wf == -6:
                print("\nPlease select the path to the folder where the \
Plots should be stored")
                self.base_path = get_path_folder()
            if wf == 9:
                print("\nPlease select the path to the folder where the \
passing fasta files should be stored")
                self.base_path = get_path_folder()

            if need_sql:
                self.sql_user = input("\nPlease enter the username for the sql database:\n-->")
                self.sql_pass = input("\nPlease enter the password for the sql database:\n-->")
                self.sql_server = input("\nPlease enter the server name for the sql database:\n-->")
                self.sql_db = input("\nPlease enter the name for the sql database:\n-->")

            if need_analysis_pathway:
                self.analysis_pathway = input("\nPlease enter 'online' if you plan to perform the nextclade and pangolin analysis \
using the online tools.\nPlease enter 'cli' if you plan to perform the nextclade and pangolin analysis using a separate system\n--> ")

            if need_ssh:
                self.ssh_ip = input("\nPlease type the ip address of the server you'd like to access (if you will run the pangolin/nextclade \
analysis on the current computer, use '127.0.0.1')\n--> ")
                self.ssh_user = input("\nPlease enter the user name of the server to be used for the pangolin/nextclade analysis\n--> ")
                self.ssh_pwd = input("\nPlease enter the password of the server to be used for the pangolin/nextclade analysis\n--> ")
                self.ssh_port = input("\nPlease enter the port number to use for communication with the server for pangolin/nextclade analysis \
(typically port '8080' or '8088' will work fine.)\n--> ")
                self.ssh_dest = input("\nPlease type the location of the nextclade package on the server.\n--> ")
            
            if need_ctrls:
                self.neg_ctrl_lot = input("\nPlease type the lot number for the negative control (something like 'AF29484103')\n--> ")
                self.neg_ctrl_exp = input("\nPlease type the expiration date for the negative control, formatted YYYY-MM-DD (something like '2021-02-19')\n--> ")
                self.pos_ctrl_lot = input("\nPlease type the lot number for the positive control (something like 'AF29484103')\n--> ")
                self.pos_ctrl_exp = input("\nPlease type the expiration date for the positive control, formatted YYYY-MM-DD (something like '2021-02-19')\n--> ")
            
            if include_controls:
                self.include_controls = int(input("\nPlease type 0 if there are no controls included on this run, and 1 if there are controls included.\n--> "))

            if need_reportable:
                self.reportable = int(input("\nPlease type 0 if you don't want the results to be reportable and 1 if you would like the results to be reportable.\n--> "))

            print("\nFinished! If you need to change these values in the \
future for any reason, modify the cache file: daily_workflow/data/private_cache.json")
            if wf == 1:
                full_private_cache[workflow]['priority_path'] = self.priority_path
                full_private_cache[workflow]['lims_conn'] = self.lims_conn
            if wf == -2:
                full_private_cache[workflow]['default_state'] = self.default_state
                full_private_cache[workflow]['folderpathbase'] = self.folderpathbase
                full_private_cache[workflow]['authors'] = self.authors
                full_private_cache[workflow]['lab_name'] = self.lab_name
                full_private_cache[workflow]['lab_addr'] = self.lab_addr
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
                full_private_cache[workflow]['folderpathbase'] = self.folderpathbase
            if wf == -6:
                full_private_cache[workflow]['base_path'] = self.base_path
            if wf == 9:
                full_private_cache[workflow]['base_path'] = self.base_path
            full_private_cache["all_workflows"]['sql_user'] = self.sql_user
            full_private_cache["all_workflows"]['sql_pass'] = self.sql_pass
            full_private_cache["all_workflows"]['sql_server'] = self.sql_server
            full_private_cache["all_workflows"]['sql_db'] = self.sql_db
            full_private_cache["all_workflows"]['analysis_pathway'] = self.analysis_pathway
            full_private_cache["all_workflows"]['ssh_ip'] = self.ssh_ip
            full_private_cache["all_workflows"]['ssh_user'] = self.ssh_user
            full_private_cache["all_workflows"]['ssh_pwd'] = self.ssh_pwd
            full_private_cache["all_workflows"]['ssh_port'] = self.ssh_port
            full_private_cache["all_workflows"]['ssh_dest'] = self.ssh_dest
            full_private_cache["all_workflows"]['neg_ctrl_lot'] = self.neg_ctrl_lot
            full_private_cache["all_workflows"]['neg_ctrl_exp'] = self.neg_ctrl_exp
            full_private_cache["all_workflows"]['pos_ctrl_lot'] = self.pos_ctrl_lot
            full_private_cache["all_workflows"]['pos_ctrl_exp'] = self.pos_ctrl_exp
            full_private_cache["all_workflows"]['reportable'] = self.reportable

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

    def setup_ssh(self):
        self.ssh_handler = ssh_handler(self)
        # client_ssh is for sending commands to server
        self.ssh_handler.establish_client_ssh()
