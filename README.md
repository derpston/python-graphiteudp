python-graphiteudp
==================

Python module for sending metrics to Graphite over UDP.

Features
--------
* Simple module-level interface, can be configured by one module and that configuration will be reused across an application importing it
* Uses python-socketcache to minimise DNS lookups and creating new socket objects for minimum performance impact on the application
* Supports a debug mode where metric messages are logged and not sent
* Logs messages for network errors instead of blowing up

Examples
-------
```python
import graphiteudp

# By default, sends metrics to localhost:2003 with no prefix.
graphiteudp.init()
graphiteudp.send("foo", 1)

# Send to a specific host and add a prefix.
graphiteudp.init("graphite.example.com", prefix = "myapp")
graphiteudp.send("bar.monkey", 123)

# The above will send "myapp.bar.monkey 123.000000 1354307985\n" to Graphite.

graphiteudp.send("bar.monkey", 123, False)

# The above will send "myapp.bar.monkey 123.000000\n" to Graphite, allowing
# the server to use the arrival time of the packet instead of specifying
# a timestamp. Useful for embedded systems which may not keep accurate time.
```

#### Debug logging
If you'd like to just log a message for testing without sending anything, you can add the ```debug=True``` parameter to `init()`:

```python
graphiteudp.init("graphite.example.com", prefix="myapp", debug=True)

graphiteudp.send("bar.monkey", 123)

# With debug=True set above, calling .send will only log the message, like this:
# DEBUG 'myapp.bar.monkey 123.000000 1354307985\n' -> ('graphite.example.com', 2003)
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

#### As a context manager
```python
import graphiteudp
graphiteudp.init(...)

with graphiteudp.measure("sleep.time"):
    time.sleep(5)
```

```python
import graphiteudp
graphiteudp.init(...)

with graphiteudp.measure("sleep.time") as g:
    g.send("foo", 1)
    time.sleep(5)
```

#### As a decorator
```python
import time
import graphiteudp

@graphiteudp.measure('slow.function')
def slow_function():
  time.sleep(5)

slow_function()
```

BUGS
----
Unknown.

TODO
----
* Should use the adns module for non-blocking DNS where available.
* Should probably not depend on python-socketcache, but should use it where available.
* Tests

Contributing
------------
Contributions welcome!
