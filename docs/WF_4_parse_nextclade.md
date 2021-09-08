# Workflow 4 Script
_______________________________________

### Runs and analyzes the `all_date_num.fasta` file using the nextclade tool, and pushes the results to the database.

<br />
<br />

## How to use the Workflow 4 Script:

<br />

 - **Step 1**
   - Start the main script, and type `4` to enter the fourth step of the daily workflow script.
   - Alternatively, this script is called as the fourth step to the `start` command.

<br />

 - **Step 2**
   - Follow any prompts for the first time using the script.  Currently, no private data is gathered for this workflow.
   - *If the user has specified 'cli' as the `analysis pathway` in `private_cache.json`:*
     - If this script is called as the fourth step to the `start` command, no user input is required, as the path to the `all_fasta.fasta` file was returned in the previous step.  Go to **Step 3**.
     - If this script is called by typing `4` at the start of the daily workflow script, the user must specify the `.fasta` file they would like to be analyzed.  Once selected the program proceeds to **Step 3**.
   - *If the user specified 'online' as the `analysis pathway` in `private_cache.json`:*
     - The user must perform the [Nextclade](https://clades.nextstrain.org/) and [Pangolin](https://pangolin.cog-uk.io/) analysis using the linked online tools, and save the results back into the parent folder (mmddyy.machine_num.day_run_num).  Since the user has performed the analysis, the script then moves to **Step 4**.

<br />

 - **Step 3**
   - *This step is only performed if the `analysis pathway` key in the `private_cache.json` file is set to 'cli'.*
   - The script continues by connecting to remote linux 'server' containing the CLI versions of both nextclade and pangolin.  
   - Next, it will send the `.fasta` file to the remote server and use ssh ([paramiko](http://docs.paramiko.org/en/stable/)) to call the appropriate commands to run the analysis.
     - *Note:* see the [ssh handler](ssh_handler.md) docs for more information on how to set up the remote server appropriately.
   - Finally, the script sends the output file back to the parent folder on the windows PC and closes the ssh connection.

<br />

 - **Step 4**
   - At this step, the results files should be stored in the parent folder, ready for the script to take the next step.
   - *If the `analysis pathway` key is set to `cli`:*
     - The script already has the path to the results file saved, no user input needed.
   - *If the `analysis pathway` key is set to `online`:*
     -  The script now prompts the user to select the `.tsv` results file from nextclade to analyze.
   - Finally, the script formats the `.tsv` file and saves the information to the main SQL database

<br />
<br />

## How the Workflow 4 Script works:

### I will split the logic up into the functions that the script calls from its helper file.

<br />

- **get_json()**
  - Loads data relevant for script into memory.
  - Requests additional information from user if first time using the script.
  - See description for how the get_json() call works to import relevant data for each script as it is called from the [workflow_obj](workflow_obj.md) doc.

<br />

- **send_fasta()** - (`cli` only)
   - Store the name of the fasta file for later
   - Establish connection to the server
   - Send the file to the linux server at the specified location

<br />

- **run_nextclade()** - (`cli` only)
  - Send commands to the linux server to run the local nextclade analysis, and output the results to a specified location

<br />

- **receive_nextclade_df()** - (`cli` only)
  - Pull the results file from the step above back into the parent folder with the name `nextclade.tsv`

<br />

- **clean_connections()** - (`cli` only)
  - Close any open connections between the windows PC and the linux server

<br />

- **get_nextclade_dfs(nc_path)**
  - If the `analysis pathway` is 'online', prompt the user to select the nextclade results file.
    - If the `analysis pathway` is 'cli', then the script already knows the location and name of the nextclade results file.
  - Remove any samples with "pool" in the label
  - Remove any samples with "blank" in the label
  - Format columns appropriately.  Alters/creates:
    - `hsn`
    - `machine_num_var`
    - `position`
    - `day_run_num_var`
    - `wgs_run_date_var`
    - `nextclade_version`
  - Split the developed dataframe into two dataframes corresponding to information needing pushed to Results table and Run_Stats table
  - Sort columns

<br />

- **database_push()**
  - Push relevant DataFrames to the database in this step.

