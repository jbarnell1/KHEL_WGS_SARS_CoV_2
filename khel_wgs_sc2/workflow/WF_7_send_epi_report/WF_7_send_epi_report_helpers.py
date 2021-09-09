from ..workflow_obj import workflow_obj
from ..ui import get_path
import sys
import paramiko as pk
import time


class WorkflowObj7(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_7"


    # methods
    def get_json(self):
        super().get_json(7)


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
        print("\nBuilding Transporter Object...")
        # establish connection
        transport = pk.Transport((self.location, int(self.port)))
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
        finally:
            self.sftp.close()
        print("File successfully sent!\n")