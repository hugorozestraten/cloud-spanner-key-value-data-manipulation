#/bin/bash
# usage
# ./spanner_json_dml_auto.sh instance database table KeyType initial_num batch_records num_of_runs ParallelProcess ExtraAttribute DataType
# example
# ./spanner_json_dml_auto.sh test test mytable1 STRING 1810000000 300 100 40 attribu2 STRING

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
PID=

for i in $(seq 1 $parallel)
do
    echo launch $initial to $(($initial+$batch_records*$num_of_runs))
    nohup python3 spanner_json_batch_insert.py $instance $database $table $dtype $initial $batch_records $num_of_runs $attribute $attribute_type > $path/output_$initial.out 2>&1 &
    PID=$!
    PIDs="$PIDs $PID"
    initial=$(($initial+$batch_records*$num_of_runs))
done



echo "**** wait for all processes to finish ****"

#wait for all processes to finish
wait $PIDs


c=0.0
a=`cat $path/* | grep "records per second" | awk '{print $8}'`
for b in $a; do c=`awk "BEGIN{ print $b + $c}"`; done
datenow=`date '+%Y-%m-%d %H:%M:%S'`
if [ ${c%.*} -eq 0 ]
then 
    echo there was an error to insert records with the arguments check the output files in $path 
else 
    echo $datenow $path $(($batch_records * $num_of_runs * $parallel)) records $c records per second >>total.out
    tail -1 total.out
fi
