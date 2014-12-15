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





def started(found, server):

    log.msg("Found nodes: %s" % found)

    #maidSafeEncrypt(inputFile, 1024, server, iterations=1000, xor=False)

    maidSafeDecrypt(inputFile + '.hashes', 1024, server, iterations=1000, xor=False)






inputFile = sys.argv[1]


# Start Server
log.startLogging(sys.stdout)
server = Server()

# Start own server on port 5678
server.listen(5678)

# Bootstrap with a known ip address of an existing kad server
server.bootstrap([('127.0.0.1', 8468)]).addCallback(started, server)


reactor.run()
