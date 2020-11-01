import numpy as np
import psutil
try:
    from ctypes import windll

    import win32gui
    import win32ui
except Exception as e:
    print("now windows :(")


def get_process_by_name(name):
    processes = psutil.process_iter()
    for p in processes:
        try:
            process_name = p.name()
            pid = p.pid
            if process_name == name:
                return p
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def get_screenshot(hwnd):
    # hwnd = win32gui.FindWindow(None, windowname)
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(dcObj, w, h)

    cDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, cDC.GetSafeHdc(), 0)
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    bmpinfo = saveBitMap.GetInfo()

    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())

    # cv2.IMREAD_COLOR in OpenCV 3.1
    img = img[..., :3]

    img = np.ascontiguousarray(img)

    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109

    return img
