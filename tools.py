'''
from Crypto.Cipher import AES
import sys
import hashlib
import binascii
import base64
'''
from pbkdf2 import pbkdf2_hex
#from shaGeneration import *


def splitStringInTwo(given_str):
  return given_str[:len(given_str)/2], given_str[len(given_str)/2:]

def strxor(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))


def keyDeriv(shaOne, shaTwo, shaThree, size, iter):
  shas = shaOne + shaTwo + shaThree
  pw, salt = splitStringInTwo(shas)
  return pbkdf2_hex(pw,salt,keylen=size, iterations=iter)
