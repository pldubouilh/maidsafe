#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage : bash benchSlice.sh"
    echo "    Arg 1 : Number of tries"
    echo "    Arg 2 : File to send"
    echo "    Arg 3 : Bootstrap IP addr"
    exit
fi

echo "$1 tries on file $2. Bootstraping on $3"
echo "size, shasTime, pbkdfTime, aesTime, resizingTime, networkTime, pktLoss"

echo "$1 tries on file $2. Bootstraping on $3" > "res_$1_tries_$2_file__$3.csv"
echo "size, shasTime, pbkdfTime, aesTime, resizingTime, networkTime, pktLoss" >> "res_$1_tries_$2_file__$3.csv"

for i in `seq 1 $1`;
do

    ./bench.py -z twoMeg -i $3 -d none -s $2 >> "res_$1_tries_$2_file__$3.csv"
    sleep 1
    clear
    echo "$1 tries on file $2. Bootstraping on $3"
    echo "size, shasTime, pbkdfTime, aesTime, resizingTime, networkTime, pktLoss"
    tail "res_$1_tries_$2_file__$3.csv"

done
