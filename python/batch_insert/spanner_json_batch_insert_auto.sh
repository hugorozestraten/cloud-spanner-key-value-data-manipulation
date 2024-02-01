#/bin/bash
# usage
# ./spanner_json_batch_insert_auto.sh instance database table KeyType initial_num batch_records num_of_runs ParallelProcess ExtraAttribute DataType
# example
# ./spanner_json_batch_insert_auto.sh test test mytable1 STRING 1810000000 300 100 40 attribu2 STRING

instance=$1
database=$2
table=$3
dtype=$4
initial=$5
batch_records=$6
num_of_runs=$7
parallel=$8
attribute=$9
attribute_type=${10}

path=p_$parallel
rm -rf $path
mkdir $path

for i in $(seq 1 $parallel)
do
    echo launch $initial to $(($initial+$batch_records*$num_of_runs))
    nohup python3 spanner_json_batch_insert.py $instance $database $table $dtype $initial $batch_records $num_of_runs $attribute $attribute_type > $path/output_$initial.out 2>&1 &
    initial=$(($initial+$batch_records*$num_of_runs))
done
