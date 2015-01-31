#!/bin/bash
echo "Testing file wind.mp3. Size 15MB"
echo "size, shasTime, pbkdfTime, aesTime, resizingTime, networkTime"

for i in `seq 1 1`;
do

  rm *.pid 2&> /dev/null

  twistd -noy kademlia/examples/server.tac &
  sleep 5

  ./bench.py -z noSlices -d none -s wind.mp3
  sleep 2

  ./bench.py -z fifKil -d none -s wind.mp3
  sleep 2

  ./bench.py -z hunKil -d none -s wind.mp3
  sleep 2

  ./bench.py -z fvhKil -d none -s wind.mp3
  sleep 2

  ./bench.py -z oneMeg -d none -s wind.mp3
  sleep 2

  ./bench.py -z twoMeg -d none -s wind.mp3
  sleep 2

  ./bench.py -z fivMeg -d none -s wind.mp3
  sleep 2

  ./bench.py -z eigMeg -d none -s wind.mp3
  sleep 2

  ./bench.py -z tenMeg -d none -s wind.mp3
  sleep 2

  ./bench.py -z fifMeg -d none -s wind.mp3
  sleep 2

  ./bench.py -z tweMeg -d none -s wind.mp3
  sleep 2


  kill `cat twistd.pid`
  sleep 2

done
