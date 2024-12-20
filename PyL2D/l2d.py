""" Wrapper for the Live2D Cubism Core dll. """

import ctypes
from pathlib import Path
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
        self.dll = ctypes.CDLL(str(dll_path),use_errno=True, use_last_error=True)

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
    
    def csmHasMocConsistency(self, address: int, size: int) -> bool:
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

    def csmReviveMocInPlace(self, address: int, size: int) -> csmMoc:
        """
        - address:  Address of unrevived moc. The address must be aligned to 'csmAlignofMoc'.
        - size:     Size of moc (in bytes).
        - return: '1' if Moc is revived successfully; '0' otherwise.
        """
        return self.call_func("csmReviveMocInPlace", ctypes.POINTER(csmMoc), [ctypes.c_void_p, ctypes.c_uint], address, size)    
    
    def csmGetSizeofModel(self, moc: csmMoc) -> int:
        """ Get the size of the model in bytes. """
        return self.call_func("csmGetSizeofModel", ctypes.c_uint, [ctypes.POINTER(csmMoc)], moc)
    
    def csmInitializeModelInPlace(self, moc: csmMoc, address: int, size: int) -> csmModel:
        """
        Tries to instantiate a model in place.
        - moc: Sources moc.
        - address: Address to place instance at. Address must be aligned to 'csmAlignofModel'.
        - size: Size of instance (in bytes).
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmInitializeModelInPlace", ctypes.POINTER(csmModel), [ctypes.POINTER(csmMoc), ctypes.c_void_p, ctypes.c_uint], moc, address, size)
    
    def csmUpdateModel(self, model: csmModel) -> None:
        """
        Updates the model.
        - model: Model to update.
        """
        return self.call_func("csmUpdateModel", None, [ctypes.POINTER(csmModel)], model)
    
    def csmReadCanvasInfo(self, model: csmModel, outSizeInPixels: csmVector2, outOriginInPixels: csmVector2, outPixelsPerUnit: float) -> None:
        """
        Reads the canvas information from the model.
        - model: Model to read from.
        - outSizeInPixels: Output parameter for the size of the canvas in pixels.
        - outOriginInPixels: Output parameter for the origin of the canvas in pixels.
        """
        self.call_func("csmReadCanvasInfo", None, [ctypes.POINTER(csmModel), ctypes.POINTER(csmVector2), ctypes.POINTER(csmVector2), ctypes.POINTER(ctypes.c_float)], model, outSizeInPixels, outOriginInPixels, outPixelsPerUnit)

    def csmGetParameterCount(self, model: csmModel) -> int:
        """
        Gets the number of parameters in the model. 
        - model: Model to query.
        - return: Valid count on success; '-1' otherwise.
        """
        return self.call_func("csmGetParameterCount", ctypes.c_int, [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterIds(self, model: csmModel) -> str:
        """
        Gets parameter IDs.
        All IDs are null-terminated ANSI strings.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterIds", ctypes.POINTER(ctypes.c_char_p), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterTypes(self, model: csmModel) -> csmParameterType:
        """
        Gets parameter types.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterTypes", ctypes.POINTER(csmParameterType), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterMinimumValues(self, model: csmModel) -> float:
        """
        Gets parameter minimum values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterMinimumValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterMaximumValues(self, model: csmModel) -> float:
        """
        Gets parameter maximum values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterMaximumValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterDefaultValues(self, model: csmModel) -> float:
        """
        Gets parameter default values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterDefaultValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterValues(self, model: csmModel) -> float:
        """
        Gets parameter values.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterValues", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterKeyCounts(self, model: csmModel) -> int:
        """
        Gets parameter key counts.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterKeyCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetParameterKeyValues(self, model: csmModel) -> float:
        """
        Gets parameter key values.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetParameterKeyValues", ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartCount(self, model: csmModel) -> int:
        """
        Gets the number of parts in the model.
        - model: Model to query.
        - return: Valid count on success; '-1' otherwise.
        """
        return self.call_func("csmGetPartCount", ctypes.c_int, [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartIds(self, model: csmModel):
        """
        Gets part IDs.
        All IDs are null-terminated ANSI strings.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetPartIds", ctypes.POINTER(ctypes.c_char_p), [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartOpacities(self, model: csmModel) -> float:
        """
        Gets part opacities.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetPartOpacities", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetPartParentPartIndices(self, model: csmModel) -> int:
        """
        Gets part parent part indices.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetPartParentPartIndices", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableCount(self, model: csmModel) -> int:
        """
        Gets the number of drawables in the model.
        - model: Model to query.
        - return: Valid count on success; '-1' otherwise.
        """
        return self.call_func("csmGetDrawableCount", ctypes.c_int, [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableIds(self, model: csmModel):
        """
        Gets drawable IDs.
        All IDs are null-terminated ANSI strings.
        
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableIds", ctypes.POINTER(ctypes.c_char_p), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableConstantFlags(self, model: csmModel) -> csmFlags:
        """
        Gets constant drawable flags.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableConstantFlags", ctypes.POINTER(csmFlags), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableDynamicFlags(self, model: csmModel) -> csmFlags:
        """
        Gets dynamic drawable flags.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableDynamicFlags", ctypes.POINTER(csmFlags), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableTextureIndices(self, model: csmModel) -> int:
        """
        Gets drawable texture indices.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableTextureIndices", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableDrawOrders(self, model: csmModel) -> int:
        """
        Gets drawable draw orders.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableDrawOrders", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableRenderOrders(self, model: csmModel) -> int:
        """
        Gets drawable render orders.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableRenderOrders", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableOpacities(self, model: csmModel) -> float:
        """
        Gets drawable opacities.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableOpacities", ctypes.POINTER(ctypes.c_float), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableMaskCounts(self, model: csmModel) -> int:
        """
        Gets the number of masks for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableMaskCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableMasks(self, model: csmModel) -> int:
        """
        Gets the masks for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableMasks", ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableVertexCounts(self, model: csmModel) -> int:
        """
        Gets the number of vertices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableVertexCounts", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableVertexPositions(self, model: csmModel) -> csmVector2:
        """
        Gets the vertex positions for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableVertexPositions", ctypes.POINTER(ctypes.POINTER(csmVector2)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableVertexUvs(self, model: csmModel) -> csmVector2:
        """
        Gets the vertex UVs for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableVertexUvs", ctypes.POINTER(ctypes.POINTER(csmVector2)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableIndexCounts(self, model: csmModel) -> int:
        """
        Gets the number of indices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableIndexCounts", ctypes.pointer(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableIndices(self, model: csmModel) -> int:
        """
        Gets the indices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableIndices", ctypes.POINTER(ctypes.POINTER(ctypes.c_ushort)), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableMultiplyColors(self, model: csmModel) -> csmVector4:
        """
        Gets the multiply colors for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableMultiplyColors", ctypes.POINTER(csmVector4), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableScreenColors(self, model: csmModel) -> csmVector4:
        """
        Gets the screen colors for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableScreenColors", ctypes.POINTER(csmVector4), [ctypes.POINTER(csmModel)], model)
    
    def csmGetDrawableParentPartIndices(self, model: csmModel) -> int:
        """
        Gets the parent part indices for each drawable.
        - model: Model to query.
        - return: Valid pointer on success; '0' otherwise.
        """
        return self.call_func("csmGetDrawableParentPartIndices", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(csmModel)], model)
    
    def csmResetDrawableDynamicFlags(self, model: csmModel) -> None:
        """
        Resets the dynamic flags for all drawables.
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