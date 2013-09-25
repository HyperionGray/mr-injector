#!/bin/bash

date=`date +%s`

#meh, just a little hacky
sqlmapargs=`shift
shift
for i in $*; do
    echo -n $i " "
done`

sites_to_inject_file=$1
outfile=$2

hadoop dfs -rmr $sites_to_inject_file
hadoop dfs -copyFromLocal sqlmap.tar.gz sqlmap.tar.gz
hadoop dfs -copyFromLocal $sites_to_inject_file $sites_to_inject_file

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/*streaming*.jar -archives\
 hdfs://punkscan-master:54310/user/pgotsr/sqlmap.tar.gz#sqlmaparch -input ${sites_to_inject_file}\
 -mapper "mapper.py ${sqlmapargs}" -output ${outfile} -file $sites_to_inject_file -file mapper.py

hadoop dfs -copyToLocal $outfile $outfile
