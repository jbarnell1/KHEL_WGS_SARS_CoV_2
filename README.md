
# Daily Workflow
_______________________________________

### The daily workflow package contains the following workflows in their respective subdirectories:
 - **Workflow 1:** Import demographics
   - Open HORIZON LIMS database (Oracle).
   - Join all demographics with HSN's contained in the demographics workbook.
   - Push new demographics to SARS_COV_2 MS SQL database (Table_1).

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

All of these workflows can be run on their own, but I've provided a runner script that can call each one, waiting for the user
to complete the critical steps.  For more information on each workflow, see the [docs](docs/overview.md).

This README is a work in progress.  We will be updating regularly, so check back often! :)

