import ctypes

# 定义必要的数据结构和常量
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

class MONITORINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_long),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", ctypes.c_long)]

MONITORINFOF_PRIMARY = 1

MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)

def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
    # 获取显示器信息
    monitor_info = MONITORINFO()
    monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
    ctypes.windll.user32.GetMonitorInfoA(hMonitor, ctypes.byref(monitor_info))

    # 获取显示器的坐标
    r = lprcMonitor.contents
    left = r.left
    top = r.top
    right = r.right
    bottom = r.bottom

    # 判断是否为主显示器
    is_primary = bool(monitor_info.dwFlags & MONITORINFOF_PRIMARY)
    
    # 添加显示器信息到列表
    if is_primary:
        primary_resolutions.append({
            "monitor_index": 0,  # 主显示器为 0
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
            "is_prime": True  # 标记为主显示器
        })
    else:
        secondary_resolutions.append({
            "monitor_index": len(secondary_resolutions) + 1,  # 副显示器从 1 开始
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
            "is_prime": False  # 标记为非主显示器
        })
    
    return 1

def get_all_monitors_resolutions():
    global primary_resolutions, secondary_resolutions
    primary_resolutions = []
    secondary_resolutions = []
    
    # 调用 SetProcessDPIAware 或 SetProcessDpiAwareness 来禁用 DPI 缩放
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Windows 8.1 and later
    except AttributeError:
        ctypes.windll.user32.SetProcessDPIAware()  # Windows Vista and later
    
    user32 = ctypes.windll.user32
    user32.EnumDisplayMonitors(None, None, MonitorEnumProc(monitor_enum_proc), 0)
    
    # 返回所有显示器信息
    return primary_resolutions + secondary_resolutions

# 获取并返回所有显示器的分辨率和坐标
all_monitors = get_all_monitors_resolutions()

# # 打印结果
# for monitor_info in all_monitors:
#     print(monitor_info['monitor_index'])
#     print(monitor_info['left'])
