# Sample code to create Key-Value table in Cloud Spanner
# Created by Hugo Rozestraten
# Google Cloud Consulting - PSO 

# Use arguments: instance_id database_id table_name key_data_type extra_attribute attribute_data_type"

# Example:
# python3 spanner_json_ddl.py instance1 dbtest1 mytable1 "string(50)" attribu2 "string(100)"

#import spanner library, datetime to control execution time and sys to read arguments
from google.cloud import spanner
import datetime
import sys

# check for correct number of arguments
assertion_error="Argument 1 error. Use arguments: instance_id database_id table_name key_data_type extra_attribute attribute_data_type"
assert len(sys.argv) >= 5,assertion_error

assert isinstance(sys.argv[1], str),assertion_error
assert isinstance(sys.argv[2], str),assertion_error
assert isinstance(sys.argv[3], str),assertion_error
assert isinstance(sys.argv[4], str),assertion_error

# get arguments from command line
instance_id=sys.argv[1]
database_id=sys.argv[2]
table_name = sys.argv[3]
key_type = sys.argv[4]

# Instantiate a client.
spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# check for extra attribute to create index
if len(sys.argv) >= 6:
    create_index='Y'
    assert isinstance(sys.argv[5], str),assertion_error
    assert isinstance(sys.argv[6], str),assertion_error
    extra_attribute = sys.argv[5]
    attribute_data_type = sys.argv[6]
    index_name='Index_'+table_name+'_'+extra_attribute
    index_attribute=extra_attribute+' '+attribute_data_type+','
else:
    create_index='N'
    index_attribute=''


# create table in Cloud Spanner Database
def create_table_function(table_name,key_type,index_attribute):   # use key_type S for String(100),  I for INT64 and B for BYTE(16)
    key=f'tbkey {key_type}'
    SQL=f'''
        CREATE TABLE IF NOT EXISTS {table_name}
         ( {key} NOT NULL,
            {index_attribute}
            Value JSON,
            )
        PRIMARY KEY
        (tbkey)
    '''
    print(SQL)
    return SQL

# create index in Cloud Spanner Database
def create_index_function(table_name,index_name,extra_attribute):  
    SQL=f'''
        CREATE INDEX {index_name} ON {table_name}({extra_attribute})
    '''
    return SQL

def create_index_operation(table_name,index_name,extra_attribute): 
    # create index in Cloud Spanner Database for extra attribute    
    operation = database.update_ddl([
            create_index_function(table_name,index_name,extra_attribute)])
    print('Waiting for operation to complete...')
    operation.result()
    print('Created index {} on table {} on database {} - instance {}'.format(
        index_name, table_name, database_id, instance_id))

def create_table(table_name,key_type,index_attribute,create_index):
    # create table in Cloud Spanner Database
    operation = database.update_ddl([
        create_table_function(table_name,key_type,index_attribute)])
    print('Waiting for operation to complete...')
    operation.result()
    print('Created table {} on database {} - instance {}, Index: {}'.format(
        table_name, database_id, instance_id,create_index))
    # create index only if extra_attribute is given
    # create index in Cloud Spanner Database for extra attribute    
    if create_index == 'Y':
        create_index_operation(table_name,index_name,extra_attribute)
        

if __name__ == "__main__":
    create_table(table_name,key_type,index_attribute,create_index)
   
