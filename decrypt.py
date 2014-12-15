from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import sys
import hashlib
import binascii
import base64
from pbkdf2 import pbkdf2_hex
from shaGeneration import *
from tools import *
import pdb
import pickle
import time

from twisted.internet import reactor, task
from twisted.python import log
from kademlia.network import Server



def grepChunks(result, i, server, encrypedHashes, inputHash, chunkSize):

  # Write result from previous query
  fn1 = encrypedHashes[i]
  fc = open(('scrambled/' + fn1), 'wb')
  fc.write(result.decode('hex'))
  fc.close()

  # Increment for next query
  i += 1

  # Got all the chunks, return bach to decryption scheme
  if i == len(encrypedHashes) :
    reactor.stop()
    maidSafeDecrypt(inputHash, chunkSize, server, grepNotDone=False)
    return

  # Get the next chunk
  fn1 = encrypedHashes[i]
  server.get(fn1).addCallback(grepChunks, i, server, encrypedHashes, inputHash, chunkSize)




def maidSafeDecrypt(inputHash, chunkSize, server, grepNotDone=True, iterations=1000, xor=False):

    # Getting back the objects:
    with open(inputHash, 'rb') as f:
        shas, encHashes = pickle.load(f)

    # Get filename
    filename = inputHash.replace('.hashes', '')

    # Erase file if already existing...
    fc = open(('reconstructed/' + filename), 'w')
    fc.write('')
    fc.close()

    noOfChunks = len(shas)


    # Grep chunks if not done befor. Return and let callback do the job
    if (grepNotDone):
      server.get(encHashes[0]).addCallback(grepChunks, 0, server, encHashes, inputHash, chunkSize)
      return


    # Resolve file from chunks
    for i in range(0, noOfChunks):

      # Get first item to decipher. First hash in the list and so on
      fn1 = encHashes[i]

      fc = open(('scrambled/' + fn1), 'rb')
      scrambledData = fc.read().encode('hex')
      fc.close()

      # Get data and create chunk #
      chunkNumer = i

      # Pick right hash...
      if(chunkNumer == 0):
        shaOne = shas[noOfChunks-1]
        shaTwo = shas[noOfChunks-2]
        shaThree = shas[chunkNumer]
      elif(chunkNumer == 1):
        shaOne = shas[noOfChunks-1]
        shaTwo = shas[chunkNumer-1]
        shaThree = shas[chunkNumer]
      else:
        shaOne = shas[chunkNumer-2]
        shaTwo = shas[chunkNumer-1]
        shaThree = shas[chunkNumer]


      # Need massive key deriv to xor out of AES
      if xor: keyDerivOut = keyDeriv(shaOne, shaTwo, shaThree, len(scrambledData.decode('hex')), iterations)
      else : keyDerivOut = keyDeriv(shaOne, shaTwo, shaThree, 48, iterations)

      # Unxor if needed
      if xor: unXored = strxor(scrambledData.decode("hex"),keyDerivOut.decode("hex"))
      else: unXored = scrambledData.decode('hex')

      # Setup cipher with key = first half[:32] of pbkdf2, and IV = second part[:16]
      cipher = AES.new(keyDerivOut[:64].decode('hex'), AES.MODE_CFB, keyDerivOut[64:(64+32)].decode('hex'))

      # Encrypt
      outCipher = (cipher.decrypt(unXored))

      # Append decrypted data to file...
      fc = open(('reconstructed/' + filename), 'ab')
      fc.write(outCipher)
      fc.close()

      print 'Chunk...'
