#/bin/bash
# usage
# ./spanner_json_dml_auto.sh instance database table KeyType StartNumber ParallelProcess RecordsPerRun ExtraAttribute DataType 
# example
# ./spanner_json_dml_auto.sh test test mytable1 STRING 600000 80 2000 attribu2 STRING 


instance=$1
database=$2
table=$3
type=$4
startnum=$5
parallel=$6
records=$7
attribute=$8
attribute_type=$9

#set initial number
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
rm -rf $path/*
PIDs=

#launch parallel processes
for i in $(seq 1 $parallel)
do
    echo launch $initial to $(($initial+999))
    nohup python3 spanner_json_line_insert.py $instance $database $table $type $initial $(($initial+$records-1)) $attribute $attribute_type > $path/output_$initial.out 2>&1 &
    PID=$!
    PIDs="$PIDs $PID"
    initial=$(($initial+$records))
done

wait $PIDs


c=0.0
a=`cat $path/* | grep "records per second" | awk '{print $8}'`
for b in $a; do c=`awk "BEGIN{ print $b + $c}"`; done
datenow=`date '+%Y-%m-%d %H:%M:%S'`
echo $path $datenow $initial_records $c records per second >>total.out
