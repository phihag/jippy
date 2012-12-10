#!/usr/bin/env python

import setup_path

import jippy

import shutil
import tempfile
import unittest

class InstallationTest(unittest.TestCase):
    def test_installation(self):
        tmpdir = tempfile.mkdtemp('test_jvm_installation')
        try:
            path = jippy.install_jvm(tmpdir)
            assert(jippy.is_jvm_location(path))
        finally:
            shutil.rmtree(tmpdir)

if __name__ == '__main__':
    unittest.main()
