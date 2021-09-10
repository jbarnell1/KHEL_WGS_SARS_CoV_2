
# Workflow_Obj Class
_______________________________________

### Abstracts class which describes common functions for all workflow objects

<br />
<br />

## How the Workflow_Obj class works:

### Functions
______

<br />

- **get_json()**
  - Loads all relevant lists, values, and dictionaries specific to a workflow's base class as class variables from both `private_cache.json` and `static_cache.json`
  - If expected variables can't be found, the `get_json()` function will prompt the user for the workflow's required values.
  - Finally, the variables will be stored for future use in the appropriate `.json` file

<br />

- **setup_db()**
  - Create [ms_sql_handler](ms_sql_handler.md) object and save as class variable
  - Call `establish_db()` on object to setup connection

<br />

- **setup_ssh()**
  - Create [ssh_handler](ssh_handler.md) object and save as class variable
  - Call `establish_client_ssh()` on object to setup connection

