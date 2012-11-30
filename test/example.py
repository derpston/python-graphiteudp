import sys
import logging
sys.path.insert(0, "../src/")
import graphiteudp

graphiteudp.send("foo", 1.2)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # Writes to stderr by default
handler.setFormatter(logging.Formatter('%(process)d %(name)s %(levelname)s %(message)s'))
logger.addHandler(handler)

graphiteudp.init(debug = True)
graphiteudp.send("foo2", 1.2)

graphiteudp.init("example.com")
graphiteudp.send("foo3", 1.2)

graphiteudp.init("example.com", 2005)
graphiteudp.send("foo3", 1.2)

graphiteudp.init("example.com", 2005, prefix = "bzrt")
graphiteudp.send("foo4", 1.2, 100)

