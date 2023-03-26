import os

#os.system("echo %PYTHONPATH%")

#os.system('set  RESOLVE_SCRIPT_API="' + os.getenv('PROGRAMDATA') + '\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting')

# os.environ['RESOLVE_SCRIPT_API'] = os.getenv('PROGRAMDATA') + '\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting'

os.environ['PYTHONPATH']=os.getenv('PYTHONPATH') +';' + os.getenv('RESOLVE_SCRIPT_API') + '\\Modules\\'
# #os.environ['PYTHONPATH']= os.getenv('RESOLVE_SCRIPT_API') + '\\Modules\\'

# print("RESOLVE_SCRIPT_API")
os.system("echo %RESOLVE_SCRIPT_API%")
# print("RESOLVE_SCRIPT_LIB")
os.system("echo %RESOLVE_SCRIPT_LIB%")
# print("PYTHONPATH")
os.system("echo %PYTHONPATH%")

#print(os.getenv('RESOLVE_SCRIPT_API'))

import win32gui
import win32con
import pygetwindow as gw
import time

# time.sleep(1)
# def send_page_down(handle, param):
#     if win32gui.GetClassName(handle) == param or 1:
#         win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
#         win32gui.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_UP, 0)

# G = gw.getWindowsWithTitle("Avee Player")
# G[0].moveTo(0, 0)
# window_id = win32gui.FindWindow(None, "Avee Player")
# win32gui.EnumChildWindows(window_id, send_page_down, 'FoxitDocWnd')


from pywinauto.application import Application
a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"
#a = "notepad.exe"
import time
import pywinauto, ctypes

print(gw.getActiveWindowTitle())
title = "DaVinci Resolve - Untitled Project"
app = pywinauto.Application(backend="win32").connect(title=title)

time.sleep(1)
G = gw.getWindowsWithTitle(title)[0]
hwnd = G._hWnd

print(app.windows())
print('sleeping over')
Wizard = app[G.title]
Wizard = app["Qt5152QWindow"] #Qt5152QWindowOwnDCIcon
while True:
   # n = app.window(best_match='Blocco note',  top_level_only=False)
#    n.send_keystrokes("97")
    #Wizard.send_keystrokes("97")
    #Wizard.send_keystrokes("{VK_F3}")
    for w in app.windows():
        Wizard.send_keystrokes("{VK_F3}")
        print(w)
        #w.send_keystrokes("{VK_F3}")
        # try:
        #     w.send_keys("{VK_SHIFT down}"
        #   "pywinauto"
        #   "{VK_SHIFT up}") 
        #     print("wrote")
        # except Exception as e:
        #     print(e)


   # Wizard.send_keystrokes("{VK_RIGHT}")
        time.sleep(0.5)