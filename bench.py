#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import sys
import hashlib
import binascii
import base64
from pbkdf2 import pbkdf2_hex
from shaGeneration import *
from encrypt import *
from decrypt import *
from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys
import time
import pdb
import pickle
import getopt
import os.path





def started(found, server, send, file, debug):

    oneK = 1024
    hundredK = 100*oneK
    oneMeg = oneK*oneK
    twoMeg = 2*oneMeg


    if debug == 'loads': log.msg("Found nodes: %s" % found)

    if send : maidSafeEncryptSetDebug(file, twoMeg, server, debug, iterations=1000, xor=False)
    else : maidSafeDecryptSetDebug(file, twoMeg, server, debug, iterations=1000, xor=False)




def helper(file, ip, bootstrapPort, localPort, send, debug):

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
             -p  Bootstrap port. Default 8450.
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
    output = None
    debug = 'wee'
    bootstrapIP = '127.0.0.1'
    bootstrapPort = 8450
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
                send = True
            else:
                print '\n    Exiting, file not found\n'
                sys.exit(2)

        elif opt in ('-g'):
            file = arg
            if os.path.isfile(arg) :
                print '    Getting file ' + arg
                send = False

            else:
                print '\n    Exiting, file not found\n'
                sys.exit(2)


        else:
            usage()
            sys.exit(2)

    helper(file, bootstrapIP, bootstrapPort, localPort, send, debug)



main()
print ''
