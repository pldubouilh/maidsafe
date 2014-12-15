import pyscrypt

hashed = pyscrypt.hash(password = "correct horse battery staple",
                       salt = "seasalt",
                       N = 1024,
                       r = 1,
                       p = 1,
                       dkLen = 256)
print hashed.encode('hex')
