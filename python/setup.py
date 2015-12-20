#!/usr/bin/env python

from distutils.core import setup

setup(name='amplifier',
      version='2.0.0',
      description='Python library for interfacing custom network (i2c controlled) WiFi amplifier',
      author='Ronald Diaz',
      author_email='ronald@ronalddiaz.net',
      url='http://github.com/ronnied/wifi-amplifier',
      license = 'LICENSE.txt',
      long_description=open('README.txt').read(),
      packages=['amplifier'],
)
