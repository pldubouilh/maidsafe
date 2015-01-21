#!/usr/bin/python
# -*- coding: utf-8 -*-
from encryptBench import maidSafeEncryptSetDebug
from decryptBench import maidSafeDecryptSetDebug
from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys
import pdb
#pdb.set_trace()
import getopt
import os.path




def started(found, server, send, file, debug, size):

    oneK = 1024
    hundredK = 100*oneK
    fiveHundredK = 5*hundredK
    oneMeg = oneK*oneK
    twoMeg = 2*oneMeg
    fourMeg = 2*twoMeg
    fiveMeg = 5*oneMeg

    cryptoChunksSize = oneMeg

    if size == 'oneK': cryptoChunksSize = oneK
    elif size == 'hundredK': cryptoChunksSize = oneK
    elif size == 'fiveHundredK': cryptoChunksSize = fiveHundredK
    elif size == 'oneMeg': cryptoChunksSize = oneMeg
    elif size == 'twoMeg': cryptoChunksSize = twoMeg
    elif size == 'fourMeg': cryptoChunksSize = fourMeg
    elif size == 'fiveMeg': cryptoChunksSize = fiveMeg

    if debug == 'loads': log.msg("Found nodes: %s" % found)

    print (size + ','),
    if send : maidSafeEncryptSetDebug(file, cryptoChunksSize, server, debug, iterations=1000, xor=False)
    else : maidSafeDecryptSetDebug(file, cryptoChunksSize, server, debug, iterations=1000, xor=False)


def helper(file, ip, bootstrapPort, localPort, send, debug, size):

    # Start Server
    if debug == 'loads': log.startLogging(sys.stdout)
    server = Server()

    # Start own server on port 5678
    server.listen(localPort)

    # Bootstrap with a known ip address of an existing kad server
    server.bootstrap([(ip, bootstrapPort)]).addCallback(started, server, send, file, debug, size)


    reactor.run()




def sayHi():
  print ''
  print '''    ##########################
    ## Maidsafe Interpreter ##
    ##########################\n'''


def usage():
  print '''    Usage: [option] <file>

    Options: -s   Send file on network.
             -g   Get file from network. Input file must be a hash list.

    Optionnal:
             -z  Crypto chunks size. Default oneMeg.
             -l  Local port to use. Default 5678.
             -i  Bootstrap IP address. Default 127.0.0.1
             -p  Bootstrap port. Default 8468.
             -d  Print debug log. wee < normal < loads. Default wee.

    ##########################\n'''

def send(file, size):
    helper(file, size, '127.0.0.1', 8468, 5688, True, 'none')

def get(file, size):
    helper(file, size, '127.0.0.1', 8468, 5688, false, 'none')

def main():


    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:p:s:g:l:d:z:h', ['i=','p=','s=','g=', 'd=','l=','z=','help'])
    except getopt.GetoptError as err:
        usage()
        print '>>  ' + str(err) + '\n'
        sys.exit(2)

    # Default options
    validCommand = False
    debug = 'wee'
    bootstrapIP = '127.0.0.1'
    bootstrapPort = 8468
    localPort = 5678
    file = 'a'
    size = 'oneMeg'
    send = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)

        elif opt == "-d":
            if arg == 'wee':
                debug = arg
                print '    Printing a wee debug log.'
            elif arg == 'normal':
                debug = arg
                print '    Printing some debug log.'
            elif arg == 'loads':
                debug = arg
                print '    Printing _loads_ of logs. Might slow down the process.'
            elif arg == 'none':
                debug = arg
            else:
                print '    Invalid log argument'
                sys.exit(2)

        elif opt in ('-i'):
            bootstrapIP = arg

        elif opt in ('-l'):
            localPort = int(arg)

        elif opt in ('-p'):
            bootstrapPort = int(arg)

        elif opt in ('-s'):
            file = arg
            if os.path.isfile(arg) :
                validCommand = True
                send = True
            else:
                sys.exit(2)

        elif opt in "-z":
            size = arg

        elif opt in ('-g'):
            file = arg
            if os.path.isfile(arg) :
                # Proper hashes file provided
                if arg.endswith('.hashes'):
                    validCommand = True
                    send = False
                # No hash file provided
                else:
                    # Trying to get the hash file
                    if os.path.isfile(arg + '.hashes') :
                        file = arg + '.hashes'
                        validCommand = True
                        send = False

                    # Not found. Quit
                    else :
                        print '    Exiting, to get a file from the network, the input file must be .hashes\n'
                        sys.exit(2)

            else:
                print '\n    Exiting, file not found\n'
                sys.exit(2)


        else:
            usage()
            sys.exit(2)

    if validCommand : helper(file, bootstrapIP, bootstrapPort, localPort, send, debug, size)
    else :
        usage()
        print '\n    Exiting, a command, -s to send or -g to get, must be provided.\n'
        sys.exit(2)



main()
