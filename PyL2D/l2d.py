""" Wrapper for the Live2D Cubism Core dll. """

import ctypes
from pathlib import Path
from .PointerType import (
    CharPtrPtr,
    csmParameterTypePtr,
    csmMocPtr,
    csmModelPtr,
    csmVector2Ptr,
    csmVector2PtrPtr,
    floatPtr,
    floatPtrPtr,
    csmFlagsPtr,
    uShortPtrPtr,
    csmVector4Ptr,
    IntPtr,
    IntPtrPtr
)
from .l2dData import (
    csmVersion,
    csmMocVersion,
    csmLogFunction,
    csmMoc,
    csmModel,
    csmVector2,
    csmVector4,
    csmParameterType,
    csmFlags
)

l2d_path = Path(__file__).parent / "bin" / "Live2DCubismCore.dll"

class Live2DCubismCore:
    """ Wrapper for the Live2D Cubism Core dll. """
    def __init__(self, dll_path: Path = l2d_path):
        self.dll = ctypes.CDLL(str(dll_path if dll_path not in (None, '') else l2d_path) ,use_errno=True, use_last_error=True)

    def _define_function(self, name, restype, argtypes=[]):
        func = getattr(self.dll, name)
        func.restype = restype
        func.argtypes = argtypes
        return func
    
    def call_func(self, name: str, restype, argtypes, *args):
        """ Call a function from the dll. """
        func = self._define_function(name, restype, argtypes)
        return func(*args)

    def csmGetVersion(self) -> csmVersion:
        """ Get the version of the Live2D Cubism Core dll. """
        return self.call_func("csmGetVersion", csmVersion, [])
    
    def csmGetLatestMocVersion(self) -> csmMocVersion:
        """ Get the latest version of the moc file format. """
        return self.call_func("csmGetLatestMocVersion", csmMocVersion, [])
    
    def csmGetMocVersion(self, address: int, size: int) -> csmMocVersion:
        """ Get the version of the moc file at the given address. """
        return self.call_func("csmGetMocVersion", csmMocVersion, [ctypes.c_void_p, ctypes.c_uint], address, size)
    
    def csmHasMocConsistency(self, address: int, size: int) -> ctypes.c_int:
        """
        - address:  Address of unrevived moc. The address must be aligned to 'csmAlignofMoc'.
        - size:     Size of moc (in bytes).
        - return: '1' if Moc is valid; '0' otherwise.
        """
        return self.call_func("csmHasMocConsistency", ctypes.c_int, [ctypes.c_void_p, ctypes.c_uint], address, size)
    
    def csmGetLogFunction(self) -> csmLogFunction: # type: ignore
        """ Get the log function of the Live2D Cubism Core dll. """
        return self.call_func("csmGetLogFunction", csmLogFunction, [])
    
    def csmSetLogFunction(self, log_function: csmLogFunction) -> None:  # type: ignore
        """ Set the log function of the Live2D Cubism Core dll. """
        self.call_func("csmSetLogFunction", None, [csmLogFunction], log_function)

    def csmReviveMocInPlace(self, address: int, size: int) -> csmMocPtr:
        """
        - address:  Address of unrevived moc. The address must be aligned to 'csmAlignofMoc'.
        - size:     Size of moc (in bytes).
        - return: '1' if Moc is revived successfully; '0' otherwise.
        """
        return self.call_func("csmReviveMocInPlace", ctypes.POINTER(csmMoc), [ctypes.c_void_p, ctypes.c_uint], address, size)    
    
    def csmGetSizeofModel(self, moc: csmMoc) -> ctypes.c_uint:
        """ Get the size of the model in bytes. """
        return self.call_func("csmGetSizeofModel", ctypes.c_uint, [ctypes.POINTER(csmMoc)], moc)
    
    def csmInitializeModelInPlace(self, moc: csmMocPtr, address: int, size: int) -> csmModelPtr:
        """
        Tries to instantiate a model in place.
        - moc: Sources moc.
        - address: Address to place instance at. Address must be aligned to 'csmAlignofModel'.
        - size: Size of instance (in bytes).
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmInitializeModelInPlace", ctypes.POINTER(csmModel), [ctypes.POINTER(csmMoc), ctypes.c_void_p, ctypes.c_uint], moc, address, size)
    
    def csmUpdateModel(self, model: csmModelPtr) -> None:
        """
        Updates the model.
        - model: Model to update.
        """
        return self.call_func("csmUpdateModel", None, [ctypes.POINTER(csmModel)], model)
    
    def csmReadCanvasInfo(self, model: csmModelPtr, outSizeInPixels: csmVector2Ptr, outOriginInPixels: csmVector2Ptr, outPixelsPerUnit: float) -> None:
        """
        Reads the canvas information from the model.
        - model: Model to read from.
        - outSizeInPixels: Output parameter for the size of the canvas in pixels.
        - outOriginInPixels: Output parameter for the origin of the canvas in pixels.
        """
        self.call_func("csmReadCanvasInfo", None, [ctypes.POINTER(csmModel), ctypes.POINTER(csmVector2), ctypes.POINTER(csmVector2), ctypes.POINTER(ctypes.c_float)], model, outSizeInPixels, outOriginInPixels, outPixelsPerUnit)

    def csmGetParameterCount(self, model: csmModelPtr) -> ctypes.c_int:
        """
        Gets the number of parameters in the model. 
        - model: Model to query.
        - return: Valid count on success; '-1' otherwise.
        """
        return self.call_func("csmGetParameterCount", ctypes.c_int, [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterIds(self, model: csmModelPtr) -> CharPtrPtr:
        """
        Gets parameter IDs.
        All IDs are null-terminated ANSI strings.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterIds", ctypes.POINTER(ctypes.c_char_p), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterTypes(self, model: csmModelPtr) -> csmParameterTypePtr:
        """
        Gets parameter types.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterTypes", ctypes.POINTER(csmParameterType), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterMinimumValues(self, model: csmModelPtr) -> floatPtr:
        """
        Gets parameter minimum values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterMinimumValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterMaximumValues(self, model: csmModelPtr) -> floatPtr:
        """
        Gets parameter maximum values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterMaximumValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterDefaultValues(self, model: csmModelPtr) -> floatPtr:
        """
        Gets parameter default values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterDefaultValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterValues(self, model: csmModelPtr) -> floatPtr:
        """
        Gets parameter values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterKeyCounts(self, model: csmModelPtr) -> IntPtr:
        """
        Gets parameter key counts.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterKeyCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterKeyValues(self, model: csmModelPtr) -> floatPtrPtr:
        """
        Gets parameter key values.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterKeyValues", ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartCount(self, model: csmModelPtr) -> ctypes.c_int:
        """
        Gets the number of parts in the model.
        - model: Model to query.
        - return: Valid count on success; '-1' otherwise.
        """
        return self.call_func("csmGetPartCount", ctypes.c_int, [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartIds(self, model: csmModelPtr) -> CharPtrPtr:
        """
        Gets part IDs.
        All IDs are null-terminated ANSI strings.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetPartIds", ctypes.POINTER(ctypes.c_char_p), [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartOpacities(self, model: csmModelPtr) -> floatPtr:
        """
        Gets part opacities.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetPartOpacities", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartParentPartIndices(self, model: csmModelPtr) -> IntPtr:
        """
        Gets part parent part indices.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetPartParentPartIndices", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableCount(self, model: csmModelPtr) -> ctypes.c_int:
        """
        Gets the number of drawable(s) in the model.
        - model: Model to query.
        - return: Valid count on success; '-1' otherwise.
        """
        return self.call_func("csmGetDrawableCount", ctypes.c_int, [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableIds(self, model: csmModelPtr) -> CharPtrPtr:
        """
        Gets drawable IDs.
        All IDs are null-terminated ANSI strings.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableIds", ctypes.POINTER(ctypes.c_char_p), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableConstantFlags(self, model: csmModelPtr) -> csmFlagsPtr:
        """
        Gets constant drawable flags.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableConstantFlags", ctypes.POINTER(csmFlags), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableDynamicFlags(self, model: csmModelPtr) -> csmFlagsPtr:
        """
        Gets dynamic drawable flags.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableDynamicFlags", ctypes.POINTER(csmFlags), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableTextureIndices(self, model: csmModelPtr) -> IntPtr:
        """
        Gets drawable texture indices.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableTextureIndices", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableDrawOrders(self, model: csmModelPtr) -> IntPtr:
        """
        Gets drawable draw orders.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableDrawOrders", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableRenderOrders(self, model: csmModelPtr) -> IntPtr:
        """
        Gets drawable render orders.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableRenderOrders", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableOpacities(self, model: csmModelPtr) -> floatPtr:
        """
        Gets drawable opacities.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableOpacities", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableMaskCounts(self, model: csmModelPtr) -> IntPtr:
        """
        Gets the number of masks for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableMaskCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableMasks(self, model: csmModelPtr) -> IntPtrPtr:
        """
        Gets the masks for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableMasks", ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableVertexCounts(self, model: csmModelPtr) -> IntPtr:
        """
        Gets the number of vertices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableVertexCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableVertexPositions(self, model: csmModelPtr) -> csmVector2PtrPtr:
        """
        Gets the vertex positions for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableVertexPositions", ctypes.POINTER(ctypes.POINTER(csmVector2)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableVertexUvs(self, model: csmModelPtr) -> csmVector2PtrPtr:
        """
        Gets the vertex UVs for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableVertexUvs", ctypes.POINTER(ctypes.POINTER(csmVector2)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableIndexCounts(self, model: csmModelPtr) -> IntPtr:
        """
        Gets the number of indices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableIndexCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableIndices(self, model: csmModelPtr) -> uShortPtrPtr:
        """
        Gets the indices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableIndices", ctypes.POINTER(ctypes.POINTER(ctypes.c_ushort)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableMultiplyColors(self, model: csmModelPtr) -> csmVector4Ptr:
        """
        Gets the multiply colors for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableMultiplyColors", ctypes.POINTER(csmVector4), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableScreenColors(self, model: csmModelPtr) -> csmVector4Ptr:
        """
        Gets the screen colors for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableScreenColors", ctypes.POINTER(csmVector4), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableParentPartIndices(self, model: csmModelPtr) -> IntPtr:
        """
        Gets the parent part indices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableParentPartIndices", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmResetDrawableDynamicFlags(self, model: csmModelPtr) -> None:
        """
        Resets the dynamic flags for all drawable(s).
        - model: Model to modify.
        - return: None.
        """
        self.call_func("csmResetDrawableDynamicFlags", None, [ctypes.POINTER(csmModel)], model)

    def get_error(self) -> str:
        """
        Gets the last error message.
        - return: Error message.
        """
        err_code = ctypes.get_last_error()
        err_msg = ctypes.FormatError(err_code)
        err = f"[{err_code}]: {err_msg}"
        return err
    
# example usage:
if __name__ == "__main__":
    l2d = Live2DCubismCore()
    print(l2d.csmReviveMocInPlace(1, 2))
    print(l2d.get_error())