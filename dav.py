import os
from pprint import pprint

# #os.system("echo %PYTHONPATH%")

# #os.system('set  RESOLVE_SCRIPT_API="' + os.getenv('PROGRAMDATA') + '\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting')

# # os.environ['RESOLVE_SCRIPT_API'] = os.getenv('PROGRAMDATA') + '\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting'

#os.environ['PYTHONPATH']=r"C:\Users\amade\AppData\Local\Programs\Python\Python310"
#os.environ['PYTHONPATH']=os.getenv('PYTHONPATH') +';' + os.getenv('RESOLVE_SCRIPT_API') + '\\Modules\\'



# # #os.environ['PYTHONPATH']= os.getenv('RESOLVE_SCRIPT_API') + '\\Modules\\'

print("RESOLVE_SCRIPT_API")
os.system("echo %RESOLVE_SCRIPT_API%")
print("RESOLVE_SCRIPT_LIB")
os.system("echo %RESOLVE_SCRIPT_LIB%")
print("PYTHONPATH")
os.system("echo %PYTHONPATH%")

import DaVinciResolveScript as dvr_script
resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()
#if __name__ == "__main__":
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()
rootFolder = mediaPool.GetRootFolder()
clips = rootFolder.GetClipList()


from pprint import pprint





timeline = project.GetCurrentTimeline()
if not timeline:
    if project.GetTimelineCount() > 0:
        timeline = project.GetTimelineByIndex(1)
        project.SetCurrentTimeline(timeline)

if not timeline:
    print("Current project has no timelines")
    sys.exit()

#timeline.InsertFusionCompositionIntoTimeline()
#timeline.InsertFusionGeneratorIntoTimeline()




for clip in clips:
    print(type(clip))
    p = clip.GetClipProperty()
    print(p)
    if clip.GetClipProperty()["Video Codec"] != "" or 1:
        subClip = {
            "mediaPoolItem": clip,
            "startFrame": 50,
            "endFrame": 73,
        }

        if mediaPool.AppendToTimeline([ subClip ]):
            print("added subclip (first 24 frames) of \"" + clip.GetName() + "\" to current timeline.")










# #print(os.getenv('RESOLVE_SCRIPT_API'))

# import win32gui
# import win32con
# import pygetwindow as gw
# import time, shutil

# time.sleep(1)
# def send_page_down(handle, param):
#     if win32gui.GetClassName(handle) == param or 1:
#         win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
#         win32gui.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_UP, 0)

# G = gw.getWindowsWithTitle("Avee Player")
# G[0].moveTo(0, 0)
# window_id = win32gui.FindWindow(None, "Avee Player")
# win32gui.EnumChildWindows(window_id, send_page_down, 'FoxitDocWnd')


# from pywinauto.application import Application
# #a = "notepad.exe"
# import time
# import pywinauto, ctypes

# print(gw.getActiveWindowTitle())

# script_path= r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Comp\scr.py"
# src_path = r"F:\all\GitHub\aws-python\dav_src.py"

# with open (src_path, "r") as inp:
#     with open (script_path, "w") as out:
#         d = inp.read()
#         out.write(d)
# title = "DaVinci Resolve - Untitled Project"
# title2 = "DaVinci Resolve - new proj"
# app = None
# try:
#     app = pywinauto.Application(backend="win32").connect(title=title)
# except:
#     app=  pywinauto.Application(backend="win32").connect(title=title2)


# #time.sleep(1)
# # G = gw.getWindowsWithTitle(title)[0]
# # hwnd = G._hWnd


# #shutil.copyfile(src_path, script_path )
# print(app.windows())
# print('sleeping over')
# #Wizard = app[G.title]
# Wiz = app["Qt5152QWindow"] #Qt5152QWindowOwnDCIcon
# wiz2 = app["Qt5152QWindowIcon"]

# wiz2.send_keystrokes("{VK_F4}")

# console_hwnd = win32gui.FindWindow(None, "Resolve")
# console_app =  pywinauto.Application(backend="win32").connect(handle=console_hwnd)
# print("\n\n\n")
# print(console_app.windows())
# for w in console_app.windows():
#     if w.handle == console_hwnd:
#         w.send_keystrokes("{VK_F3}")
#         print()
#     pass

# while True:
#    # n = app.window(best_match='Blocco note',  top_level_only=False)
# #    n.send_keystrokes("97")
#     #Wizard.send_keystrokes("97")
#     #Wiz.send_keystrokes("H")#{VK_F3}")
#     for w in app.windows():
#         if w.friendlyclassname == "Qt5152QWindowIcon" or w.friendlyclassname == "Qt5152QWindow":
#             w.send_keystrokes("H")
#             print(w)
#         # w.send_keystrokes("{VK_F3}")
#         # try:
#         #     w.send_keys("{VK_SHIFT down}"
#         #   "pywinauto"
#         #   "{VK_SHIFT up}") 
#         #     print("wrote")
#         # except Exception as e:
#         #     print(e)


#    # Wizard.send_keystrokes("{VK_RIGHT}")
#         time.sleep(0.5)