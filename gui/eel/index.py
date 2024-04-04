# coding: utf-8
import sys, threading, time, os

from bson import ObjectId
from mongo import MongoDBClient
import utils
#sys.path.insert(1, r'F:\all\GitHub\Eel')
import eel
import mongo_schema

uri = os.getenv("MONGODB_URI")
mongo_client = MongoDBClient(uri, 'social-media-helper', 'track-tasks')

if hasattr(sys, "_MEIPASS"): # if the script is started from an executable file
    with open("logs.txt", "a") as f_logs:
        sys.stdout = f_logs
        sys.stderr = f_logs

entries = []

@eel.expose
def update_field(payload):
    update_task(payload, lambda: utils.update_nested_field(utils.find_element_by_id(entries, payload["_id"]), payload["path"], payload["index"], payload["field"], payload["value"]))

@eel.expose
def add_field(payload):
    update_task(payload, lambda: utils.add_to_field(utils.find_element_by_id(entries, payload["_id"]), payload["path"], payload["field"], payload["value"]))

@eel.expose
def delete_field(payload):
    update_task(payload, lambda: utils.delete_field(utils.find_element_by_id(entries, payload["_id"]), payload["path"], payload["field"], payload["index"]))


def update_task(payload, fun):
    entry = utils.find_element_by_id(entries, payload["_id"])
    fun()
    update_result = mongo_client.update_entry({"_id": ObjectId(payload["_id"])}, entry, mongo_schema.trackSchema.schema)
    print("update_result", update_result.modified_count)
    eel.setCompState({"track_entries": entries})

@eel.expose
def hello(x):
    print('hello23123123123', x)

@eel.expose
def get_track_entries():
    global entries
    entries =  mongo_client.fetch_entries()
    for entry in entries:
        entry["_id"] = str(entry["_id"])
    return entries

def d():
    n = 0
    while 1:
        time.sleep(2)
        try:
            payload = {"count": n}
            #eel.console_log(payload)
            #eel.setCompState(payload)
            n+=1
        except Exception as e: print("e", e)
    
threading.Thread(target=d).start()

if __name__ == '__main__':
    if sys.argv[1] == '--develop':
        eel.init('src')
        eel.start({"port": 3000}, host="localhost", port=8888, mode="edge")
    else:
        eel.init('build')
        eel.start('index.html', host="localhost", port=8888, mode="edge")
