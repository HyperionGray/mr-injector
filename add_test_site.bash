#!/bin/bash

for i in {6..101}
do
    echo "http://sqlixxx.hyperiongray.com/?user=root" | sed "s/xxx/${i}/g"
done
