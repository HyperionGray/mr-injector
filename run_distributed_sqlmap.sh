#!/bin/bash

date=`date +%s`

outfile=${date}-distributed-output

hadoop dfs -rmr sites_to_inject.txt

hadoop dfs -copyFromLocal sqlmap.tar.gz sqlmap.tar.gz

hadoop dfs -copyFromLocal sites_to_inject.txt sites_to_inject.txt

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/*streaming*.jar -archives hdfs://punkscan-master:54310/user/pgotsr/sqlmap.tar.gz#sqlmaparch -input sites_to_inject.txt\
 -mapper mapper.py -output ${outfile} -file sites_to_inject.txt -file mapper.py

hadoop dfs -copyToLocal $outfile $outfile
