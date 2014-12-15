from Crypto.PublicKey import RSA 
import hashlib

#65537
    
new_key = RSA.generate(2048, e=65537) 

public_key = new_key.publickey().exportKey("PEM") 
private_key = new_key.exportKey("PEM") 

print public_key

print '###########################'

binary =  new_key.exportKey("DER").encode("hex")
print binary

print '###########################'

hashd = hashlib.sha512(binary).hexdigest()
print hashd
