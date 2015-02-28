#!/usr/bin/python
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys
import pdb
#pdb.set_trace()
import getopt
import os.path
from encrypt import maidSafeEncryptSetDebug
from decrypt import maidSafeDecryptSetDebug
import config



def started(found, server, send, file, debug):

    noSlices = 8100
    oneKil = 1024
    tenKil = 10*oneKil
    hunKil = 100*oneKil
    oneMeg = oneKil*oneKil
    twoMeg = 2*oneMeg
    fivMeg = 5*oneMeg
    eigMeg = 8*oneMeg
    tenMeg = 10*oneMeg

    cryptoChunksSize = twoMeg

    if debug == 'loads': log.msg("Found nodes: %s" % found)

    if len(found) == 0:
        print '    Bootstraping returned nothing.'
        print '    Exiting...'
        reactor.stop()
        return
        sys.exit(2)

    if send : maidSafeEncryptSetDebug(file, cryptoChunksSize, server, debug, iterations=2000, xor=False)
    else : maidSafeDecryptSetDebug(file, cryptoChunksSize, server, debug, iterations=2000, xor=False)




def helper(file, ip, bootstrapPort, localPort, send, debug):

    # No loss yet !
    config.totalLoss = 0
    config.debug = debug

    # Start Server
    if debug == 'loads': log.startLogging(sys.stdout)
    server = Server()

    # Start own server on port 5678
    server.listen(localPort)

    # Bootstrap with a known ip address of an existing kad server
    server.bootstrap([(ip, bootstrapPort)]).addCallback(started, server, send, file, debug)


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
             -l  Local port to use. Default 5678.
             -i  Bootstrap IP address. Default 127.0.0.1
             -p  Bootstrap port. Default 8468.
             -d  Print debug log. wee < normal < loads. Default wee.

    ##########################\n'''


def main():

    sayHi()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:p:s:g:l:d:h', ['i=','p=','s=','g=', 'd=','l=','help'])
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
                print '    Printing no log.'
            else:
                print '    Invalid log argument'
                sys.exit(2)

        elif opt in ('-i'):
            bootstrapIP = arg
            print '    Bootstraping on IP address ' + arg

        elif opt in ('-l'):
            localPort = int(arg)
            print '    Local port ' + arg

        elif opt in ('-p'):
            bootstrapPort = int(arg)
            print '    Bootstraping on port ' + arg

        elif opt in ('-s'):
            file = arg
            if os.path.isfile(arg) :
                print '    Sending file ' + arg
                validCommand = True
                send = True
            else:
                print '\n    Exiting, file not found\n'
                sys.exit(2)

        elif opt in ('-g'):
            file = arg
            if os.path.isfile(arg) :
                # Proper hashes file provided
                if arg.endswith('.hashes'):
                    print '    Getting file ' + arg
                    validCommand = True
                    send = False
                # No hash file provided
                else:
                    # Trying to get the hash file
                    if os.path.isfile(arg + '.hashes') :
                        file = arg + '.hashes'
                        print '    Getting file ' + arg
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

    if validCommand : helper(file, bootstrapIP, bootstrapPort, localPort, send, debug)
    else :
        print ''
        usage()
        print '\n    Exiting, a command, -s to send or -g to get, must be provided.\n'
        sys.exit(2)



main()
print ''
