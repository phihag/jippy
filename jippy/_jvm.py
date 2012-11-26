
import hashlib
import io
import platform
import os
import sys
import tarfile
import tempfile

from . import _util

_JVM_DOWNLOAD_URL = 'http://www.java.com/en/download/manual.jsp?locale=en'

# Mapping from Python architecture (platform.machine() to Java's)
_JAVA_ARCH = {
    'x86_64': 'amd64',
}

JVM_LOCROOT_SYSTEM = '/usr/share/jippy/jvms/'
JVM_LOCROOT_USER = os.path.expanduser('~/.local/share/jippy/jvms/')

DEFAULT_CACHE_DIR = os.path.expanduser('~/.local/share/jippy/downloads/')

class NoJVMFoundError(RuntimeError):
    pass

def _listall(path):
    for fn in os.listdir(path):
        yield os.path.join(path, fn)

def _list_jvm_candidates_roots():
    """ Yield all candidates for a JVM """
    if 'JAVA_HOME' in os.environ:
        yield os.environ['JAVA_HOME']
    # No yield from for backwards compatibility
    for c in _listall(os.path.join(JVM_LOCROOT_USER, sys.platform + '-' + platform.machine())):
        yield c
    for c in _listall(os.path.join(JVM_LOCROOT_SYSTEM, sys.platform + '-' + platform.machine())):
        yield c
    yield os.path.dirname(os.path.abspath(os.readlink('/usr/bin/java')))
    for c in _listall('/usr/lib/jvm'):
        yield c

def _list_jvm_locations():
    for root in _list_jvm_candidates_roots():
        p = os.path.join(root, jvm_name)
        if is_jvm_location(p):
            yield p

def _find_libjvm_so(loc):
    java_arch = _JAVA_ARCH.get(platform.machine())
    subdirs = [
        os.path.join('jre', 'lib', java_arch, 'server'), # OpenJDK on debian
        'lib',                                           # Sun JRE on debian
        os.path.join('lib', java_arch, 'server'),        # Oracle JDK on Linux,
        os.path.curdir                                   # Location already complete
    ]
    for subdir in subdirs:
        fn = os.path.join(loc, subdir, 'libjvm.so')
        print(fn)
        if os.path.isfile(fn):
            return fn
    return None

def is_jvm_location(loc):
    return _find_libjvm_so(loc) is not None

def find_jvm_location(locations=None, auto_install=False):
    """
    Find a JVM on the system.
    If auto_install is set, automatically a JVM if none is present (may take a while)
    """
    if not locations:
        locations = _list_jvm_locations()
    try:
        return next(locations)
    except IndexError:
        if auto_install:
            return install_jvm()
        else:
            raise NoJVMFoundError()

def install_jvm(loc_root=JVM_LOCROOT_USER, cache_dir=None):
    """
    Download and install a JVM into the specified location root.
    Return the actual location.
    cache_dir specifies the location of the directory where the large downloads (not the index is cached). Set to False to disable caching.
    """
    import urllib
    import re

    if cache_dir is None:
        cache_dir = DEFAULT_CACHE_DIR
    dlp = urllib.urlopen(_JVM_DOWNLOAD_URL)
    try:
        dlPage = dlp.read()
    finally:
        dlp.close()

    def _findLink(linkText):
        m = re.match(r'.*?<a title="' + re.escape(linkText) + '" href="([^"]+)"', dlPage, re.DOTALL)
        if not m:
            raise ValueError('Cannot find specified link text ' + repr(linkText) + ' in JVM download page')
        return m.group(1)

    def _downloadFile(url):
        """ Returns a bytes object of the downloaded url """
        if cache_dir != False:
            cacheId = hashlib.sha512(url.encode('utf-8')).hexdigest()
            cacheFn = os.path.join(cache_dir, cacheId)
            try:
                with open(cacheFn, 'rb') as cacheFile:
                    return cacheFile.read()
            except IOError:
                pass # Cache file not present, download
        dl = urllib.urlopen(url)
        try:
            content = dl.read()
        finally:
            dl.close()
        if cache_dir != False:
            try:
                _util.makedirs(cache_dir)
                with tempfile.NamedTemporaryFile(dir=cache_dir, prefix='jvm_cache_' + cacheId, delete=False) as tf:
                    tf.write(content)
                os.rename(tf.name, cacheFn) # atomic - the cache file should always be of full size
            except IOError:
                pass # Creation of cache file failed, but that's not that important
        return content

    if sys.platform == 'linux2':
        if platform.machine() == 'i386':
            url = _findLink(' Download Java software for Linux')
        elif platform.machine() == 'x86_64':
            url = _findLink(' Download Java software for Linux x64')
        else:
            raise NotImplementedError('JVM installation not yet implemented for ' + sys.platform + ' / ' + platform.machine())

        content = _downloadFile(url)
        with tarfile.open('r:gz', fileobj=io.BytesIO(content)) as tf:
            platf = sys.platform + '-' + platform.machine()
            vname = next(n for n in tf.getnames() if '/' not in n)
            jvmDir = os.path.join(loc_root, platf)
            _util.extractall_safely(tf, jvmDir)
            path = os.path.join(jvmDir, vname)
    else:
        raise NotImplementedError('JVM installation not yet implemented for ' + sys.platform)
    return path

class JVM(object):
    def __init__(self, path=None):
        if path is None:
            path = next(find_jvms())
        self._path = path


__all__ = ['JVM_LOCROOT_SYSTEM', 'JVM_LOCROOT_USER', 'is_jvm_location', 'install_jvm']
