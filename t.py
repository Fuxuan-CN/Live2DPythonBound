from PyL2D.l2d import Live2DCubismCore
from PyL2D.l2dData import csmVector2
from ctypes import c_void_p, c_float
from pathlib import Path
import numpy as np

class Live2DModel:
    """高级接口，封装Live2D模型的操作。"""

    def __init__(self, dll_path: Path = None):
        """
        初始化Live2D模型。
        :param dll_path: Live2D Cubism Core DLL的路径。
        """
        self.core = Live2DCubismCore(dll_path)
        self.moc = None
        self.model = None
        self.parameter_count = 0
        self.part_count = 0
        self.drawable_count = 0

    def load_moc(self, moc_data: bytes) -> bool:
        """
        加载Moc文件数据。
        :param moc_data: Moc文件的二进制数据。
        :return: 是否加载成功。
        """
        address = c_void_p.from_buffer_copy(moc_data)
        size = len(moc_data)
        if not self.core.csmHasMocConsistency(address, size):
            raise ValueError("Moc data is inconsistent or invalid.")
        
        self.moc = self.core.csmReviveMocInPlace(address, size)
        if not self.moc:
            raise RuntimeError("Failed to revive Moc.")
        return True

    def initialize_model(self, buffer_size: int) -> bool:
        """
        初始化模型。
        :param buffer_size: 模型缓冲区的大小。
        :return: 是否初始化成功。
        """
        if not self.moc:
            raise RuntimeError("Moc must be loaded before initializing the model.")
        
        buffer = np.zeros(buffer_size, dtype=np.uint8)
        address = c_void_p(buffer.ctypes.data)
        self.model = self.core.csmInitializeModelInPlace(self.moc, address, buffer_size)
        if not self.model:
            raise RuntimeError("Failed to initialize model.")
        
        self.parameter_count = self.core.csmGetParameterCount(self.model)
        self.part_count = self.core.csmGetPartCount(self.model)
        self.drawable_count = self.core.csmGetDrawableCount(self.model)
        return True

    def update(self):
        """
        更新模型状态。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before updating.")
        self.core.csmUpdateModel(self.model)

    def get_parameter_ids(self) -> list:
        """
        获取所有参数的ID。
        :return: 参数ID列表。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before getting parameter IDs.")
        ids_ptr = self.core.csmGetParameterIds(self.model)
        return [ids_ptr[i].decode('utf-8') for i in range(self.parameter_count)]

    def get_parameter_values(self) -> list:
        """
        获取所有参数的值。
        :return: 参数值列表。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before getting parameter values.")
        values_ptr = self.core.csmGetParameterValues(self.model)
        return [values_ptr[i] for i in range(self.parameter_count)]

    def set_parameter_value(self, parameter_id: str, value: float):
        """
        设置指定参数的值。
        :param parameter_id: 参数ID。
        :param value: 参数值。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before setting parameter values.")
        ids = self.get_parameter_ids()
        if parameter_id not in ids:
            raise ValueError(f"Parameter ID '{parameter_id}' not found.")
        index = ids.index(parameter_id)
        values_ptr = self.core.csmGetParameterValues(self.model)
        values_ptr[index] = value

    def get_canvas_info(self) -> dict:
        """
        获取画布信息。
        :return: 包含画布大小、原点和像素每单位信息的字典。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before getting canvas info.")
        size = csmVector2()
        origin = csmVector2()
        pixels_per_unit = c_float()
        self.core.csmReadCanvasInfo(self.model, size, origin, pixels_per_unit)
        return {
            "size": (size.x, size.y),
            "origin": (origin.x, origin.y),
            "pixels_per_unit": pixels_per_unit.value
        }

    def get_drawable_opacities(self) -> list:
        """
        获取所有可绘制对象的不透明度。
        :return: 不透明度列表。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before getting drawable opacities.")
        opacities_ptr = self.core.csmGetDrawableOpacities(self.model)
        return [opacities_ptr[i] for i in range(self.drawable_count)]

    def reset_dynamic_flags(self):
        """
        重置所有可绘制对象的动态标志。
        """
        if not self.model:
            raise RuntimeError("Model must be initialized before resetting dynamic flags.")
        self.core.csmResetDrawableDynamicFlags(self.model)

    def get_error(self) -> str:
        """
        获取最后一个错误信息。
        :return: 错误信息。
        """
        return self.core.get_error()
    
if __name__ == '__main__':
    model = Live2DModel()
    with open(r'符玄\符玄.moc3', 'rb') as f:
        moc_data = f.read()
    model.load_moc(moc_data)
    model.initialize_model(1024 * 1024)  