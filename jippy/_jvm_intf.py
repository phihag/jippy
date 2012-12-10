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

        ('foo',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.c_int,                    # a
                ctypes.POINTER(ctypes.c_int),    # b
            )
        ),
        ('GetVersion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
            )
        ),
        ('DefineClass',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.POINTER(ctypes.c_char),   # name
                _jobject,                        # loader
                ctypes.POINTER(_jbyte),          # buf
                _jsize,                          # len
            )
        ),
        ('FindClass',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.POINTER(ctypes.c_char),   # name
            )
        ),
        ('FromReflectedMethod',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # method
            )
        ),
        ('FromReflectedField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # field
            )
        ),
        ('ToReflectedMethod',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # cls
                _jmethodID,                      # methodID
                _jboolean,                       # isStatic
            )
        ),
        ('GetSuperclass',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # sub
            )
        ),
        ('IsAssignableFrom',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # sub
                _jclass,                         # sup
            )
        ),
        ('ToReflectedField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # cls
                _jfieldID,                       # fieldID
                _jboolean,                       # isStatic
            )
        ),
        ('Throw',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jthrowable,                     # obj
            )
        ),
        ('ThrowNew',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                ctypes.POINTER(ctypes.c_char),   # msg
            )
        ),
        ('ExceptionOccurred',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
            )
        ),
        ('ExceptionDescribe',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
            )
        ),
        ('ExceptionClear',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
            )
        ),
        ('FatalError',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.POINTER(ctypes.c_char),   # msg
            )
        ),
        ('PushLocalFrame',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jint,                           # capacity
            )
        ),
        ('PopLocalFrame',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # result
            )
        ),
        ('NewGlobalRef',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # lobj
            )
        ),
        ('DeleteGlobalRef',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # gref
            )
        ),
        ('DeleteLocalRef',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
            )
        ),
        ('IsSameObject',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj1
                _jobject,                        # obj2
            )
        ),
        ('NewLocalRef',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # ref
            )
        ),
        ('EnsureLocalCapacity',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jint,                           # capacity
            )
        ),
        ('AllocObject',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
            )
        ),
        # NewObject skipped because of varargs
        # NewObjectV skipped because of varargs
        ('NewObjectA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        ('GetObjectClass',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
            )
        ),
        ('IsInstanceOf',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
            )
        ),
        ('GetMethodID',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                ctypes.POINTER(ctypes.c_char),   # name
                ctypes.POINTER(ctypes.c_char),   # sig
            )
        ),
        # CallObjectMethod skipped because of varargs
        # CallObjectMethodV skipped because of varargs
        ('CallObjectMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallBooleanMethod skipped because of varargs
        # CallBooleanMethodV skipped because of varargs
        ('CallBooleanMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallByteMethod skipped because of varargs
        # CallByteMethodV skipped because of varargs
        ('CallByteMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallCharMethod skipped because of varargs
        # CallCharMethodV skipped because of varargs
        ('CallCharMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallShortMethod skipped because of varargs
        # CallShortMethodV skipped because of varargs
        ('CallShortMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallIntMethod skipped because of varargs
        # CallIntMethodV skipped because of varargs
        ('CallIntMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallLongMethod skipped because of varargs
        # CallLongMethodV skipped because of varargs
        ('CallLongMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallFloatMethod skipped because of varargs
        # CallFloatMethodV skipped because of varargs
        ('CallFloatMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallDoubleMethod skipped because of varargs
        # CallDoubleMethodV skipped because of varargs
        ('CallDoubleMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallVoidMethod skipped because of varargs
        # CallVoidMethodV skipped because of varargs
        ('CallVoidMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualObjectMethod skipped because of varargs
        # CallNonvirtualObjectMethodV skipped because of varargs
        ('CallNonvirtualObjectMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualBooleanMethod skipped because of varargs
        # CallNonvirtualBooleanMethodV skipped because of varargs
        ('CallNonvirtualBooleanMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualByteMethod skipped because of varargs
        # CallNonvirtualByteMethodV skipped because of varargs
        ('CallNonvirtualByteMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualCharMethod skipped because of varargs
        # CallNonvirtualCharMethodV skipped because of varargs
        ('CallNonvirtualCharMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualShortMethod skipped because of varargs
        # CallNonvirtualShortMethodV skipped because of varargs
        ('CallNonvirtualShortMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualIntMethod skipped because of varargs
        # CallNonvirtualIntMethodV skipped because of varargs
        ('CallNonvirtualIntMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualLongMethod skipped because of varargs
        # CallNonvirtualLongMethodV skipped because of varargs
        ('CallNonvirtualLongMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualFloatMethod skipped because of varargs
        # CallNonvirtualFloatMethodV skipped because of varargs
        ('CallNonvirtualFloatMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualDoubleMethod skipped because of varargs
        # CallNonvirtualDoubleMethodV skipped because of varargs
        ('CallNonvirtualDoubleMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallNonvirtualVoidMethod skipped because of varargs
        # CallNonvirtualVoidMethodV skipped because of varargs
        ('CallNonvirtualVoidMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        ('GetFieldID',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                ctypes.POINTER(ctypes.c_char),   # name
                ctypes.POINTER(ctypes.c_char),   # sig
            )
        ),
        ('GetObjectField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetBooleanField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetByteField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetCharField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetShortField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetIntField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetLongField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetFloatField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('GetDoubleField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
            )
        ),
        ('SetObjectField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jobject,                        # val
            )
        ),
        ('SetBooleanField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jboolean,                       # val
            )
        ),
        ('SetByteField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jbyte,                          # val
            )
        ),
        ('SetCharField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jchar,                          # val
            )
        ),
        ('SetShortField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jshort,                         # val
            )
        ),
        ('SetIntField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jint,                           # val
            )
        ),
        ('SetLongField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jlong,                          # val
            )
        ),
        ('SetFloatField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jfloat,                         # val
            )
        ),
        ('SetDoubleField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
                _jfieldID,                       # fieldID
                _jdouble,                        # val
            )
        ),
        ('GetStaticMethodID',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                ctypes.POINTER(ctypes.c_char),   # name
                ctypes.POINTER(ctypes.c_char),   # sig
            )
        ),
        # CallStaticObjectMethod skipped because of varargs
        # CallStaticObjectMethodV skipped because of varargs
        ('CallStaticObjectMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticBooleanMethod skipped because of varargs
        # CallStaticBooleanMethodV skipped because of varargs
        ('CallStaticBooleanMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticByteMethod skipped because of varargs
        # CallStaticByteMethodV skipped because of varargs
        ('CallStaticByteMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticCharMethod skipped because of varargs
        # CallStaticCharMethodV skipped because of varargs
        ('CallStaticCharMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticShortMethod skipped because of varargs
        # CallStaticShortMethodV skipped because of varargs
        ('CallStaticShortMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticIntMethod skipped because of varargs
        # CallStaticIntMethodV skipped because of varargs
        ('CallStaticIntMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticLongMethod skipped because of varargs
        # CallStaticLongMethodV skipped because of varargs
        ('CallStaticLongMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticFloatMethod skipped because of varargs
        # CallStaticFloatMethodV skipped because of varargs
        ('CallStaticFloatMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticDoubleMethod skipped because of varargs
        # CallStaticDoubleMethodV skipped because of varargs
        ('CallStaticDoubleMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        # CallStaticVoidMethod skipped because of varargs
        # CallStaticVoidMethodV skipped because of varargs
        ('CallStaticVoidMethodA',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # cls
                _jmethodID,                      # methodID
                ctypes.POINTER(_jvalue),         # args
            )
        ),
        ('GetStaticFieldID',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                ctypes.POINTER(ctypes.c_char),   # name
                ctypes.POINTER(ctypes.c_char),   # sig
            )
        ),
        ('GetStaticObjectField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticBooleanField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticByteField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticCharField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticShortField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticIntField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticLongField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticFloatField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('GetStaticDoubleField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
            )
        ),
        ('SetStaticObjectField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jobject,                        # value
            )
        ),
        ('SetStaticBooleanField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jboolean,                       # value
            )
        ),
        ('SetStaticByteField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jbyte,                          # value
            )
        ),
        ('SetStaticCharField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jchar,                          # value
            )
        ),
        ('SetStaticShortField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jshort,                         # value
            )
        ),
        ('SetStaticIntField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jint,                           # value
            )
        ),
        ('SetStaticLongField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jlong,                          # value
            )
        ),
        ('SetStaticFloatField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jfloat,                         # value
            )
        ),
        ('SetStaticDoubleField',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                _jfieldID,                       # fieldID
                _jdouble,                        # value
            )
        ),
        ('NewString',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.POINTER(_jchar),          # unicode
                _jsize,                          # len
            )
        ),
        ('GetStringLength',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
            )
        ),
        ('GetStringChars',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('ReleaseStringChars',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
                ctypes.POINTER(_jchar),          # chars
            )
        ),
        ('NewStringUTF',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.POINTER(ctypes.c_char),   # utf
            )
        ),
        ('GetStringUTFLength',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
            )
        ),
        ('GetStringUTFChars',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('ReleaseStringUTFChars',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
                ctypes.POINTER(ctypes.c_char),   # chars
            )
        ),
        ('GetArrayLength',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jarray,                         # array
            )
        ),
        ('NewObjectArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
                _jclass,                         # clazz
                _jobject,                        # init
            )
        ),
        ('GetObjectArrayElement',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobjectArray,                   # array
                _jsize,                          # index
            )
        ),
        ('SetObjectArrayElement',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobjectArray,                   # array
                _jsize,                          # index
                _jobject,                        # val
            )
        ),
        ('NewBooleanArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewByteArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewCharArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewShortArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewIntArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewLongArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewFloatArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('NewDoubleArray',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jsize,                          # len
            )
        ),
        ('GetBooleanArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbooleanArray,                  # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetByteArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbyteArray,                     # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetCharArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jcharArray,                     # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetShortArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetIntArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetLongArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jlongArray,                     # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetFloatArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jfloatArray,                    # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('GetDoubleArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jdoubleArray,                   # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('ReleaseBooleanArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbooleanArray,                  # array
                ctypes.POINTER(_jboolean),       # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseByteArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbyteArray,                     # array
                ctypes.POINTER(_jbyte),          # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseCharArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jcharArray,                     # array
                ctypes.POINTER(_jchar),          # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseShortArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                ctypes.POINTER(_jshort),         # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseIntArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                ctypes.POINTER(_jint),           # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseLongArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jlongArray,                     # array
                ctypes.POINTER(_jlong),          # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseFloatArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jfloatArray,                    # array
                ctypes.POINTER(_jfloat),         # elems
                _jint,                           # mode
            )
        ),
        ('ReleaseDoubleArrayElements',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jdoubleArray,                   # array
                ctypes.POINTER(_jdouble),        # elems
                _jint,                           # mode
            )
        ),
        ('GetBooleanArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbooleanArray,                  # array
                _jsize,                          # start
                _jsize,                          # l
                ctypes.POINTER(_jboolean),       # buf
            )
        ),
        ('GetByteArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbyteArray,                     # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jbyte),          # buf
            )
        ),
        ('GetCharArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jcharArray,                     # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jchar),          # buf
            )
        ),
        ('GetShortArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jshort),         # buf
            )
        ),
        ('GetIntArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jint),           # buf
            )
        ),
        ('GetLongArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jlongArray,                     # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jlong),          # buf
            )
        ),
        ('GetFloatArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jfloatArray,                    # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jfloat),         # buf
            )
        ),
        ('GetDoubleArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jdoubleArray,                   # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jdouble),        # buf
            )
        ),
        ('SetBooleanArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbooleanArray,                  # array
                _jsize,                          # start
                _jsize,                          # l
                ctypes.POINTER(_jboolean),       # buf
            )
        ),
        ('SetByteArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jbyteArray,                     # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jbyte),          # buf
            )
        ),
        ('SetCharArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jcharArray,                     # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jchar),          # buf
            )
        ),
        ('SetShortArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jshort),         # buf
            )
        ),
        ('SetIntArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jintArray,                      # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jint),           # buf
            )
        ),
        ('SetLongArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jlongArray,                     # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jlong),          # buf
            )
        ),
        ('SetFloatArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jfloatArray,                    # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jfloat),         # buf
            )
        ),
        ('SetDoubleArrayRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jdoubleArray,                   # array
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jdouble),        # buf
            )
        ),
        ('RegisterNatives',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
                ctypes.POINTER(_JNINativeMethod), # methods
                _jint,                           # nMethods
            )
        ),
        ('UnregisterNatives',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jclass,                         # clazz
            )
        ),
        ('MonitorEnter',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
            )
        ),
        ('MonitorExit',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
            )
        ),
        ('GetJavaVM',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.POINTER(ctypes.POINTER(_JavaVM)), # vm
            )
        ),
        ('GetStringRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(_jchar),          # buf
            )
        ),
        ('GetStringUTFRegion',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # str
                _jsize,                          # start
                _jsize,                          # len
                ctypes.POINTER(ctypes.c_char),   # buf
            )
        ),
        ('GetPrimitiveArrayCritical',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jarray,                         # array
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('ReleasePrimitiveArrayCritical',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jarray,                         # array
                ctypes.c_void_p,                 # carray
                _jint,                           # mode
            )
        ),
        ('GetStringCritical',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # string
                ctypes.POINTER(_jboolean),       # isCopy
            )
        ),
        ('ReleaseStringCritical',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jstring,                        # string
                ctypes.POINTER(_jchar),          # cstring
            )
        ),
        ('NewWeakGlobalRef',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
            )
        ),
        ('DeleteWeakGlobalRef',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jweak,                          # ref
            )
        ),
        ('ExceptionCheck',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
            )
        ),
        ('NewDirectByteBuffer',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                ctypes.c_void_p,                 # address
                _jlong,                          # capacity
            )
        ),
        ('GetDirectBufferAddress',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # buf
            )
        ),
        ('GetDirectBufferCapacity',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # buf
            )
        ),
        ('GetObjectRefType',
            ctypes.POINTER(ctypes.CFUNCTYPE(
                ctypes.POINTER(_JNIEnv),         # env
                _jobject,                        # obj
            )
        ),
    ]
