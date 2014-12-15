from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys

# log to std out
log.startLogging(sys.stdout)

def quit(result):
    print "Key result:", result
    reactor.stop()

# Get value from NW. Callback > done...
def get(result, server):
    return server.get("a key").addCallback(quit)

# Set value on NW. Callback > Get
def set(found, server):
    log.msg("Found nodes: %s" % found)
    return server.set("a key", "a value").addCallback(get, server)


# Start Server
server = Server()

# Start own server on port 5678
server.listen(5678)

# Bootstrap with a known ip address of an existing kad server
# Callback on Set
server.bootstrap([('127.0.0.1', 8450)]).addCallback(set, server)

reactor.run()
