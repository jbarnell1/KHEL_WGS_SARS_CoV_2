# Workflow 1 Script
_______________________________________

### Gets list of samples from excel file, and grabs all demographics from the LIMS database, finally pushes them to the main SQL database.

<br />
<br />

## How to use the Workflow 1 Script:

<br />

 - **Step 1**
   - Start the main script, and type either `start` or `1` to enter the first step of the daily workflow script.
     - If you enter `start`, the script will move from steps 1 to 5 automatically

<br />

 - **Step 2**
   - Follow any prompts for the first time using the script.  Data gathered will be stored in `data/private_cache.json` for future use.  The data stored will be:
     - **lims_conn:**  The login string to use to access the LIMS database (Oracle SQL).  The format is: {`user`}/{`table`}@{`database_name`}
       - `user`: username to access the database
       - `table`: table name that contains patient demographics in the Oracle SQL database
       - `database_name`: name of the Oracle SQL database
   - Next, the script will ask the user to select an excel document containing a list of the samples on a machine's run.  This is the last user intervention required for the script to run correctly.

<br />

 - **Step 3**
   - The script at this point builds a list of all samples contained in the excel document supplied by the user and queries the Oracle SQL database for all patient demographics, formats the demographics, and pushes them to the main SQL database.
   - For KDHE, the same document used to upload sample names into the ClearLabs machine is the same document selected by the user in the previous step.

<br />
<br />

## How the Workflow 1 Script works:

### I will split the logic up into the functions that the script calls from its helper file.

<br />

- **get_json()**
  - Loads data relevant for script into memory.
  - Requests additional information from user if first time using the script.
  - See description for how the get_json() call works to import relevant data for each script as it is called from the [workflow_obj](workflow_obj.md) doc.

<br />

- **get_initial_demo_df()**
  - Prompt user for path to excel file holding list of HSNs on given machine run.
  - Read excel file into pandas `DataFrame`.
  - Drop controls from the DataFrame of HSNs, since the controls will not be in the LIMS database


<br />

- **format_demo_df()**
  - Remove any samples with "pool" in the label, won't be in the LIMS database (case-insensitive)
  - Remove any samples with "blank" in the label, won't be in the LIMS database (case-insensitive)
  - Rename column of dataframe to 'hsn'
  - Drop any duplicate HSN's from the DataFrame

<br />

- **get_initial_lims_df()**
  - Grab list of HSN's from the DataFrame
  - Connect to the LIMS database and query patient demographics from list in previous step into new DataFrame

<br />

- **format_lims_df()**
  - Rename columns in LIMS DataFrame, convert HSN column type to `str`

<br />

- **merge_dfs()**
  - Execute a Pandas `merge` on the two dataframes (HSN DataFrame + LIMS DataFrame) on `'hsn'`

<br />

- **format_dfs()**
  - Format columns appropriately.  Alters/creates:
    - `pcr_run_date`
    - `wgs_run_date`
    - `date_recd`
    - `f_name`
    - `l_name`
    - `age`
    - `doc`
    - `dob`
    - `sex`
    - `state`
    - `facility`
    - `facility_category`
    - `source`
    - `race`
  - Sort columns


<br />

- **database_push()**
  - Push DataFrame to the database in this step.