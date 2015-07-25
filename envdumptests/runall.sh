#!/bin/bash -eu

i=0
while [[ "$i" -lt "6000" ]]
do 
    ./a.out & 
    i=$(($i+1))
done

for job in $(jobs -p)
do
    wait $job
done
