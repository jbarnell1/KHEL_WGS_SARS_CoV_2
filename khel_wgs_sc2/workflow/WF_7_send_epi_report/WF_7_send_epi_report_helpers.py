from ..processor import *
from ..workflow_obj import workflow_obj
from ..reader import *
from ..writer import *
from ..ui import *
from ..formatter import *
import sys
import paramiko as pk
import time


class WorkflowObj7(workflow_obj):
    # constructor
    def __init__(self, logger):
        self.logger = logger
        self.id = "WF_7"

    # methods
    def get_json(self):
        self.logger.info(self.id + ": Acquiring local data from cache")
        super().get_json(7)
        self.logger.info(self.id + ": get_json finished!")

    def get_file_path(self):
        try:
            print("Use the following dialog box to select the file to send to epi")
            self.source = get_path()
            ext_lst = self.source.split(".")
            ext = ext_lst[-1]
            if ext != "csv":
                raise Exception
            print(" Success!\n")
        except Exception as e:
            print("\n" + self.source + " results in an error.  Please check spelling\
                \n and that the file is a .csv format and is not open and try again.\n")
            print(e)
            raise

    def make_transporter(self):
        
        print("\nEstablishing database connection...")
        # establish connection
        transport = pk.Transport((self.location, self.port))
        transport.connect(username=self.sftp_user, password=self.sftp_pwd)
        self.sftp = pk.SFTPClient.from_transport(transport)

        print(" Connected!\n")

    def send_file(self):
        print("\nAttempting to send file...")
        try:
            # transfer file
            folder_lst = self.source.split("/")
            file_name = folder_lst[-1]
            self.sftp.put(self.source, self.destination + file_name)
        except Exception as e:
            print("An error has occurred!")
            print("\n\n", e)
            time.sleep(5)
            sys.exit()
        finally:
            self.sftp.close()
        
        print("File successfully sent!\n")