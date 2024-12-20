""" 根据live2dCubismCore.h头文件，封装了Live2D模型的相关数据结构。"""
import ctypes
import sys

# Cubism moc.
class csmMoc(ctypes.Structure):
    """ Live2D模型文件类型结构体，根据live2dCubismCore.h头文件，封装了Live2D模型文件的相关数据结构。
    源代码：
    ```c++
    typedef struct csmMoc csmMoc;
    ```
    """
    _fields_ = [] # 没有字段

# Cubism model.
class csmModel(ctypes.Structure):
    """ Live2D模型类型结构体，根据live2dCubismCore.h头文件，封装了Live2D模型的相关数据结构。
    源代码：
    ```c++
    typedef struct csmModel csmModel;
    ```
    """
    _fields_ = [] # 没有字段

csmVersion = ctypes.c_uint
""" Live2D模型版本号。
源代码如下:
```c++
typedef unsigned int csmVersion;
```
"""
csmAlignofMoc = 64
csmAlignofModel = 16
csmBlendAdditive = 1 << 0
csmBlendMultiplicative = 1 << 1
csmIsDoubleSided = 1 << 2
csmIsInvertedMask = 1 << 3
csmIsVisible = 1 << 0
csmVisibilityDidChange = 1 << 1
csmOpacityDidChange = 1 << 2
csmDrawOrderDidChange = 1 << 3
csmRenderOrderDidChange = 1 << 4
csmVertexPositionsDidChange = 1 << 5
csmBlendColorDidChange = 1 << 6

csmFlags = ctypes.c_ubyte
"""
Live2D模型的属性标记。
源代码如下:
```c++
typedef unsigned char csmFlags;
```
"""

csmMocVersion_Unknown = 0
csmMocVersion_30 = 1
csmMocVersion_33 = 2
csmMocVersion_40 = 3
csmMocVersion_42 = 4
csmMocVersion_50 = 5

csmMocVersion = ctypes.c_uint
"""
Live2D模型文件的版本号。
源代码如下:
```c++
typedef unsigned int csmMocVersion;
```
"""
csmParameterType_Normal = 0
csmParameterType_BlendShape = 1

csmParameterType = ctypes.c_int
"""
Live2D模型参数类型。
源代码如下:
```c++
typedef int csmParameterType;
```
"""

class csmVector2(ctypes.Structure):
    """
    二维向量类型。
    源代码如下:
    ```c++
    typedef struct csmVector2 {
        float x;
        float y;
    } csmVector2;
    ```
    """
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float)
    ]

    def __str__(self) -> str:
        return f"csmVector2(x={self.x}, y={self.y})"
    
class csmVector4(ctypes.Structure):
    """
    四维向量类型。
    源代码如下:
    ```c++
    typedef struct csmVector4 {
        float x;
        float y;
        float z;
        float w;
    } csmVector4;
    ```
    """
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('w', ctypes.c_float)
    ]

    def __str__(self) -> str:
        return f"csmVector4(x={self.x}, y={self.y}, z={self.z}, w={self.w})"
    
"""
日志输出函数类型。
源代码如下:
```c++
typedef void (*csmLogFunction)(const char* message);
```
"""

"""
#if CSM_CORE_WIN32_DLL
#define csmCallingConvention __stdcall
#else
#define csmCallingConvention
#endif
"""
if sys.platform == 'win32':
    csmCallingConvention = ctypes.WINFUNCTYPE
else:
    csmCallingConvention = ctypes.CFUNCTYPE

csmLogFunction = csmCallingConvention(None, ctypes.c_char_p)
"""
日志输出函数类型。
源代码如下:
```c++
typedef void (*csmLogFunction)(const char* message);
```
"""