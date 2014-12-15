import sys
import hashlib
import pdb

# define the function to split the file into smaller chunks
def listShas(inputFile,chunkSize):

  #read the contents of the file
  f = open(inputFile, 'rb')
  data = f.read() # read the entire content of the file
  f.close()

  # get the length of data, ie size of the input file in bytes
  bytes = len(data)

  #calculate the number of chunks to be created
  noOfChunks= bytes/chunkSize
  if(bytes%chunkSize):
    noOfChunks+=1

  hashes = []

  for i in range(0, bytes+1, chunkSize):
    #fn1 = "chunk%s" % (i/chunkSize)

    dataToHash = data[i:i+ chunkSize]

    # Prevent creation of 0 bit file is filezise is multiple of 2^n
    if(len(dataToHash) == 0):
      continue

    #print 'HASH FILE #' + str(i/chunkSize) +  ' ==  ' + hashlib.sha512(data[i:i+ chunkSize]).hexdigest()
    hashes.append(hashlib.sha512(dataToHash).hexdigest())

    # Chunk of Data
    '''
    fc = open(fn1, 'wb')
    fc.write(dataToHash)
    fc.close()
    '''

  return hashes


#print listShas(sys.argv[1], 1024)
