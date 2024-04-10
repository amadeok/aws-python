import subprocess
import threading
import time
import tkinter as tk
from tkinter import filedialog

def get_field_current(obj, path):
    keys = path.split('.')
    current = obj

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    last_key = keys[-1]
    return current, last_key

def check_type(current):
    if not isinstance(current, list):
        raise ValueError('The specified path does not point to an array.')

def update_nested_field(obj, path, index, field, value):
    current, last_key = get_field_current(obj, path)

    if field is None:
        if index is None:
            current[last_key] = value
        else:
            check_type(current[last_key])
            current[last_key][index] = value
    else:
        if index is None:
            current[last_key][field] = value
        else:
            check_type(current)
            current[last_key][index][field] = value

def add_to_field(obj, path, field, value):
    current = get_field_current(obj, path)
    check_type(current)

    if field is None:
        current.append(value)
    else:
        current[field].append( value)
    
def delete_field(obj, path, field, index):
    current = get_field_current(obj, path)
    check_type(current)

    if field is None:
        del current[index]
    else:
        del current[field][index]

    
def find_element_by_id(array, target_id):
    return next((element for element in array if element.get('_id') == target_id), None)


def merge_arrays(arr1, arr2, arr1_field_name, arr2_field_name):
    # Create a dictionary with _id as keys and corresponding objects from arr2 as values
    id_dict = {}
    for obj in arr2:
        _id = obj[arr2_field_name] #'track_entry_id'
        if _id not in id_dict:
            id_dict[_id] = []
        id_dict[_id].append(obj)

    # Merge arr1 and arr2
    for obj in arr1:
        _id = obj[arr2_field_name]
        if _id in id_dict:
            obj[arr1_field_name] = id_dict[_id]
        else:
            obj[arr1_field_name] = []

    return arr1


def check_field_presence(dict1, dict2, field1, field2):
    values_dict1 = set(dict1[field1])
    values_dict2 = [item[field2] for item in dict2]

    for value in values_dict1:
        if value in values_dict2:
            return True
    return False


import pygetwindow as gw
import win32gui

def open_file_dialog_old():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    stop = False
    h = 0
    time.sleep(0.5)
    def task():
        sl = 0.1
        while not stop:
            time.sleep(sl)
            wins = gw.getWindowsWithTitle("Open")
            if len(wins):
                try: 
                    win32gui.SetForegroundWindow(wins[0]._hWnd)
                except Exception as e: print(e)
            sl = 1
            
    t = threading.Thread(target=task)
    t.start()
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected file:", file_path)
    else:
        print("No file selected.")
    stop = True
    t.join()
    
def open_file_dialog():

    process = subprocess.Popen(['python', 'file_dialog.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stdout:
        ret = stdout.decode()
        ret2 = ret.split("|")
        if len(ret2) > 1:
            file = ret2[1].replace("\n", "").replace("\r", "")
            print("Selected file: ", file)
            return file
        else: return None
        
    if stderr:
        print("Error:")
        print(stderr.decode())


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

# print(obj)
gw.getAllTitles