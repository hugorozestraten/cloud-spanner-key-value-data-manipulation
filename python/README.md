## Python code snipets for Cloud Spanner Key-Value modeling

In order to run this code snipets:

1. Create a Cloud Spanner instance.

2. Create a Database in your Spanner instance.
   
3. Create a Cloud Engine VM ( Virtual Machine ) in your GCP environment, in the same region of your Cloud Spanner.

5. Add the permission for your VM to create tables and perform operations on Google Cloud Spanner . 

6. Have the Cloud Spanner python library installed 
```bash
sudo apt-get install python3-pip

pip3 install google-cloud-spanner
```



## Create table and Index

### spanner_json_ddl.py

#### Usage:

python3 spanner_json_ddl.py instance_id database_id table_name "key_data_type" *(STRING(n),BYTE(n),INT64)* extra_attribute_index "extra_attribute_data_type" 

#### Example:

python3 spanner_json_ddl.py instance1 test mytable1 "string(50)" attribu2 "string(100)"

*output example*

```result
Waiting for operation to complete...
Created table mytable1 on database test - instance instance1, Index: Y
Waiting for operation to complete...
Created index Index_mytable1_attribu2 on table mytable1 on database test - instance instance1
```

Every table will be created with:
- a Key "tbkey" that can be STRING(n), BYTE(n) or INT64, the data type should be put in double quote as parameters
- a Value column of JSON data type

If extra_attribute_index and extra_attribute_data_type are given, then a column with the attribute name is created. 
After the table creation one index is created for the column created as extra_attribute_index.








