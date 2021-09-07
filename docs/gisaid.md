
# GISAID Report Generator
_______________________________________

### Generates two files: a metadata file for a list of samples, and a fasta file of all samples contained in the metadata file

<br />
<br />

## How to use the GISAID report:

<br />

 - **Step 1**
   - Start the script, and type 'gisaid' to enter the gisaid report generator script.

<br />

 - **Step 2**
   - Follow any prompts for the first time using the script.  Data gathered will be stored in `data/private_cache.json` for future use.  The data stored will be:
     - **default_state:**  The region that most samples arrive from, according to GISAID formatting rules.  For example:
       - `North America / USA / Kansas`
       - `Europe / France / Bretagne / Vannes`
     - **authors:** The names of all individuals involved in generating the report.
     - **folderpathbase:** The path to the folder where the gisaid report should be stored.
       - *Note: The actual report will be saved one folder lower than the selected folder, as the folder structure is `folderpathbase/date/report.xlsx`.*
     - **lab_name:** The name of the lab compiling/submitting the report to GISAID.
     - **lab_addr:** The address of the lab compiling/submitting the report to GISAID.
   - The final prompt you will receive is for the user generating the report.  
   - This **must** be the same as the username for the [GISAID.org](https://www.gisaid.org/) account submitting the report.

<br />

 - **Step 3**
   - The script at this point reviews all samples from the last seven days by `wgs_run_date` for eligibility for submission to GISAID, and if it finds any, compiles a report and fasta for the samples.
   - The files may be found in the folder: `folderpathbase/date/report.xlsx` and `folderpathbase/date/all_fasta.fasta` 

<br />

 - **Step 4**
   - Now that the file has been generated, you must copy the contents of the gisaid report into the template for submission to GISAID.
   - The script is written to mirror the structure of the most recent template available from GISAID, so a simple copy/paste allows you to move data directly into the template file for submission.
     - *Note: The first column, `hsn`, should not be included in the copy/paste.  It is included in the report for identification purposes for the script user only, and should not be sent to GISAID.*

<br />

 - **Step 5**
   - Follow the GISAID guidelines for submitting the report.
   - It can be helpful to first submit the .fasta file to the [pre-analysis](https://www.gisaid.org/epiflu-applications/covsurver-mutations-app/) tool provided by GISAID to identify framshift indels that may cause samples in the submission to be rejected.
   - Reports can be submitted [here](https://www.epicov.org/epi3/frontend#43b970)

<br />
<br />

## How the GISAID report works:

### I will split the logic up into the functions that the script calls from its helper file.

<br />

- **get_json()**
  - Loads data relevant for script into memory.
  - Requests additional information from user if first time using the script.
  - See description for how the get_json() call works to import relevant data for each script as it is called from the [workflow_obj](workflow_obj.md) doc.

<br />

- **scan_db()**
  - Scan database for all eligible samples for submission.  Eligibility determined by:
    - Samples run in the last week, according to `wgs_run_date` column
    - Samples with percent coverage above the set cutoff.
      - To alter the cutoff values, see the docs about the [`.json`](json.md) files
    - Samples with values for the following columns:
      - `path_to_fasta` (non-NULL)
        - paths to `.fasta` file for each sample is required to build the submission file.
      - `gisaid_num` (NULL)
        - If a sample has a `gisaid_num`, it has already been submitted.
      - `gisaid_epi_isl` (NULL)
        - If a sample has a `gisaid_epi_isl` number, it has already been submitted.
      - `doc` (non-NULL)
        - Date of collection is required by GISAID for submission.
  - Execute query, collecting satisfactory samples into a list for later use.

<br />

- **get_gisaid_df()**
  - Query database for all samples in the satisfactory samples list, and convert output to Pandas DataFrame for manipulation
  - Ask for user generating report, store for future use.

<br />

- **compile_fasta()**
  - Build path to fasta file
    - Each fasta file name includes a number that increments if a fasta file with the same name has already been saved in the folder.  This allows users to submit multiple times in the same day while maintaining track of each submission.
    - The file number is matched with the `.xlsx` report so that the user does not lose track of which fasta file goes with which metadata file.
    - Store a list of paths to all fasta files (this comes from the `path_to_fasta` column of the gisaid DataFrame generated in the step above)

<br />

- **compile_gisaid()**
  - Rename, add, format, sort, and remove columns to match the template submission file for GISAID.  This allows for easier copy/pasting for the user later.
    - A critical step in this process is the `get_virus_name` function, which calculates the next gisaid number to use, and assigns the virus name with the following structure: <br>`hCoV-19/lab_id/<year_of_collection>`, where the lab_id contains the assigned gisaid_number.
    - In this function, the gisaid number is connected to the sample, so that the `make_fasta_file` function knows what to name each fasta entry in the file.
  - The altering of the gisaid DataFrame is described in the `static_cache.json` file.  See [`.json`](json.md) doc for more info.

<br />

- **make_fasta_file()**
  - Open each file in list of fasta files generated in the `compile_fasta` step
  - If the line starts with a "`>`" character, it contains the virus name.  The virus name contains the gisaid number, and must match the virus name given in the gisaid DataFrame.  Since the DataFrame and list are both ordered, we can use indices to match virus names with their metadata.
    - This requires replacing the original virus header in each fasta file with the virus name located in the DataFrame, and generated using the assigned `gisaid_num` for that sample.
  - We now write the data from the file into a master file saved at the location that we determined in the `compile_fasta` step.

<br />

- **make_gisaid_file()**
  - Save the gisaid DataFrame to a `.xlsx` file
  - Destination calculated by today's date, and the file number found by the `compile_fasta` step

<br />

- **database_push()**
  - We need to store the assigned gisaid numbers for each sample in the sql database, so we push that data to the database in this step.