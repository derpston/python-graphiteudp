#!/usr/bin/env python

from distutils.core import setup

setup(
      name = 'graphiteudp'
   ,  version = '0.0.3'
   ,  description = 'A clean interface for sending metrics to Graphite over UDP'
   ,  long_description = """Uses a cache of socket objects to minimise DNS lookups and \
performance impact on the application. Supports a debug mode that logs metric messages, \
and handles network errors by logging an exception."""
   ,  author = 'Derp Ston'
   ,  author_email = 'derpston+pypi@sleepygeek.org'
   ,  url = 'https://github.com/derpston/python-graphiteudp'
   ,  packages = ['']
   ,  package_dir = {'': 'src'}
   ,  install_requires = ['socketcache']
   )

