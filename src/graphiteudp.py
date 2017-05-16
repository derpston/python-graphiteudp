__version__ = "0.0.2"

import time
import logging
import warnings
import socketcache
from contextlib2 import contextmanager
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
            sock.sendto(message.encode(), addr)
         except Exception as ex:
            logging.info("Failed to send graphite UDP message: %s" % ex)

def init(*args, **kwargs):
   global _module_client
   _module_client = GraphiteUDPClient(*args, **kwargs)

def send(*args, **kwargs):
   if _module_client is not None:
      _module_client.send(*args, **kwargs)
   else:
      warnings.warn("graphiteudp.send called before graphiteudp.init, metrics will be dropped.", RuntimeWarning, 2)


@contextmanager
def measure(metric, measure_func=time.time, reverse=False):
   """
   Function to allow usage of graphiteudp as both a context manager
   and a decorator. Takes an optional measure_func argument which is
   called before and after to obtain the `value` thats passed to
   graphiteudp.send. Defaults to time.

   Args:
      metric: The metric path to use.
      measure_func: The function thats called on entry and exit of the
         context or before and after a decorated function when used as
         a decorator.
      reverse: Reverse the order of arguments used when obtainning
         the difference.

   Examples:

      with graphite_measure('my.example.metric'):
         time.sleep(5)

      @graphite_measure('slow_function.time')
      def slow_function():
         time.sleep(5)

      def get_memory():
         return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

      with graphite_measure('memory_usage', get_memory):
         _ = [x for x in range(100000)]
   """
   try:
      before = measure_func()
      yield _module_client

   finally:
      if reverse:
         value = before - measure_func()
      else:
         value = measure_func() - before

      send(metric, value)
