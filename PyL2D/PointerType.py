
import ctypes
from typing import Type
from ctypes import POINTER
from .l2dData import (
    csmParameterType,
    csmMoc,
    csmModel,
    csmVector2,
    csmVector4,
    csmFlags
)

IntPtr = Type[POINTER(ctypes.c_int)]
IntPtrPtr = Type[POINTER(POINTER(ctypes.c_int))]
CharPtr = ctypes.c_char_p
CharPtrPtr = Type[POINTER(ctypes.c_char_p)]
csmParameterTypePtr = Type[POINTER(csmParameterType)]
csmMocPtr = Type[POINTER(csmMoc)]
csmModelPtr = Type[POINTER(csmModel)]
csmVector2Ptr = Type[POINTER(csmVector2)]
csmVector2PtrPtr = Type[POINTER(POINTER(csmVector2))]
floatPtr = Type[POINTER(ctypes.c_float)]
floatPtrPtr = Type[POINTER(POINTER(ctypes.c_float))]
csmFlagsPtr = Type[POINTER(csmFlags)]
uShortPtr = Type[POINTER(ctypes.c_ushort)]
uShortPtrPtr = Type[POINTER(POINTER(ctypes.c_ushort))]
csmVector4Ptr = Type[POINTER(csmVector4)]
csmVector4PtrPtr = Type[POINTER(POINTER(csmVector4))]