from PyL2D.l2d import Live2DCubismCore
import ctypes

# 实例化 DLL 包装器
l2d = Live2DCubismCore()

# 加载 moc3 文件到内存中
with open(r'F:\python_play\FuxuanLive2d\l2dtest\符玄\符玄.moc3', 'rb') as f:
    moc_data = f.read()

# 将 MOC 文件数据复制到 ctypes 数组中
moc_array = (ctypes.c_byte * len(moc_data)).from_buffer_copy(moc_data)

# 获取 MOC 文件数据的指针
moc_array_ptr = ctypes.cast(moc_array, ctypes.c_void_p)

# 复活 MOC 文件
moc = l2d.csmReviveMocInPlace(moc_array_ptr, len(moc_data))
if not moc:
    print("MOC复活失败")
    exit()
else:
    print("MOC复活成功")

# 获取模型大小
model_size = l2d.csmGetSizeofModel(moc)
if model_size == 0:
    print("获取模型大小失败")
    exit()
else:
    print(f"模型大小为 {model_size} bytes")

# 初始化模型实例
model_address = (ctypes.c_char * model_size)()  # 创建一块内存空间，大小为 model_size
model = l2d.csmInitializeModelInPlace(moc, model_address, model_size)
if not model:
    print("模型初始化失败")
    exit()
else:
    print("模型初始化成功")

prameter = l2d.csmGetDrawableCount(model)
print(f"模型有 {prameter} 个可绘制参数")