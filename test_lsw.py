import ctypes
import time

import logitech_steering_wheel as lsw
import pygetwindow as gw


DEVICE_NUM = 1

if __name__ == '__main__':
    # w = gw.getActiveWindow()._hWnd


    #  This code doesn't seem to work in an active command line window



    w = gw.getActiveWindow()
    print(gw.getActiveWindowTitle())
    print(w)
    initialized = lsw.initialize_with_window(True, w._hWnd)
    # initialized = lsw.initialize(True)

    print("SDK version is: " + str(lsw.get_sdk_version()))

    if initialized:
        print('initialized successfully')
    else:
        exit()

    if lsw.is_connected(DEVICE_NUM):
        print(f'connected to a steering wheel at index {DEVICE_NUM}')
    else:
        print('Connection failed')
        exit()

    lsw.update()
    print(lsw.get_current_controller_properties(DEVICE_NUM))
    
    for i in range(20):
        lsw.update()
        s = lsw.get_state(DEVICE_NUM)
        print(s.lX)
        time.sleep(.5)

    lsw.play_bumpy_road_effect(DEVICE_NUM, 20)
    time.sleep(2)
    lsw.stop_bumpy_road_effect(DEVICE_NUM)

    lsw.shutdown()
    exit()


