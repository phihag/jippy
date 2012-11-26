import errno
import os
import sys

def makedirs(path):
    """ Create a directory hierarchy if it's not there. """
    if sys.version >= (3,2):
        os.makedirs(path, exist_ok=True)
    else:
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass # Directory already present
            else:
                raise

def extractall_safely(tarf, dir):
    """
    Like tarfile.TarFile.extractall, but without the path traversal
    """
    rootDir = os.path.abspath(dir)
    if not rootDir.endswith(os.path.sep):
        rootDir += os.path.sep
    def is_safe_member(m):
        effName = os.path.abspath(os.path.join(dir, m.name))
        return effName.startswith(rootDir)

    tarf.extractall(dir, members=filter(is_safe_member, tarf.getmembers()))
