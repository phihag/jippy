_jboolean = ctypes.c_ubyte
_jbyte = ctypes.c_ubyte
_jchar = ctypes.c_short
_jshort = ctypes.c_int16
_jint = ctypes.c_int32
_jlong = ctypes.c_int64
_jfloat = ctypes.c_float
_jdouble = ctypes.c_double

_jsize = _jint


class _jobject_struct(ctypes.Structure):
    __fields = []
_jobject = ctypes.POINTER(_jobject_struct)
_jclass = _jobject
_jarray = _jobject
_jobjectArray = _jarray
_jbooleanArray = _jarray
_jbyteArray = _jarray
_jcharArray = _jarray
_jshortArray = _jarray
_jintArray = _jarray
_jlongArray = _jarray
_jfloatArray = _jarray
_jdoubleArray = _jarray
_jobjectArray = _jarray
_jweak = _jobject

class _jvalue(ctypes.Union):
    _fields_ = [
        (_jboolean, 'z'),
        (_jbyte, 'b'),
        (_jchar, 'c'),
        (_jshort, 's'),
        (_jint, 'i'),
        (_jlong, 'j'),
        (_jfloat, 'f'),
        (_jdouble, 'd'),
        (_jobject, 'l'),
    ]


class _jmethodID_struct(ctypes.Structure):
    _fields_ = []
_jmethodID = ctypes.POINTER(_jmethodID_struct)

class _jfieldID_struct(ctypes.Structure):
    _fields_ = []
_jfieldID = ctypes.POINTER(_jfieldID_struct)

class _JNINativeMethod(ctypes.Structure):
    _fields = [
        (ctypes.c_char_p, 'name'),
        (ctypes.c_char_p, 'signature'),
        (ctypes.c_void_p, 'fnPtr'),
    ]

class _JavaVMOption(ctypes.Structure):
    _fields = [
        ('optionString', ctypes.c_char_p),
        ('extraInfo', ctypes.c_void_p),
    ]

class _JavaVMInitArgs(ctypes.Structure):
    _fields = [
        ('version', _jint),
        ('nOptions', _jint),
        ('options', ctypes.POINTER(_JavaVMOption)),
        ('ignoreUnrecognized', _jboolean)
    ]

class _JavaVM(ctypes.Structure):
    _fields = [
        ('functions', ctypes.c_void_p),
        # really a ctypes.POINTER(_JNIInvokeInterface)
    ]

class _JNIInvokeInterface(ctype.Structure):
    _fields = [
        ('reserved0', ctypes.c_void_p),
        ('reserved1', ctypes.c_void_p),
        ('reserved2', ctypes.c_void_p),

        ('DestroyJavaVM',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                _jint,
                ctypes.POINTER(_JavaVM))           # JavaVM* vm
            )
        ),
        ('AttachCurrentThread',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                _jint,
                ctypes.POINTER(_JavaV_),           # JavaVM* vm
                ctypes.POINTER(ctypes.c_void_p)),  # void** penv
                ctypes.c_void_p),                  # void* args
            )
        ),
        ('DetachCurrentThread',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                _jint,
                ctypes.POINTER(_JavaVM),           # JavaVM* vm
            )
        ),
        ('GetEnv',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                _jint,
                ctypes.POINTER(_JavaVM),           # JavaVM* vm
                ctypes.POINTER(ctypes.c_void_p)),  # void** penv
                _jint),                            # jint version
            )
        ),
        ('AttachCurrentThreadAsDaemon',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                _jint,
                ctypes.POINTER(_JavaVM),           # JavaVM* vm
                ctypes.POINTER(ctypes.c_void_p)),  # void** penv
                ctypes.c_void_p),                  # void* args
            )
        ),
   ]

class _JNIEnv(ctypes.Structure):
    _fields = [
        ('functions', ctypes.c_void_p),
        # really a ctypes.POINTER(_JNINativeInterface)
    ]

class _JNINativeInterface(ctypes.Structure):
    _fields = [
        ('reserved0', ctypes.c_void_p),
        ('reserved1', ctypes.c_void_p),
        ('reserved2', ctypes.c_void_p),
        ('reserved3', ctypes.c_void_p),


    ]
