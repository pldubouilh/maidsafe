from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import sys
import hashlib
import binascii
import base64
import hashlib
from pbkdf2 import pbkdf2_hex
from shaGeneration import *
from entropy import *
from tools import *
import pdb
#pdb.set_trace()

import pickle
import time
from twisted.internet import reactor, task
from twisted.python import log
from kademlia.network import Server




def sendChunks(result, i, server, encrypedHashes):

  print 'GET >> ' + str(i)

  # Out of bound, stop reactor and leave
  if i == len(encrypedHashes) :
    reactor.stop()
    return

  # Get file i
  fn1 = encrypedHashes[i]
  fc = open(('scrambled/' + fn1), 'rb')
  scrambledData = fc.read().encode('hex')
  fc.close()

  # Increment i for next call
  i += 1

  # Set hash(encChunk), encChunk on NW. Call back here !
  server.set(fn1, scrambledData).addCallback(sendChunks, i, server, encrypedHashes)



def maidSafeEncrypt(inputFile, chunkSize, server, iterations=1000, xor=False, i=0):

    # List and save all shas
    shas = listShas(inputFile, chunkSize)

    # Read the contents of the file
    f = open(inputFile, 'rb')
    data = f.read() # read the entire content of the file
    f.close()

    # Save filename and hash
    fileHash = hashlib.sha512(data).hexdigest()

    # Get the length of data, ie size of the input file in bytes
    bytes = len(data)

    # Calculate the number of chunks to be created
    noOfChunks= bytes/chunkSize
    if(bytes%chunkSize):
      noOfChunks+=1

    # Init Encripted hashes list
    encrypedHashes = []

    # Scan all chunks
    for i in range(0, bytes, chunkSize):

      # Get data and create chunk #
      chunkNumer = i/chunkSize
      dataToHash = data[i:i+ chunkSize]

      # Prevent creation of 0 bit file is filezise is multiple of 2^n
      if(len(dataToHash) == 0):
        continue


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
      if xor : keyDerivOut = keyDeriv(shaOne, shaTwo, shaThree, len(dataToHash), iterations)
      else : keyDerivOut = keyDeriv(shaOne, shaTwo, shaThree, 48, iterations)

      # Encrypt
      cipher = AES.new(keyDerivOut[:64].decode('hex'), AES.MODE_CFB, keyDerivOut[64:(64+32)].decode('hex'))
      outCipher = cipher.encrypt(dataToHash).encode('hex')

      # Quick sanity check
      print 'Cipherin\' !'

      # Xor outCipher and pbkdfOut
      if xor : scrambledChunck = strxor(outCipher.decode("hex"),keyDerivOut.decode("hex"))
      else : scrambledChunck = outCipher.decode('hex')


      # Compute hash of encrypted datas
      fn1 = hashlib.sha512(scrambledChunck).hexdigest()
      encrypedHashes.append(fn1)


      fc = open(('scrambled/' + fn1), 'wb')
      fc.write(scrambledChunck)
      fc.close()


    # Saving the objects:
    with open(inputFile + '.hashes', 'wb') as f:
        pickle.dump([shas, encrypedHashes], f)


    # Send chunks on DHT
    sendChunks(0, 0, server, encrypedHashes)
