import setup_path

import jippy

import shutil
import tempfile

def test_installation():
    tmpdir = tempfile.mkdtemp('test_jvm_installation')
    try:
        path = jippy.install_jvm(tmpdir)
        assert(jippy.is_jvm_location(path))
    finally:
        shutil.rmtree(tmpdir)
