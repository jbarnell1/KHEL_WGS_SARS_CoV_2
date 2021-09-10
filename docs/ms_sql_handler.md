
# MS_SQL_Handler Class
_______________________________________

### Abstracts common functions for scripts to maintain readability and brevity

<br />
<br />

## How the MS_SQL_Handler class works:

### Variables
______

<br />

- Created from class Function:
  - **engine**
- Pulled in from `private_cache.json` and `static_cache.json`
  - **sql_user**
  - **sql_pass**
  - **sql_server**
  - **sql_db**
  - **avg_depth_cutoff**
  - **percent_cvg_cutoff**

<br />

### Functions
______

<br />

- **establish_db()**
  - Attempt to create [SQLAlchemy engine](https://docs.sqlalchemy.org/en/14/core/engines.html) using the private data (username, password, server, table name) from `private_cache.json` and store in the `self.engine` variable

<br />

- **clear_db()**
  - Using the engine established above, execute complete `DELETE`s from both tables (`Results` and `Run_Stats`)

<br />

- **ss_read()**
  - Using the engine established above and the [Pandas.read_sql()](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) function, read information from the database.
  - The query used will be pulled from the `static_cache.json` file.

<br />

- **sub_read()**
  - Same logic as above, but substitutes `avg_depth_cutoff` and `percent_cvg_cutoff` for their respective values from the `static_cache.json` file

<br />

- **sub_lst_read()**
  - Same logic as `ss_read()` but substitutes `hsn_query` with a list of hsn's supplied to the function, and surrounded by parentheses

<br />

- **to_sql_push()**
  - Using the engine established above and the [Pandas.DataFrame.to_sql()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) function, read information from the database.
  - The query used will be pulled from the `static_cache.json` file.

<br />

- **lst_push()**
  - Same logic as above, but substitutes `df_cols` and `df_lst_query` with their corresponding values in a DataFrame
    - df_lst_query is done by calling `DataFrame.values.astype(str).tolist()`

<br />

- **lst_ptr_push()**
  - Same logic as above, but sbustitutes values according to a list/pointer strategy
  - Parameters:
    - **df_lst**      - Required  : nested list that holds values to fill ([[x],[y]])
    - **query**       - Required  : stored in cache, generic string with placeholders (Str)
    - **full**        - Optional  : True if full dataframe being pushed. For use with refresh or ouside_lab scripts (Bool)
    - **df**          - Optional  : dataframe of values to clean. For use with refresh or outside_lab (Pandas DataFrame)
  - Iterates through every nested list, creating a unique and specific query each time, and finally executing the query to push data to the database.