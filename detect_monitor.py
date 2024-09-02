import ctypes
from ctypes import windll, Structure, byref, POINTER

# Constants and structures
MONITORINFOF_PRIMARY = 1

class RECT(Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

class MONITORINFOEX(Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", ctypes.c_ulong),
                ("szDevice", ctypes.c_wchar * 32)]

def enum_display_monitors():
    hmonitors = []

    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitor_info = MONITORINFOEX()
        monitor_info.cbSize = ctypes.sizeof(MONITORINFOEX)
        windll.user32.GetMonitorInfoW(hMonitor, byref(monitor_info))
        
        monitor = {
            "monitor_index": None,  # We'll assign this later
            "left": monitor_info.rcMonitor.left,
            "top": monitor_info.rcMonitor.top,
            "right": monitor_info.rcMonitor.right,
            "bottom": monitor_info.rcMonitor.bottom,
            "is_primary": bool(monitor_info.dwFlags & MONITORINFOF_PRIMARY),
            "device_name": monitor_info.szDevice
        }
        
        hmonitors.append(monitor)
        return True

    MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, POINTER(RECT), ctypes.c_double)
    windll.user32.EnumDisplayMonitors(0, 0, MonitorEnumProc(monitor_enum_proc), 0)
    
    # Adjust indices after enumeration
    for idx, monitor in enumerate(hmonitors):
        if monitor["is_primary"]:
            monitor["monitor_index"] = 0
        else:
            monitor["monitor_index"] = idx + 1 if idx != 0 else 1

    return hmonitors

# Get monitor information
monitors = enum_display_monitors()
# for monitor in monitors:
#     print(f"Monitor {monitor['monitor_index']}: {monitor['device_name']} - Primary: {monitor['is_primary']}")
print(monitors)
