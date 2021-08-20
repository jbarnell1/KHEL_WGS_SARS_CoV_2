
# Overview
_______________________________________

### The docs section serves as an in-depth explanation of the logic and structure behind each of the scripts.

<br />
<br />

## The code is designed with several attributes in mind:

<br />

 - **Modularity:**
   - Each of the scripts has both a defined function and a call to that function if the script `__name__ == "__main__"`.
   - This allows the scripts to be called from the runner script as well as run on their own in case there was an error<br>in the runner script, the workflow can be manually finished by running each of the scripts in turn.

<br />

 - **Portability:**
   - This will be a big focus for the future, as currently only certain excel template files, sql server types, and folder structures are supported.  After the build is stable locally, I will attempt to improve portability to solve a wider range of problems.

<br />

 - **Simplicity:**
   - The focus of the scripts is to abstract away from analysts the complicated process of data management.  In addition to abstracted data management, many parameters exist in the `static_cache.json` file which allow easy alteration of the scripts function.

<br />

- **Reliability:**
  - In order to improve reliability, functions will be tested using pytest or unittest
  - On the user side, this means that having the correct packages and file structure is ensured.
  - On the developer side, this means robust testing before each release.

<br />
<br />

## How to use (once peripherals have been established):

<br />

- **Step 1: Start the runner script**
  - If you have established your peripherals as described in the [setup](setup.md) section, you will use the `main_workflow.py` script.  
  - Otherwise, you will need to navigate down the file structure of folders called `khel_wgs_sc2` until you find the file named `khel_wgs_sc2`.  This is the runner script for the package.

<br />

- **Step 2: Follow the prompts**
  - If the user selects the 'start' option after starting the script, the first 5 workflows will be run in tandem automatically.  Alternatively, each of those scripts (and all others in the package) can be run individually.
  - The workflow will direct you through the setup of initial values to store on device such as passwords, usernames, etc.  These values will be stored in the `data/private_cache.json` file within the package *locally*.
  - After the relevant information has been gathered, the workflow will continue.
  - Links to more information about the first 5 workflows are linked below:
    - [Importing demographics to database](WF_1_import_demos.md)
    - [Parsing run information from ClearLabs Website](WF_2_parse_run_data.md)
    - [Compiling multiple .fasta files into one](WF_3_compile_fasta.md)
    - [Parsing NextClade information](WF_4_parse_nextclade.md)
    - [Parsing Pangolin information](WF_5_parse_pangolin.md)

<br />

- **Step 3:**
  - After the 'start' workflow has finished, the user should generate a report of results added to the database, and may send it if they so choose.  This is done through workflows [6](WF_6_build_epi_report) and [7](WF_7_send_epi_report), respectively.  
  - As before, the script will walk you through any initial set up required, and will store results in the `data/private_cache.json` file within the package *locally*.

<br />

- **Beyond:**
  - There are several other scripts that users may select from, and shortcuts to those scripts are below:
    - [Import epi_isl numbers](epi_isl.md)
    - [Generate report for submission to GISAID](gisaid.md)
    - [Import data to database from template excel file](outside_lab.md)
    - [Querying the database simplified](query.md)
    - [Reset the database and import all data from an excel file](refresh.md)




