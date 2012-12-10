
import ctypes
import hashlib
import io
import platform
import os
import sys
import tarfile
import tempfile
import threading

from . import _util
from .jvm_intf import *

_JVM_DOWNLOAD_URL = 'http://www.java.com/en/download/manual.jsp?locale=en'

# Mapping from Python architecture (platform.machine() to Java's)
_JAVA_ARCH = {
    'x86_64': 'amd64',
}

NO_CACHE = False

JVM_LOCROOT_SYSTEM = '/usr/share/jippy/jvms/'
JVM_LOCROOT_USER = os.path.expanduser('~/.local/share/jippy/jvms/')

DEFAULT_CACHE_DIR = os.path.expanduser('~/.local/share/jippy/downloads/')


class NoJVMFoundError(RuntimeError):
    pass

class JVMError(BaseException):
    pass

def _listall(path):
    try:
        for fn in os.listdir(path):
            yield os.path.join(path, fn)
    except OSError: # File not there or inaccessible, ignore
        return

def _list_jvm_candidates_roots():
    """ Yield all candidates for a JVM """
    if 'JAVA_HOME' in os.environ:
        yield os.environ['JAVA_HOME']
    # No yield from for backwards compatibility
    platName = sys.platform + '-' + platform.machine()
    for c in _listall(os.path.join(JVM_LOCROOT_USER, platName)):
        yield c
    for c in _listall(os.path.join(JVM_LOCROOT_SYSTEM, platName)):
        yield c
    yield os.path.dirname(os.path.abspath(os.readlink('/usr/bin/java')))
    for c in _listall('/usr/lib/jvm'):
        yield c

def _list_jvm_locations():
    for root in _list_jvm_candidates_roots():
        if is_jvm_location(root):
            yield root

def _find_libjvm_so(loc):
    java_arch = _JAVA_ARCH.get(platform.machine())
    subdirs = [
        os.path.join('jre', 'lib', java_arch, 'server'), # OpenJDK on debian
        'lib',                                           # Sun JRE on debian
        os.path.join('lib', java_arch, 'server'),        # Oracle JDK on Linux
        os.path.curdir,                                  # Full location
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
    If auto_install is set, automatically download and install a JVM if none is
        present (may take a while)
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
    cache_dir specifies the location of the directory where the large downloads
              (not the index) is cached. Set to NO_CACHE to disable caching.
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
        if cache_dir != NO_CACHE:
            cacheId = hashlib.sha512(url.encode('utf-8')).hexdigest()
            cacheFn = os.path.join(cache_dir, cacheId)
            try:
                with open(cacheFn, 'rb') as cacheFile:
                    return cacheFile.read()
            except IOError:
                pass  # Cache file not present, download
        dl = urllib.urlopen(url)
        try:
            content = dl.read()
        finally:
            dl.close()
        if cache_dir != NO_CACHE:
            try:
                _util.makedirs(cache_dir)
                with tempfile.NamedTemporaryFile(dir=cache_dir, prefix='jvm_cache_' + cacheId, delete=False) as tf:
                    tf.write(content)
                # atomic - the cache file should always be of full size
                os.rename(tf.name, cacheFn)
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
        raise NotImplementedError('JVM installation not yet implemented for ' +
                                  sys.platform)
    return path


class JVM(object):
    # For details on the inner workings, see
    # http://docs.oracle.com/javase/1.5.0/docs/guide/jni/spec/invocation.html

    def __init__(self, path=None, autostart=True, auto_install=None):
        if path is None:
            path = find_jvm_location(auto_install=auto_install)
        self._path = path
        self._autostart = autostart

    @property
    def started(self):
        return hasattr(self, '_dll')

    def start(self):
        """
        Start running the current JVM in the current process.
        Note that current JVM implementations support only one JVM per process.
        """
        self._dllPath = _find_libjvm_so(self._path)
        if self._dllPath is None:
            raise OSError('Cannot find JVM in specified path. '
              'Call find_jvm_location(..., auto_install=True) to download one.')
        self._dll = ctypes.cdll.LoadLibrary(self._dllPath)
        vm_args = _JavaVMInitArgs()
        vm_args.version = 0x00010002
        res = self._dll.JNI_GetDefaultJavaVMInitArgs(ctypes.pointer(vm_args))
        if res != 0:
            raise JVMError('JVM is too old, update to 1.2+')
        #self._dll.
        # TODO boot em up

    def call(self, name, **args):
        if not self.started and self._autostart:
            self.start()
        # TODO attach thread if necessary
        # TODO actually call
        # TODO handle result

    def matches_spec(self, spec):
        if spec.get('path'):
            if spec.get('path') != self._path:
                return False
        # autostart is ignored
        return True

_singleton_jvm_data = {
    'jvm': None,
    'lock': threading.Lock(),
}
def jvm(jvmSpec={}, auto_install=None):
    """
    Return a singleton JVM.
    Since virtually all JVM implementations only support one VM per process,
    that's all we can do.
    jvmSpec defines the requirements for the JVM. Current supported keys are:
        path - The location of the JVM in the file system
    Set auto_install to download and install a JVM if none is found.
    """

    with _singleton_jvm_data['lock']:
        if _singleton_jvm_data['jvm']:
            if not _singleton_jvm_data['jvm'].matches_spec(jvmSpec):
                raise Exception('Java VM already started, but it does not conform to requested specs')
        else:
            _singleton_jvm_data['jvm'] = JVM(auto_install=auto_install,
                                             **jvmSpec)

        return _singleton_jvm_data['jvm']

__all__ = ['JVM_LOCROOT_SYSTEM', 'JVM_LOCROOT_USER', 'NO_CACHE',
           'is_jvm_location', 'install_jvm', 'jvm']
