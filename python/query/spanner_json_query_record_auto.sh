#/bin/bash
# usage
# ./spanner_json_query_record_auto.sh instance database table table_records_range initial_offset limit parallel 
# ./spanner_json_query_record_auto.sh test test mytable1 1000000 3000 1000 10

instance_id=${1}
database_id=${2}    
table_name=${3}
limit_value=${4}
offset_value=${5}
cap=${6}
parallel=${7}

echo instance_id=$instance_id
echo database_id=$database_id
echo table_name=$table_name
echo limit=$limit_value
echo offset=$offset_value
echo cap=$cap
echo parallel=$parallel


path=p_$parallel
rm -rf $path
mkdir $path

new_offset=$(($offset_value))

for i in $(seq 1 $parallel)
do
    echo launch $new_offset of $limit_value
    nohup python3 spanner_json_query_record.py $instance_id $database_id $table_name $limit_value $new_offset $cap > $path/output_$new_offset.out 2>&1 &
    new_offset=$(($new_offset+$cap))
done
