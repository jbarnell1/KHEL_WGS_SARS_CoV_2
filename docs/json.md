# JSON Files' Functions
_______________________________________

### Contains class variables and settings for scripts to abstract most functions to the [formatter](formatter.md) package.

<br />
<br />

## How the JSON files work:


### Private cache
______

<br />

- Created on first run of the script.  Not included in the original package, to maintain privacy of data.
- The private cache contains usernames, passwords, IP addresses, control lots, expiration dates, paths to files, and database information.  Again, all of this data is stored locally on the private_cache, and will not be included in pushes to the git repository.
- The private cache can be split into two major sections:
  - **All workflows:**
    - Variables and information generally required by all workflows, so that information does not have to be repeated in every individual workflow section.
  - **Individual workflows:**
    - Variables and information generally unique to an individual workflow.
  - Each script, when run, loads in both the all_workflow dictionary and the corresponding individual workflow's dictionary

<br />

### Static cache
______

<br />

- Included in the original git repo, downloaded with clone.
- The static cache contains variable names, settings, dictionaries of abbreviations, and general query structures.  
- The private cache can be split into two major sections:
  - **All workflows:**
    - Variables and information generally required by all workflows, so that information does not have to be repeated in every individual workflow section.
      - `percent_cvg_cutoff` - This is the location to set the cutoff to include samples on reports
      - `neg_percent_cvg_cutoff` - This is the location to set the cutoff that the negative must be below to pass
      - `avg_depth_cutoff` - This is the location to set the cutoff to include samples on reports
      - `col_func_map` - This is used by the formatter and `add_cols` function to determine what functions should be applied to new columns added, including instance variables and functions.
  - **Individual workflows:**
    - Variables and information generally unique to an individual workflow.
  - Each script, when run, loads in both the all_workflow dictionary and the corresponding individual workflow's dictionary containing lists, dictionaries, queries, etc.



