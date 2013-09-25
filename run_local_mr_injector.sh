#!/bin/bash

sqlmapargs=`shift
    for i in $*; do
        echo -n $i " "
    done`


cat $1 | ./mapper.py $sqlmapargs
