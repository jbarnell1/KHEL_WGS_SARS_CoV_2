
# Overview
_______________________________________

### The docs section serves as an in-depth explanation of the logic and structure behind each of the scripts.

<br />
<br />

## The code is designed with several attributes in mind:
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
  - In order to improve reliability, testing functions using pytest or unittest
  - On the user side, this means that having the correct packages and file structure is ensured.
  - On the developer side, this means robust testing before each release.

<br />

## How to use (once peripherals have been established):

- **Step 1: Start the runner script**
  - If you have established your peripherals as described in the [setup](setup.md) section, you will use the `main_workflow.py` script.  
  - Otherwise, you will need to navigate down the file structure of folders called `khel_wgs_sc2` until you find the file named `khel_wgs_sc2`.  This is the runner script for the package.

<br />

- **Step 2: Follow the prompts**
  - The workflow will direct you through the setup of initial values to store on device such as passwords, usernames, etc.  These values will be stored in the `data/private_cache.json` file within the package *locally*.
  - After the relevant information has been gathered, the workflow will continue.
  - 

<br />

- **Step 3: 


<br /><br /><br /><br /><br />

  > This step is absolutely required, since the HSN is the primary key in the database<br>
  > making it impossible to insert any other results further down the workflow.

 - **Workflow 2:** Parse Run Statistics (Data)
   - Ask user for run data (currently only supports CL run data, copy/paste functionality).
   - Push run data to SARS_COV_2 MS SQL database (Table 1 and Table 2).

  > *Run statistics* will be used to identify which duplicate is selected to be represented in the
  > Results table

 - **Workflow 3:** Compile FASTA
   - Ask user for path to download folder (typically the FAST files folder) of files<br>that should be concatenated.
   - Concatenate fasta files, store new all_fasta file in parent folder, and save<br>pointers to each sample fasta.
   - Push the fasta pointers to both tables in the SARS_COV_2 MS SQL database.

  > At this point users should pass the fasta file to [nextclade][1] and [pangolin_lineage_analyzer][2].<br>
  > The `.tsv` download should be selected from the nextclade site, and the `.csv` download should be selected<br>
  > from the pangolin site.  Both should be stored in the parent folder for the run where the `all_fasta.fasta`<br>
  > file is located.

 - **Workflow 4:** Parse Nextclade data
   - Extract required data from user-provided `nextclade(n).tsv` file.
   - Push the Nextclade data to both tables.
 
 - **Workflow 5:** Parse Pangolin data
   - Extract required data from user-provided `results(n).csv` file.
   - Push the Pangolin data to the *results table* only.

All of these workflows can be run on their own, but I've provided a runner script that can call each one, waiting for the user<br>
to complete the critical steps.  For more information on each workflow, see the [docs](docs/overview.md).