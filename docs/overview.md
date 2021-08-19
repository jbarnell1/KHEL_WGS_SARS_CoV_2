
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


