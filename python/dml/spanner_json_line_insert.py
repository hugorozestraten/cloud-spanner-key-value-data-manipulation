# Sample code to create Key-Value table in Cloud Spanner
# Created by Hugo Rozestraten
# Google Cloud Consulting - PSO 

# import spanner library, datetime to control execution time and sys to read arguments

from google.cloud import spanner
import random
import datetime
import sys
import math
import json

# import Cloud Spanner Json Object type
from google.cloud.spanner_v1.data_types import JsonObject

assertion_error="Argument 1 error. Use arguments: instance_id database_id table_name key_data_type inicial_num end_num extra_attribute(optional) attribute_data_type(optional)"

# check for arguments"
assert len(sys.argv) >= 6,assertion_error

assert isinstance(sys.argv[1], str),assertion_error
assert isinstance(sys.argv[2], str),assertion_error
assert isinstance(sys.argv[3], str),assertion_error
assert isinstance(sys.argv[4], str),assertion_error
assert sys.argv[4] in ['STRING', 'INT64'],assertion_error
assert isinstance(int(sys.argv[5]), int),assertion_error
assert isinstance(int(sys.argv[6]), int),assertion_error

# get arguments from command line
instance_id=sys.argv[1]
database_id=sys.argv[2]
table_name = sys.argv[3]
key_type = sys.argv[4]
inicial_num=int(sys.argv[5])
end_num=int(sys.argv[6])
sum=end_num-inicial_num+1
sql_statements=[]
num=0
sql=''


# check for extra attribute to create index
if len(sys.argv) >= 8:
    index='Y'
    assert isinstance(sys.argv[7], str),assertion_error
    assert isinstance(sys.argv[8], str),assertion_error
    extra_attribute = sys.argv[7]
    attribute_data_type = sys.argv[8].upper()
    assert attribute_data_type in ['STRING', 'INT64'],assertion_error
else:
    index='N'
    extra_attribute=''
    attribute_data_type=''



# create connection with Cloud Spanner
spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# create a SQL statement to insert a Key-Value in a table
def get_sql(x):
    if index == 'Y':
        extra_attribute_definition=extra_attribute+', '
        if attribute_data_type == 'STRING':
            extra_attribute_value=random.choice(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'])
            extra_attribute_value=f"\"{extra_attribute_value}\", "
        else:
            extra_attribute_value=str(random.randint(1,10000))+', '
    else:
        extra_attribute_definition=''
        extra_attribute_value=''
    b=random.choice(['one', 'two', 'three', 'four', 'five'])
    l={
                            "items": None,
                            "classification": b,
                            "open": {"Monday": True, "Tuesday": False},
                            "tags": ["large", "airy"],
                        }
    m=json.dumps(l)
    if key_type == 'STRING':
        k='\"'+b+str(x)+'\"'
    else:
        k=x
    sqlgen=f"""
    INSERT INTO
        {table_name} (tbkey, {extra_attribute_definition}
        Value)
        VALUES
        ({k}, {extra_attribute_value}
        PARSE_JSON(\'{m}\')
        );
        """
    return sqlgen

# insert a Key-Value in a table

def insert_venues(transaction):
    row_ct=transaction.execute_update(sql)


if __name__ == "__main__":
    inicial=datetime.datetime.now()
    for a in range(inicial_num,end_num+1):
        sql=get_sql(a)
        #print(sql)
        database.run_in_transaction(insert_venues)
        num=num+1
        #if math.fmod(a,1000)==0:
        #    print(f'rows inserted: {num}')


    final=datetime.datetime.now()
    delta=final-inicial
    rps=sum/delta.seconds
    print(f'rows inserted: {sum} in {delta.seconds} seconds at {rps} records per second')
