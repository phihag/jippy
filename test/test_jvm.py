#!/usr/bin/env python

import setup_path

import jippy

def test_basic():
    jippy.jvm().call('java.lang.System.gc')
