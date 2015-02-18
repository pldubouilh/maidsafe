import time
from itertools import izip
from itertools import imap
from itertools import takewhile
import operator
from collections import OrderedDict

from zope.interface import implements
from zope.interface import Interface

from kademlia.log import Logger
import pdb
import sys
import os

'''
    Using a sqlite3 to store chunks. Excruciatingly slow...
'''
'''
def query(conn, request):
    c = conn.cursor()
    c.execute("SELECT * FROM dht WHERE key='" + request.encode('hex') + "'")
    #c.execute("SELECT * FROM dht WHERE key='"+ request + "'")

    # TODO : Check if chunk existing.
    ''''''
    if c.fetchone() is not None:
        return c.fetchone()[1]

    else: return 'nope. nothing. sorry'
    ''''''
    return c.fetchone()[1]

def setOnDb(conn, key, val):
    c = conn.cursor()
    c.execute("SELECT * FROM dht WHERE key='" + key.encode('hex') + "'")
    check = c.fetchone()

    if check is not None:
        return

    #c.execute("INSERT INTO dht VALUES (?, ?)", (key, val))
    c.execute("INSERT INTO dht VALUES ('" + key.encode('hex') + "','" + val + "')")
    conn.commit()
'''


'''
    Using a simple file to store chunks
'''
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def query(request):
    inputFile = os.getcwd() + '/dht/' + request.encode('hex')
    f = open(inputFile, 'rb')
    data = f.read()
    f.close()
    return data


def setOnDb(key, val):
    newChunk = os.getcwd() +  '/dht/' + key.encode('hex')
    fc = open(newChunk, 'wb')
    fc.write(val)
    fc.close()



class IStorage(Interface):
    """
    Local storage for this node.
    """

    def __setitem__(key, value):
        """
        Set a key to the given value.
        """

    def __getitem__(key):
        """
        Get the given key.  If item doesn't exist, raises C{KeyError}
        """

    def get(key, default=None):
        """
        Get given key.  If not found, return default.
        """

    def iteritemsOlderThan(secondsOld):
        """
        Return the an iterator over (key, value) tuples for items older than the given secondsOld.
        """

    def iteritems():
        """
        Get the iterator for this storage, should yield tuple of (key, value)
        """


class ForgetlessStorage(object):
    implements(IStorage)

    def __init__(self, ttl=604800):
        """
        By default, max age is a week.
        """
        self.data = OrderedDict()
        self.ttl = ttl
        #self.conn = sqlite3.connect('/Users/joe/Desktop/maidsafe/dht.db')

    def __setitem__(self, key, value):
        '''
        if key in self.data:
            del self.data[key]
        self.data[key] = (time.time(), value)
        self.cull()
        '''
        #setOnDb(self.conn, key, value)
        setOnDb(key, value)


    def cull(self):
        for k, v in self.iteritemsOlderThan(self.ttl):
            self.data.popitem(last=False)

    def get(self, key, default=None):
        '''
        self.cull()
        if key in self.data:
            self.log.debug('GET B')
            return self[key]
        return default
        '''
        #return query(self.conn, key)
        return query(key)

    def __getitem__(self, key):
        #self.cull()
        #return self.data[key][1]
        #return query(self.conn, key)
        return query(key)


    def __iter__(self):
        self.cull()
        return iter(self.data)

    def __repr__(self):
        self.cull()
        return repr(self.data)

    def iteritemsOlderThan(self, secondsOld):
        minBirthday = time.time() - secondsOld
        zipped = self._tripleIterable()
        matches = takewhile(lambda r: minBirthday >= r[1], zipped)
        return imap(operator.itemgetter(0, 2), matches)

    def _tripleIterable(self):
        ikeys = self.data.iterkeys()
        ibirthday = imap(operator.itemgetter(0), self.data.itervalues())
        ivalues = imap(operator.itemgetter(1), self.data.itervalues())
        return izip(ikeys, ibirthday, ivalues)

    def iteritems(self):
        self.cull()
        ikeys = self.data.iterkeys()
        ivalues = imap(operator.itemgetter(1), self.data.itervalues())
        return izip(ikeys, ivalues)
