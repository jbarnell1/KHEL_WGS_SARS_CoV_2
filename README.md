
# General Package for State Lab SARS-CoV-2 Analysis
_______________________________________

## Get started with this package by following the instructions in the [setup](docs/setup.md) guide!

## The daily workflow package contains the following workflows in their respective subdirectories:

<br />

### **Workflow 1:** [Import demographics](docs/WF_1_import_demos.md)
 - Open HORIZON LIMS database (Oracle).
 - Join all demographics with HSN's contained in the demographics workbook.
 - Push new demographics to SARS_COV_2 MS SQL database (Table_1).

  > This step is absolutely required, since the HSN is the primary key in the database<br>
  > making it impossible to insert any other results further down the workflow.

<br />
<br />

### **Workflow 2:** [Parse Run Statistics](docs/WF_2_parse_run_data.md) (Data)
 - Ask user for run data (currently only supports CL run data, copy/paste functionality).
 - Push run data to SARS_COV_2 MS SQL database (Table 1 and Table 2).

  > *Run statistics* will be used to identify which duplicate is selected to be represented in the Results table

<br />
<br />

### **Workflow 3:** [Compile FASTA](docs/WF_3_compile_fasta.md)
 - Ask user for path to download folder (typically the FAST files folder) of files<br>that should be concatenated.
 - Concatenate fasta files, store new all_fasta file in parent folder, and save<br>pointers to each sample fasta.
 - Push the fasta pointers to both tables in the SARS_COV_2 MS SQL database.

  > At this point users should pass the fasta file to [nextclade](https://clades.nextstrain.org/) and [pangolin_lineage_analyzer](https://pangolin.cog-uk.io/). The `.tsv` download should be selected from the nextclade site, and the `.csv` download should be selected<br>
  > from the pangolin site.  Both should be stored in the parent folder for the run where the `all_fasta.fasta` file is located.

<br />
<br />

### **Workflow 4:** [Parse Nextclade data](docs/WF_4_parse_nextclade.md)
 - Extract required data from user-provided `nextclade(n).tsv` file.
 - Push the Nextclade data to both tables.

  > The name of this file does not matter, but the format must be a `.tsv` file.  
 
<br />
<br />

### **Workflow 5:** [Parse Pangolin data](docs/WF_5_parse_pangolin.md)
 - Extract required data from user-provided `results(n).csv` file.
 - Push the Pangolin data to the *results table* only.
  
  > The name of this file also does not matter, but the format must be a `.csv` file
  
<br />
<br />

### **Workflow 6:** [Build Epi Report](docs/WF_6_build_epi_report.md)
 - Ask user for search to perform
   - Potential searches currently allowed: `date `
   - Coming soon: `submitting facility, performing facility, date range`
 - Extract reportable information from the database and format to be accepted by HORIZON parser for efficient reporting of results
 - Save report to appropriate folder for easy access in the future

<br />
<br />

### **Workflow 7:** [Send Epi Report](docs/WF_7_send_epi_report.md)
 - Uses the paramiko python package to send a file to EpiTrax using sftp.

<br />
<br />

### **Workflow 8:** [Build Nextstrain Report](docs/WF_8_build_nextstrain_report.md)
 - Extract all information required from the nextstrain scripts from the database and format to be accepted by the nextstrain CLI.
 - Save report to appropriate folder for easy access in the future

<br />

All of these workflows can be run on their own, but I've provided a runner script that can call workflows 1-5, waiting on input from the user to complete the critical steps.  It is recommended to create a simple script outside of the package for even easier access to call the runner script.  For more information, see the [docs](docs/overview.md).

<br />

# Other Scripts included in this package

In addition to the standard workflows, I have included several scripts which can also be called individually from the runner and add essential functionality.

<br />

### **[EPI_ISL:](docs/epi_isl.md)**
  - User submits a simple workbook downloaded from the GISAID website, containing the sample's gisaid number (which already exists in the database) and the EPI_ISL number (which does not).
  - The sql database is updated such that all EPI_ISL numbers are matched with the appropriate gisaid numbers.

  > The file can contain samples that already have EPI_ISL numbers in the database as these numbers will not change.

<br />
<br />

### **[GISAID:](docs/gisaid.md)**
  - This script scans through the database to find samples that are eligible for upload to the GISAID database.
  - After identifying eligible samples, it compiles two files formatted for upload to GISAID: a `.xlsx` file, and a `.fasta` file.
  - The xlsx file contents must be copied into the template provided by GISAID's website (`.xls` file).  After copying, the two files may be uploaded to the database.
  - This script also updates the GISAID numbers in the sql database for easy identification in the future.

<br />
<br />

### **[Outside Lab:](docs/outside_lab.md)**
  - This script uploads data to the database.
  - The supplied template must be used in order to ensure all data is imported.

<br />
<br />

### **[Query:](docs/query.md)**
  - This script seeks to simplify queries made to the database by simplifying queries into selectable statements.
  - After querying the database, the query is saved to an excel workbook for easy data manipulation/viewing
  - DEPRECATED

<br />
<br />

### **[Refresh:](docs/refresh.md)**
  - This script completely empties the database and uploads all data contained in the user-selected excel workbook to the database.
  - DEPRECATED

<br />
<br />

The README and other documentation is a work in progress.  We will be updating regularly, so check back often! :)

