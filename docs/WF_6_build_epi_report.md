# Workflow 6 Script
_______________________________________

### Gathers sample data from the SQL database as requested by the user, and formats the data into appropriate format for submission

<br />
<br />

## How to use the Workflow 6 Script:

<br />

 - **Step 1**
   - Start the main script, and type `6` to enter the first step of the daily workflow script.
     - This script is outside of the `start` function call

<br />

 - **Step 2**
   - Follow any prompts for the first time using the script.  Data gathered will be stored in `data/private_cache.json` for future use.  The data stored will be:
     - **lab:**  The name of the lab submitting the report.
     - **p_lab:** The name of the lab performing the test results presented in the report
     - **folderpathbase:** path to the Results folder that will contain the formatted excel data files extracted from the SQL database
   - Next, the script will ask the user how the data should be selected.
     - Choosing `d`: select all samples from a given date
     - Choosing `a`: select all samples from the database
     - Choosing `r`: select all samples from a date range
     - Choosing `s`: select all samples submitted by a given facility (such as using [outside_lab](outside_lab.md) import.
     - Choosing `f`: select all samples collected by a given facility.
   - The script has secondary questions associated with each selection.  For example, after selecting `d`, the user will be prompted to provide the date to be selected.

<br />

 - **Step 3**
   - The script at this point queries the database for all samples that match parameters that the user has set, and saves the resulting DataFrames into .xlsx files.

<br />
<br />

## How the Workflow 6 Script works:

### I will split the logic up into the functions that the script calls from its helper file.

<br />

- **get_json()**
  - Loads data relevant for script into memory.
  - Requests additional information from user if first time using the script.
  - See description for how the get_json() call works to import relevant data for each script as it is called from the [workflow_obj](workflow_obj.md) doc.

<br />

- **get_ui()**
  - Prompt user for input as described above.
  - Edit queries to the database corresponding to the user's selection

<br />

- **get_df()**
  - Read query formatted in previous step into DataFrame.
  - Some selections will also add a `bad_df` DataFrame including samples that match the user's selection but fail to pass the quality controls set in `static_cache.json`.

<br />

- **format_df()**
  - Format columns appropriately.  Alters/creates:
    - `Lab`
    - `Patient_Last_Name`
    - `Patient_First_Name`
    - `Patient_DOB`
    - `Patient_Gender`
    - `Ordering_Facility`
    - `Accession_Number`
    - `Specimen_Collection_Date`
    - `Specimen_Source`
    - `Test_Date`
    - `Lineage_ID`
    - `Clade`
    - `GISAID_Number`
    - `Race`
    - `Ethnicity`
    - `Performing_Lab`
    - `Report_Sent_Date`
  - Sort columns
  - Format bad_df columns appropriately. Alters/creates:
    - `hsn`
    - `percent_cvg`
    - `avg_depth`
    - `total_ns` 
    - `pos_pass` 
    - `neg_pass` 
    - `clade`
    - `lineage_id` 
    - `facility` 
    - `f_name` 
    - `l_name` 
    - `sex` 
    - `age` 
    - `dob`
  - Sort bad_df columns

<br />

- **write_epi_report()**
  - Save DataFrame(s) into excel file at `folderpathbase/date`

