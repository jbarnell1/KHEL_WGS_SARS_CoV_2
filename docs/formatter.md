
# Formatter Functions
_______________________________________

### Abstracts common functions for scripts to maintain readability and brevity

<br />
<br />

## How the Formatter package works:


### Functions
______

<br />

- **remove_blanks()**
  - Remove any rows from the dataframe in which `df[col_name]` contains 'Blank\d*.*'

<br />

- **remove_pools(df, col_name)**
  - Remove any rows from the dataframe in which `df[col_name]` contains 'pool' or 'panel'

<br />

- **merge_dataframes(df1, df2, df1_drop, df_final_drop, join_lst, join_type)**
  - Merges Pandas dataframes provided, first removing supplied columns from df1, join on join_lst, and specify join type as described in the [pandas.DataFrame.merge()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) method

<br />

- **format_hsn_col(df, hsn_colname, hsn_only)**
  - Takes hsn column of provided DataFrame
    - Convert samples to 7-digit HSN values
    - Convert HSN to string type
    - Removes pooled samples
    - Removes duplicate values
    - Removes blank samples

<br />

- **add_cols(obj, df, col_lst, col_func_map)**
  - `obj` - Workflow Object, so that the function can access the workflow object's instance variables
  - `df` - Dataframe onto which to add columns
  - `col_lst` - list of columns that should be added to DataFrame
  - `col_func_map` - as listed in `static_cache.json`, dictionary name `col_func_map`
    - Key of dictionary is column name
    - Value 1: Either function name or obj.value
    - Value 2: obj.value (if exists)
  - If column does not exist in col_func_map, add empty column
  - Returns DataFrame with inserted columns.

<br />

- **format_date(row, *colName*)**
  - Return provided date at `row[colName]` formatted as MM-DD-YYYY
  - If not correct format (pandas.Timestamp or datetime.datetime), return numpy NaN

<br />

- **get_today()**
  - Return today's date formatted as 'YYYY-MM-DD'

<br />

- **parse_seq_id(row, *arg*)**
  - Assumes `row` has either `Sequence name` or `seqName`
  - Returns parsed value based on arg: can determine:
    - hsn: Sample ID
    - m_num: ClearLabs Machine number
    - pos: Position of sample on plate
    - run_num: Run number of day (typically 1)
    - date: Date of run

<br />

- **extracted_hsn(row)**
  - Assumes `row` has `Sample ID` column
  - Truncates HSNs to 7 digits.  Useful for importing old HSNs with format '\d{7}.\w'
  - Standardizes all HSNs to length 7

<br />

- **format_str_cols(df)**
  - Convert all columns in provided dataframes to a string type.

<br />

- **format_sex(row, *ber*)**
  - `ber`: boolean value, helps to determine what column should be used for analyzing sex formatting
  - Convert abbreviations and mis-capped values to standardize `sex` column to either "Male", "Female", or "Unknown"

<br />

- **format_facility(row, *facility_replace_dict*)**
  - Assumes `row` has column `facility`
  - If `row[facility]` is null or empty string, return `None`
  - Returns facility name with appropriate abbreviations to standardize `facility` column in SQL database

<br />

- **parse_category(row, *parse_category_dict*)**
  - Assumes `row` has `facility` column
  - Look for common trends in `row['facility']`, and try to identify facility type.
  - See `static_cache.json` dictionary `parse_category_dict`

<br />

- **format_race(row)**
  - Assumes `row` has `race` column
  - Convert unknown values, empty strings, and abbreviations to non-abbreviated race values

<br />

- **format_source(row)**
  - Assumes `row` has `source` column
  - Convert full listed source to the appropriate abbreviation.
  - Currently only works for nasopharyngeal and sputum/saliva

<br />

- **add_cols_by_name(df, *lst*)**
  - Add columns to the provided DataFrame based on the values in *lst*
  - All columns aded will be placed at the beginning of the Dataframe and the value will default to numpy's NaN

<br />

- **format_f_name(row)**
  - Assumes `row` has column `name`
  - If `row[name]` is null or empty string, return `None`
  - Returns first name of `row[name]`

<br />

- **format_l_name(row)**
  - Assumes `row` has column `name`
  - If `row[name]` is null or empty string, return `None`
  - Returns last name of `row[name]`, including suffixes like Jr., Sr., etc.

<br />

- **drop_cols(df, *lst*)**
  - Return df with all columns in *lst* removed

<br />

- **get_age(row)**
  - Assumes provided `row` has both `doc` (date of collection) and `dob` (date of birth) columns
  - Returns calculated age at date of collection

<br />

- **format_state(row, *state_abbrev*)**
  - Assumes provided `row` has a `state` column.
  - *state_abbrev* (dictionary), maps states to their abbreviations
  - Returns the abbreviated state value if the state name is not null, otherwise return 'unknown'

<br />

- **parse_path(row, *path*)**
  - Assumes provided `row` has a `seqName` column.
  - Returns `path` concatenated with `row['seqName']`

<br />

- **get_gisaid(row)**
  - Convert gisaid_num (int) from database to the full string submitted to GISAID

<br />

- **get_name(row)**
  - Assumes provided `row` has a `f_name` and `l_name` columns
  - Returns `row['f_name']` and `row['l_name']` joined with a single space

<br />

- **unkwn(row, *col*)**
  - If `row[col]` is numpy NaN, return an empty string, otherwise return `row[col]`

<br />

- **cap_all(row, *col*)**
  - Take full string from `row[col]` and capitalize each word, then return string.

<br />

- **get_priority(row, *lst*)**
  - Return 1 if row[`hsn`] in *lst*




