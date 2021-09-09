# Workflow 7 Script
_______________________________________

### Simple script to move excel file from one location to another over a network using *ssh* and the [`paramiko`](http://docs.paramiko.org/en/stable/) library

<br />
<br />

## How to use the Workflow 7 Script:

<br />

 - **Step 1**
   - Start the main script, and type `7` to enter the first step of the daily workflow script.
     - This script is outside of the `start` function call

<br />

 - **Step 2**
   - Follow any prompts for the first time using the script.  Data gathered will be stored in `data/private_cache.json` for future use.  The data stored will be:
     - **destination:**  The path to the destination of the file being sent
     - **location:** Host name of destination
     - **port:** port used for ssh, typically `22`
     - **sftp_user:** username to log into the `location`
     - **sftp_pwd:** password to log into the `location`
   - Next, the script will ask the user to select the `.csv` report to send over ssh:
     - The script verifies that the user has selected a `.csv` file

<br />

 - **Step 3**
   - The script at this point sends the file to the destination set in the previous step and closes the ssh connection.
     - *Note:* at this time the script does not utilize the [ssh_handler](ssh_handler.md) class.  Only Workflows [4](WF_4_parse_nextclade.md) and [5](WF_5_parse_pangolin.md) use that class at this time.

<br />
<br />

## How the Workflow 7 Script works:

### I will split the logic up into the functions that the script calls from its helper file.

<br />

- **get_json()**
  - Loads data relevant for script into memory.
  - Requests additional information from user if first time using the script.
  - See description for how the get_json() call works to import relevant data for each script as it is called from the [workflow_obj](workflow_obj.md) doc.

<br />

- **get_file_path()**
  - Prompt user to select `.csv` file to send.
  - Verify file to send is a `.csv`

<br />

- **make_transporter()**
  - Build transporter object that will be used to send the file over ssh

<br />

- **send_file()**
  - Send file using the [sftp.put](http://docs.paramiko.org/en/stable/api/sftp.html) function
  - Close the function


