Maidsafe-like network in python
=======


    ##########################
    ## Maidsafe Interpreter ##
    ##########################

    Usage: [option] <file>

    Options: -s   Send file on network.
             -g   Get file from network. Input file must be a hash list.

    Optionnal:
             -l  Local port to use. Default 5678.
             -i  Bootstrap IP address. Default 127.0.0.1
             -p  Bootstrap port. Default 8468.
             -d  Print debug log. wee < normal < loads. Default wee.

    ##########################

<br />
### Introduction
[Maidsafe](http://maidsafe.net/)-like network implemented in python. The initial algorithm has been slightly modified to increase performance. It is described in the following schematic.

<br />
![process](process.png "Title here")
<br />

<br />
### How to start an instance

1. Clone repo : `git clone https://github.com/pldubouilh/maidsafe.git && cd maidsafe`
2. Install modified Kademlia and other deps : `(sudo) pip install twisted pycrypto config && pip install -e rpcudp-master/ kademlia/`
3. Create necessary directories `mkdir reconstructed scrambled dht`
4. Start backbone kad server : `twistd -noy kademlia/examples/server.tac`
5. Open a new terminal
6. Send file : `./main.py -s yourfile.png`
7. Get file  : `./main.py -g yourfile.png.hashes`

The reconstructed file will be in reconstructed/. scrambled/ is the (necessary) local temp file. It should clean itself after use. The dht folder is the storage folder of Kademlia.
Some extra options are available (see help). Note that the verbose option is, well, _very_ verbose.

The code is awfully hacky. Sorry about that.

<!--- Fancy call graph : `pycallgraph --max-depth 5 graphviz -- ./main.py -s wind.mp3` -->

<br />

    joe@joe:~/Desktop/maidsafe$ ./main.py -l 5678 -i 127.0.0.1 -p 8468 -d wee -s wind.mp3

      ##########################
      ## Maidsafe Interpreter ##
      ##########################

      Local port 5678
      Bootstraping on IP address 127.0.0.1
      Bootstraping on port 8468
      Printing a wee debug log.
      Sending file wind.mp3
      Computing Shas...
      Cipherin'
      Splitting chunks in smaller slices.
      Resizing Factor >> 521
      Sending slices on network

      File sent on network !
      Note that if you delete your .hashes file and your initial file, it will be forever lost in the cyphernetic ether...

    joe@joe:~/Desktop/maidsafe$ ./main.py -l 5678 -i 127.0.0.1 -p 8468 -d wee -g wind.mp3.hashes

      ##########################
      ## Maidsafe Interpreter ##
      ##########################

      Local port 5678
      Bootstraping on IP address 127.0.0.1
      Bootstraping on port 8468
      Printing a wee debug log.
      Getting file wind.mp3.hashes
      Downloading chunks from DHT...
      Chunks downloaded from DHT!
      Decrypting...

      File successfully downloaded ! It should be in reconstructed/

    joe@joe:~/Desktop/maidsafe$ shasum wind.mp3 reconstructed/wind.mp3
    832dc53acc3687a46f4070aa5af93dffa744d7f4  wind.mp3
    832dc53acc3687a46f4070aa5af93dffa744d7f4  reconstructed/wind.mp3
    joe@joe:~/Desktop/maidsafe$

4th year project - University of Strathclyde
