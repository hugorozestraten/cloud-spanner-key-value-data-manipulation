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


instance_id = sys.argv[1]
database_id = sys.argv[2]     
table_name = sys.argv[3]
limit = int(sys.argv[4])
offset = int(sys.argv[5])
cap = int(sys.argv[6])

# Instantiates a client
spanner_client = spanner.Client()

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# list sample keys from the table based on the Limit and Offset setup ( capped to cap parameter )
def list_keys(offset, limit):
    """Queries sample data from the database using SQL."""

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"select tbkey from (SELECT tbkey FROM {table_name} limit {limit} offset {offset}) limit {cap}"
        )

    return results

# query single key 
def query_key(key):
    """Queries sample data from the database using SQL."""

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"SELECT * FROM {table_name} where tbkey = '{key}'"
        )

    return results


if __name__ == "__main__":
    sum=0
    # get the list of keys to query
    keys = list_keys(offset, limit)
    # start measuring Query time
    initial=datetime.datetime.now()
    # query each key
    for key in keys:
        query_key(key)
        sum+=1
    final=datetime.datetime.now()
    delta=final-initial
    if delta.seconds==0:
        diff=1
    else:
        diff=delta.seconds
    rps=sum/diff
    print(f'rows reads: {sum} in {diff} seconds at {rps} records per second')
