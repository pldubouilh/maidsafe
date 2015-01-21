#!/bin/bash
echo "size, shasTime, cipherTime, resizingTime, networkTime"

for i in `seq 1 50`;
do
#  ./bench.py -z hundredK -d none -s wind.mp3
#  sleep 3

  ./bench.py -z fiveHundredK -d none -s wind.mp3
  sleep 3

  ./bench.py -z oneMeg -d none -s wind.mp3
  sleep 3

  ./bench.py -z twoMeg -d none -s wind.mp3
  sleep 3

  ./bench.py -z fourMeg -d none -s wind.mp3
  sleep 3

  ./bench.py -z fourMeg -d none -s wind.mp3
  sleep 3
done
