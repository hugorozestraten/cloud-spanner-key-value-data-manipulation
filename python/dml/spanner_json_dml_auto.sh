#/bin/bash
# usage
# ./spanner_json_dml_auto.sh instance database table KeyType StartNumber ParallelProcess ExtraAttribute DataType RecordsPerRun
# example
# ./spanner_json_dml_auto.sh test test mytable1 STRING 600000 80 attribu2 STRING 2000


instance=$1
database=$2
table=$3
type=$4
startnum=$5
parallel=$6
attribute=$7
attribute_type=$8
records=$9


initial=$(($startnum))

#print variables working
echo instanceID: $instance
echo database: $database
echo table: $table
echo type:$type
echo startnum: $startnum
echo parallel: $parallel
echo attribute: $attribute

path=p_$parallel
mkdir $path

for i in $(seq 1 $parallel)
do
    echo launch $initial to $(($initial+999))
    nohup python3 spanner_json_line_insert.py $instance $database $table $type $initial $(($initial+$records-1)) $attribute $attribute_type > $path/output_$initial.out 2>&1 &
    initial=$(($initial+$records))
done


