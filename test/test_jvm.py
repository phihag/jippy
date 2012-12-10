#!/usr/bin/env python

import setup_path

import unittest

import jippy

class TestJVM(unittest.TestCase):
    def test_basic(self):
        jvm = jippy.jvm()
        #jvm.call('java.lang.System.gc')

if __name__ == '__main__':
    unittest.main()
