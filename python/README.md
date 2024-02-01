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

#### Table Example

![Alt text](../images/table1.jpg?raw=true "mytable1")


## DML / Insert records

### spanner_json_line_insert.py / spanner_json_dml_auto.sh

You can run Python code directly or call it for Parallel Execution with the ShellScript


#### Python Usage ( single process ):


python3 spanner_json_line_insert.py instance_id database_id table_name key_data_type inicial_num end_num extra_attribute(optional) attribute_data_type(optional)

( This will generate random data into Spanner table_name )

If Table Key is a STRING the key will be composed by a random String value + the inicial_num(Sequence) to the number of records

If Table Key is a INT64 the key will be the exactly inicial_num(Sequence) to the number of records



#### ShellScript automation ( parallel processing ):

#### Usage:
 ./spanner_json_dml_auto.sh instance database table KeyType StartNumber ParallelProcess RecordsPerRun ExtraAttribute(Optional) ExtraAttributeDataType(Optional)


### Example:
```console
 ./spanner_json_dml_auto.sh test test mytable1 STRING 600000 80 2000 attribu2 STRING 
```

( This will generate random data into Spanner table_name )

In the example will start with number 600000 for key (if STRING a random string will be put as a prefix ) 
80 Parallel processes will be triggered

**You should increase the StartNumber for each run to avoid attempt to insert the same row twice**


An index random value type STRING will be generate, in this case the table need to have the exact attribu2 STRING - created before
I

If Table Key is a STRING the key will be composed by a random String value + the inicial_num(Sequence) to the number of records

If Table Key is a INT64 the key will be the exactly inicial_num(Sequence) to the number of records

### In another terminal console, check python parallel execution
```console
top
```
![Alt text](../images/top_example.jpg?raw=true "cat p_80")



### Retrieve results

 Check the total.out file to see all executions results

```console
cat total.out
```
```results
p_60 2024-02-01 17:17:25 120000 records inserted 1341.82 records per second
p_20 2024-02-01 17:24:21 20000 records inserted 664.461 records per second
p_50 2024-02-01 17:36:22 50000 records inserted 1179.91 records per second
p_80 2024-02-01 18:01:52 160000 records inserted 658.395 records per second
p_30 2024-02-01 18:03:49 60000 records inserted 890.926 records per second
p_40 2024-02-01 18:05:31 80000 records inserted 1111.81 records per second
```


 For each execution, the detailed results will be in the directory p_(Parallel#)
 $cat p_80/*

```console
cat p_80/*
```
![Alt text](../images/p_80_dml_insert_cat.jpg?raw=true "cat p_80")



# Batch Insert records

### spanner_json_batch_insert.py / spanner_json_batch_insert_auto.sh

You can run Python code directly or call it for Parallel Execution with the ShellScript


#### Python Usage ( single process ):


python3 spanner_json_batch_insert.py instance_id database_id table_name key_data_type initial_num num_of_records num_of_runs extra_attribute(optional) attribute_data_type(optional)


*initial_num* = is the number to use as reference for the key and will be increase in sequence + a random Prefix in case of STRING data type

*num_of_records* = number of records for EACH BATCH

*num_of_runs* = number of executions of subsequent Batches



Although the key is composite in the case of STRING data type.
**You should increase the initial_num for each run, for more than last number inserted, to avoid attempt to insert the same row twice**


#### Batch Insert ShellScript automation ( parallel processing ):

#### Usage:
 ./spanner_json_batch_insert_auto.sh instance database table KeyType initial_num batch_records num_of_runs ParallelProcess ExtraAttribute DataType


#### Retrieve results

 Check the total.out file to see all executions results
```total.out
2024-02-01 17:29:30 p_40 1200000 records 66450.1 records per second
2024-02-01 17:30:02 p_30 900000 records 65770.1 records per second
2024-02-01 17:30:37 p_30 900000 records 69423.3 records per second
2024-02-01 17:34:11 p_40 1200000 records 57857.8 records per second
2024-02-01 18:08:54 p_40 1200000 records 55714.1 records per second
2024-02-01 18:10:52 p_40 1200000 records 53714.1 records per second
2024-02-01 18:12:38 p_50 1500000 records 34443.4 records per second
2024-02-01 18:13:41 p_50 1500000 records 51352.7 records per second
```





