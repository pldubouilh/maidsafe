#!/usr/bin/python
#
# Stolen from Ero Carrera
# http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html

import math, string, sys, fileinput

# First Version
'''
def range_bytes (): return range(256)
def range_printable(): return (ord(c) for c in '0123456789abcdef')

def entropy(data, iterator=range_bytes):
    if not data:
        return 0
    entropy = 0
    for x in iterator():
        p_x = float(data.count(chr(x)))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy
'''

def entropy(string):
    #Calculates the Shannon entropy of a string

    # get probability of chars in string
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

    # calculate the entropy
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

    return entropy


def entropy_ideal(length):
    #Calculates the ideal Shannon entropy of a string with given length
    prob = 1.0 / length
    return -1.0 * length * prob * math.log(prob) / math.log(2.0)



'''
def main ():
    for row in fileinput.input():
        string = row.rstrip('\n')
        print ("%s: %f" % (string, H(string, range_printable)))

for str in ['gargleblaster', 'tripleee', 'magnus', 'lkjasdlk',
               'aaaaaaaa', 'sadfasdfasdf', '0123456789abcdef']:
    print ("%s: %f, ideally %f" % (str, entropy(str), entropy_ideal(len(str))))


toAnalyse = '0bef0db74df252efb19df85744987857e0cab0ee4c7b473a046331975efcda279fafe4e3faee37c2ba0e1d13b4b4ae3ecd62a6e0f31fe31048c648ac6e63aa0812d1cfa41aa64b6b2999590b04433db6f1846fb95c65b403308cfef59d279d49614064e4701f5690d58751a635e5d1f064829c6b71c8b5a36b3bf43a7ef9e1801a6b554ce40069f4e220a82fe824324a8b6b19d2f7c31ee0ef4d95f4c2ff357a70dda2b579fa88f9a8449c44d4e088e9b3d2e65ecd41d1aa1ed8859c23644b68fdf0d005f1daca591ab520d15aea9c6e0a068e7885c9026e1fb39e427533b5c99e398fb6512fdda7ab8997679a0bd69b2dcc43bf47c93f94287ab9f7940ff0017b41b2d468694e123dd5d87fe5117dfc052f38c4019080d7cde501e6b44e5d0bf6aa9943ab2a138b0f8c94dd5b77eeb0ecd6a2769d863982bfe70bc6e1ebb125d301b21f53786725a3f37d4845d4612bcd10e20171c073c779e365d792eeb1f238f4f873e4d647495e53fb4a3e9593ad5d35ee0357a24fb1e5fcb069b52340e53531434f83f68afda6abc3c4d19c486a7eccca81339dd9ba4e35df757a5a0aaaaeaa59d06d70977e7482bf3ad665a1dfeed27b73048a72a70ce7ded3085e76cbd70255c68825d9123711e55b6c95d4b109d6ceb3a4371ac05ff0f011215d799668959b9b72feb227b3558b5125c28c0daecdefc46a934b4e6bc5b44d6e95a84b1aff0fc0d5c66626b9c9c59d8ebe6159ad844d01771cedce187d574dbb85d8e1909548cdba431b9bbe8df0480469bdac81a3948a92195904d1b543745d57afecb5a4a7ab4da56c665b1244e74cbc45526928ef25a079e8c333c94879e167354810dcbe3afbe7a70213bae67ec2e8c48e570156b2ea9d79b80e68f080d3aa1004eaecbc46f86a3eab05ab7ebe2600a4eaa6a62d1a8cc56f2b672fc3f7911700511e6abb8131adfcfb286bbca2f10f3a7dbc34f4d19cc52e26377784b4e3d33b4c9f22b7cdb9e764e3414ebff1d25c21317069b735efbd2e16ee97bd9cb3550ccc4468ab343e40aded07024d3fa1eb0f587ee1943a94abd94fd9976325b472ff7aed4047488e71538a08ed3d59273b8455d976b9df9bc88fce79b93ab760195973a992da7f7fe38d3de6472e6fe684e0da1231fe882fb33e6623e2b9efce4498ecbc7ed1dc411150ccb8aa6693c8bb2017a07bd918360d1a61c831c95fa7d0b1f226117a6bd86eb2eedacbe938b3e3ab77950ed64e5f58488584d2df4c5409860ced185b3c6efe4ff5a81f273e9445402ed3c0f67ae0490eac9b43ee002f9b72c32a5afba98fad3990674d32b130ea84da01fde6fe2507bae0bbd774b9e60ab43e6f9be868e85f8cf967e2b0e66444d88aeb0732721877daf9a7d6a1d54a79d2ad4357b8e4c88e74f8dc691defc1efa0b827880735b8463bc7f6fbd046b78b9aca'

ent = entropy(toAnalyse)

print ("%s: %f" % (toAnalyse, ent))
print (entropy_ideal(len(toAnalyse)))
'''
