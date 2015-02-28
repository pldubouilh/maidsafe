#!/bin/bash
if [ "$#" -ne 3 ]; then
    echo "Usage : bash benchServ.sh"
    echo "    Args : delay between server restart"
    exit
fi

for i in `seq 1 99999999`;
do

  rm *.pid 2&> /dev/null

  twistd -noy kademlia/examples/server.tac &

  sleep $1

  kill `cat twistd.pid`
  sleep 20

done
