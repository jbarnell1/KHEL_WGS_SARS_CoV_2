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
            ssh = pk.SSHClient()
            self.conn = ssh
            ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
            ssh.connect(self.ssh_ip, username=self.ssh_user, password=self.ssh_pwd, port=self.ssh_port)
            print(" Connected!\n")
        except Exception as e:
            print(e)
            time.sleep(4)


    def ssh_exec(self, command):
        return self.conn.exec_command(command)


    def ssh_send_file(self, src_path, app):
        filename = src_path.split("/")[-1]
        if app == "nextclade":
            path_to_dest = "nextclade-master/data/sars-cov-2/input/" + filename
        # if not nextclade, it is pangolin
        else:
            path_to_dest = "pangolin-master/pangolin/pangolin/data/" + filename
        try:
            ftp_client=self.conn.open_sftp()
            ftp_client.put(src_path, self.ssh_dest + path_to_dest)
            ftp_client.close()
        except Exception as e:
            print("An error has occurred!")
            ftp_client.close()
            print("\n\n", e)
            time.sleep(5)


    def ssh_receive_file(self, dest_path, app):
        # check which application is being used to generate paths
        if app == "nextclade":
            path_to_result = "nextclade-master/output/nextclade.tsv"
        # if not nextclade, it is pangolin
        else:
            path_to_result = "pangolin-master/pangolin/lineage_report.csv"
        try:
            ftp_client=self.conn.open_sftp()
            ftp_client.get(self.ssh_dest + path_to_result, dest_path)
            ftp_client.close()
        except Exception as e:
            print("An error has occurred!")
            ftp_client.close()
            print("\n\n", e)
            time.sleep(5)


    def close_connections(self):
        self.conn.close()