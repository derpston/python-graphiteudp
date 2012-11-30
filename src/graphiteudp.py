__version__ = "0.0.2"

import time
import logging
import warnings
import socketcache
logger = logging.getLogger("graphiteudp")

# If the user wants to use the module-level interface, this will hold a
# reference to a Client object. Otherwise, the user will use the Client
# object directly.
_module_client = None

class GraphiteUDPClient:
   def __init__(self, host = "localhost", port = 2003, prefix = None, debug = False):
      self._host = socketcache.UDPSocketCache(host, port)
      self._addr = (host, port)
      self._prefix = prefix
      self._debug = debug

   def send(self, metric, value, timestamp = None):
      if timestamp is None:
         timestamp = int(time.time())

      message = "%s %f %d\n" % (metric, value, timestamp)

      if self._prefix is not None:
         message = self._prefix + "." + message

      if self._debug:
         logger.debug("%s -> %s" % (repr(message), repr(self._addr)))
      else:
         try:
            (sock, addr) = self._host.get()
            sock.sendto(message, addr)
         except Exception, ex:
            logging.info("Failed to send graphite UDP message: %s" % ex)

def init(*args, **kwargs):
   global _module_client
   _module_client = GraphiteUDPClient(*args, **kwargs)

def send(*args, **kwargs):
   if _module_client is not None:
      _module_client.send(*args, **kwargs)
   else:
      warnings.warn("graphiteudp.send called before graphiteudp.init, metrics will be dropped.", RuntimeWarning, 2)
