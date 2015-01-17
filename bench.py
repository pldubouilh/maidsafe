#!/usr/bin/python
# -*- coding: utf-8 -*-

from encrypt import *
from decrypt import *
from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys
import pdb
#pdb.set_trace()
import getopt
import os.path
import timeit





def started(found, size, server, send, file, debug):

    oneK = 1024
    hundredK = 100*oneK
    fiveHundredK = 5*hundredK
    oneMeg = oneK*oneK
    twoMeg = 2*oneMeg
    fourMeg = 2*twoMeg
    fiveMeg = 5*oneMeg

    if size == 'hundredK': cryptoChunksSize = hundredK
    elif size == 'fiveHundredK': cryptoChunksSize = fiveHundredK
    elif size == 'oneMeg': cryptoChunksSize = oneMeg
    elif size == 'twoMeg': cryptoChunksSize = twoMeg
    elif size == 'fourMeg': cryptoChunksSize = fourMeg


    if debug == 'loads': log.msg("Found nodes: %s" % found)

    if send : maidSafeEncryptSetDebug(file, cryptoChunksSize, server, debug, iterations=1000, xor=False)
    else : maidSafeDecryptSetDebug(file, cryptoChunksSize, server, debug, iterations=1000, xor=False)




def helper(file, size, ip, bootstrapPort, localPort, send, debug):

    # Start Server
    if debug == 'loads': log.startLogging(sys.stdout)
    server = Server()

    # Start own server on port 5678
    server.listen(localPort)

    # Bootstrap with a known ip address of an existing kad server
    server.bootstrap([(ip, bootstrapPort)]).addCallback(started, size, server, send, file, debug)


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


def send(file, size):
    helper(file, size, '127.0.0.1', 8450, 5688, True, 'none')

def get(file, size):
    helper(file, size, '127.0.0.1', 8450, 5688, false, 'none')
