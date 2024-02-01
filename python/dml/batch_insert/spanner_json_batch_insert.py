from google.cloud import spanner
import random
import datetime
from google.cloud.spanner_v1.data_types import JsonObject
import sys

sufix=sys.argv[1]

assertion_error="Argument 1 error. Use arguments: instance_id database_id table_name key_data_type initial_num num_of_records num_of_runs extra_attribute(optional) attribute_data_type(optional)"

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
num_of_records=int(sys.argv[6])
num_of_runs=int(sys.argv[7])

# create spanner client
spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# check for extra attribute to create index
if len(sys.argv) >= 9:
    index='Y'
    assert isinstance(sys.argv[8], str),assertion_error
    assert isinstance(sys.argv[9], str),assertion_error
    extra_attribute = sys.argv[8]
    attribute_data_type = sys.argv[9].upper()
    assert attribute_data_type in ['STRING', 'INT64'],assertion_error
else:
    index='N'
    extra_attribute=''
    attribute_data_type=''



# get batch sql values
def get_batch_sql(x,positional_number):
    batch_sql_values=[]
    for a in range(x):
        b=random.choice(['one', 'two', 'three', 'four', 'five'])
        c=random.choice(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'])
        d=str(random.randint(1,1000000000))
        k=d+c+str(a+positional_number)
        if index == 'Y':
            #extra_attribute_definition=extra_attribute+', '
            if attribute_data_type == 'STRING':
                extra_attribute_value=random.choice(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'])
                extra_attribute_value=f"\"{extra_attribute_value}\", "
            else:
                extra_attribute_value=str(random.randint(1,10000))+', '
        else:
            #extra_attribute_definition=''
            extra_attribute_value=''
        record=(k, 
                    JsonObject(
                        {
                            "items": None,
                            "classification": b,
                            "open": {"Monday": True, "Tuesday": False},
                            "tags": ["large", "airy"],
                        }
                    ),
                    extra_attribute_value
                )
        batch_sql_values.append(record)
    return batch_sql_values


sum=0
position=inicial_num
inicial=datetime.datetime.now()
for n in range(num_of_runs):  
    with database.batch() as batch:
        if index=='Y':
            batch.insert(
                table=table_name,
                columns=("tbkey", "Value",extra_attribute),
                values=get_batch_sql(num_of_records,position)
            ) 
        else:    
            batch.insert(
                table=table_name,
                columns=("tbkey", "Value"),
                values=get_batch_sql(num_of_records,position)
            )   
        sum+=num_of_records
        position+=num_of_records


final=datetime.datetime.now()
delta=final-inicial
if delta.seconds==0:
    diff=1
else:
    diff=delta.seconds
rps=sum/diff
print(f'rows inserted: {sum} in {diff} seconds at {rps} records per second')


