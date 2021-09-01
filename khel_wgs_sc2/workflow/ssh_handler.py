import paramiko as pk
import time
import sys


class ssh_handler():
    # constructor
    def __init__(self, obj):
        self.ssh_user = obj.ssh_user
        self.ssh_pwd = obj.ssh_pwd
        self.ssh_ip = obj.ssh_ip
        self.ssh_port = obj.ssh_port
        self.ssh_dest = obj.ssh_dest

    # methods
    # create
    def establish_client_ssh(self):
        try:
            print("\nBuilding SSH Client Object...")
            self.conn = ssh = pk.SSHClient()
            ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
            ssh.connect(self.ssh_ip, username=self.ssh_user, password=self.pwd, port=self.port)
            print(" Connected!\n")
        except:
            time.sleep(4)
    

    def establish_transporter(self):
        try:
            print("\nBuilding Transporter Object...")
            # establish connection
            transport = pk.Transport((self.ssh_location, int(self.ssh_port)))
            transport.connect(username=self.ssh_user, password=self.ssh_pwd)
            self.ssh_sftp = pk.SFTPClient.from_transport(transport)
            print(" Connected!\n")
        except:
            time.sleep(4)


    def ssh_exec(self, command):
        self.conn.exec_command(command)


    def ssh_send_file(self, src_path):
        try:
            self.ssh_sftp.put(src_path, self.ssh_dest)
        except Exception as e:
            print("An error has occurred!")
            print("\n\n", e)
            time.sleep(5)
        finally:
            self.ssh_sftp.close()


    def ssh_receive_file(self, dest_path, app):
        # check which application is being used to generate paths
        if app == "nextclade":
            path_to_result = "nextclade-master/output/nextclade.tsv"
        # if not nextclade, it is pangolin
        else:
            path_to_result = "pangolin-master/pangolin/pangolin/data/lineage_report.csv"
        try:
            self.ssh_sftp.get(self.ssh_dest + path_to_result, dest_path)
        except Exception as e:
            print("An error has occurred!")
            print("\n\n", e)
            time.sleep(5)
        finally:
            self.ssh_sftp.close()


    def close_connections(self):
        self.conn.close()
        self.ssh_sftp.close()