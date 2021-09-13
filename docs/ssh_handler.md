
# SSH_Handler Class
_______________________________________

### Abstracts common functions for scripts to maintain readability and brevity

<br />
<br />

## How the SSH_Handler class works:

### **Variables**
______

<br />

- Created from class Function:
  - **conn**
- Pulled in from `private_cache.json` and `static_cache.json`
  - **ssh_user**
  - **ssh_pwd**
  - **ssh_ip**
  - **ssh_port**
  - **ssh_dest**

<br />

### **Functions**
_____
<br />

- **establish_client_ssh()**
  - Attempt to create [Paramiko SSHClient](http://docs.paramiko.org/en/stable/api/client.html) using the private data (username, password, port, ip) from `private_cache.json` and store in the `self.conn` variable.

<br />

- **ssh_exec()**
  - Using the connection established above, execute command using paramiko's `exec_command()`.

<br />

- **ssh_send_file()**
  - Using the connection established above, push the selected file to the destination file, depending on whether the app being used is nextclade or pangolin.

<br />

- **ssh_receive_file()**
  - Same as `ssh_send_file` except pull file from client, and put in host.

<br />

- **close_connections()**
  - Safely close SSHClient() connection.


