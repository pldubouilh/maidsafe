#!/bin/bash
echo "Testing file 1024.rnd. Size 1MB"
echo "size, shasTime, pbkdfTime, aesTime, resizingTime, networkTime"

for i in `seq 1 1`;
do

  rm *.pid 2&> /dev/null

  twistd -noy kademlia/examples/server.tac &
  sleep 5

  ./bench.py -z oneKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z twoKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z forKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z noSlices -d none -s 1024.rnd
  sleep 2

  ./bench.py -z tenKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z fifKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z hunKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z twhKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z fvhKil -d none -s 1024.rnd
  sleep 2

  ./bench.py -z oneMeg -d none -s 1024.rnd
  sleep 2

  ./bench.py -z twoMeg -d none -s 1024.rnd
  sleep 2

  ./bench.py -z fivMeg -d none -s 1024.rnd
  sleep 2

  ./bench.py -z tenMeg -d none -s 1024.rnd
  sleep 2


  kill `cat twistd.pid`
  sleep 2

done
