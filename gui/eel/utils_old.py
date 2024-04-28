import logging
import subprocess
import threading
import time
import tkinter as tk
from tkinter import filedialog
import os, sys, eel




import pygetwindow as gw
# import win32gui

# def open_file_dialog_old():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window
#     stop = False
#     h = 0
#     time.sleep(0.5)
#     def task():
#         sl = 0.1
#         while not stop:
#             time.sleep(sl)
#             wins = gw.getWindowsWithTitle("Open")
#             if len(wins):
#                 try: 
#                     win32gui.SetForegroundWindow(wins[0]._hWnd)
#                 except Exception as e: logging.info(e)
#             sl = 1
            
#     t = threading.Thread(target=task)
#     t.start()
#     file_path = filedialog.askopenfilename()
#     if file_path:
#         logging.info(f"Selected file: {file_path}")
#     else:
#         logging.info("No file selected.")
#     stop = True
#     t.join()
#p = None


def start_node():
    
    #global p
    #os.system("start node %AppData%\\npm\\node_modules\\serve\\build\\main.js -s build") #putting this exact line in index.py cause huge pyinstaller file
    p = subprocess.Popen(["node", r"C:\Users\amade\AppData\Roaming\npm\node_modules\serve\build\main.js", "-s", "build" ]) 
    # def task():
    #     #global stop
    #     sl = 0.1
    #     while not stop:
    #         time.sleep(sl)

    #         sl = 1
    #     p.kill()
            
    # t = threading.Thread(target=task)
    # t.start()
    #return p





# obj = {
#     'a': {
#         'b': {
#             'c': [
#                 {'id': 1, 'name': 'Alice'},
#                 {'id': 2, 'name': 'Bob'},
#                 {'id': 3, 'name': 'Charlie'}
#             ],
#             'd': [
#                 "car", "shift", "boat"
#             ]
#         },
#         'e': "crack"
#     }
# }

# update_nested_field(obj, 'a.b.c', 1, 'name', 'Updated Bob')
# update_nested_field(obj, 'a.b.d', 2, None, 'Updated boat')
# update_nested_field(obj, 'a.e', None, None, 'Updated crack')

# logging.info(obj)
