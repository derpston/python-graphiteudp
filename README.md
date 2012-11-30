python-graphiteudp
==================

Python module for sending metrics to Graphite over UDP.

Features
--------
* Simple module-level interface, can be configured by one module and that configuration will be reused across an application importing it
* Uses python-socketcache to minimise DNS lookups and creating new socket objects for minimum performance impact on the application
* Supports a debug mode where metric messages are logged and not sent
* Logs messages for network errors instead of blowing up

Example
-------
```python
import graphiteudp

# By default, sends metrics to localhost:2003 with no prefix.
graphiteudp.init()
graphiteudp.send("foo", 1)

# Send to a specific host, add a prefix, and log messages instead of sending them.
graphiteudp.init("graphite.example.com", prefix = "myapp", debug = True)
# Generates log message: DEBUG 'myapp.bar.monkey 123.000000 1354307985\n' -> ('graphite.example.com', 2003)
graphiteudp.send("bar.monkey", 123)
```

#### For multiple modules in the same application, graphiteudp.init() only needs to be called once.
##### foo.py
```python
import graphiteudp
graphiteudp.init(...)
import bar
```

##### bar.py
```python
import graphiteudp
graphiteudp.send("bar.things", 1)
```

#### Multiple client objects can be maintained if you need to.
```python
import graphiteudp

g = graphiteudp.GraphiteUDPClient(...)
g.send("foo", 1)
```

BUGS
----
Unknown.

TODO
----
* Should use the adns module for non-blocking DNS where available.
* Should probably not depend on python-socketcache, but should use it where available.
* Add a simple Timer class supporting ```with``` syntax (```__enter__``` and ```__exit__```)
* Tests

Contributing
------------
Contributions welcome!
