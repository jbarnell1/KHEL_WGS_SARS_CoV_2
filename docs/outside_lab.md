# Outside Lab Importer
_______________________________________

### Fills in Outside Lab excel file into database

<br />
<br />

## How to use the Outside Lab script:

<br />

 - **Step 1**
   - Start the script, and type `outside lab` to enter the gisaid report generator script.

<br />

 - **Step 2**
   - Follow any prompts for the first time using the script.  Currently, no private data is gathered for this workflow.
   - Next, the script will ask the user to select the template from an outside lab to upload to the database.

<br />

 - **Step 3**
   - The script at this point builds a DataFrame from the template file, and pushes the information into the database.

<br />
<br />

## How the Outside Lab script works:

### I will split the logic up into the functions that the script calls from its helper file.

<br />

- **get_json()**
  - Loads data relevant for script into memory.
  - Requests additional information from user if first time using the script.
  - See description for how the get_json() call works to import relevant data for each script as it is called from the [workflow_obj](workflow_obj.md) doc.

<br />

- **get_outside_lab_dfs()**
  - Ask user to select the excel file and read into pandas DataFrame
  - Format columns appropriately.  Alters/creates:
    - `path_to_fasta`
    - `avg_depth`
    - `percent_cvg`
    - `f_name`
    - `l_name`
    - `pango_learn_version`
    - `platform`
    - `machine_num`
    - `position`
    - `day_run_num`
    - `gisaid_num`
    - `source`
    - `age`
    - `sex`
    - `state`
    - `facility`
  - Format all date-related columns
  - Format all str-type columns
  - Split dataframe into two tables: one to push to `Results` Table, one to push to `Run_Stats` Table.
  - Remove duplicates, and format HSNs
  - All helper functions in this script have sisters in the formatter, but due to complications, they remain in this script as well as the formatter.

<br />

- **database_push()**
  - Store created dataframes into both tables using the `lst_ptr_push` function of the [ms_sql_handler](ms_sql_handler.md) class.


