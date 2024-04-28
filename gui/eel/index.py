# coding: utf-8
import subprocess
import sys, time, os
import uuid
#import threading
from bson import ObjectId
#import pyautogui
from mongo import MongoDBClient
import utils
#sys.path.insert(1, r'F:\all\GitHub\Eel')
import eel
import mongo_schema
import copy
import logging
import gdrive

sys.path.append('../../')  # Adds the parent directory to the Python path
import provision

uri = os.getenv("MONGODB_URI")
mongo = MongoDBClient(uri, 'social-media-helper',
                             {'track_entries': mongo_schema.trackSchema.schema, 
                              "upload_attempts": mongo_schema.uploadAttempt.schema,
                              "upload_sessions": mongo_schema.uploadSession.schema} )

if hasattr(sys, "_MEIPASS"): # if the script is started from an executable file
    with open("logs.txt", "a") as f_logs:
        sys.stdout = f_logs
        sys.stderr = f_logs


@eel.expose
def update_field(payload):
    update_task(payload, lambda: utils.update_nested_field(utils.find_element_by_id(mongo.cd[payload["collection"]], payload["_id"]), payload["path"], payload["index"], payload["field"], payload["value"]))

@eel.expose
def add_field(payload):
    update_task(payload, lambda: utils.add_to_field(utils.find_element_by_id(mongo.cd[payload["collection"]], payload["_id"]), payload["path"], payload["field"], payload["value"]))

@eel.expose
def delete_field(payload):
    update_task(payload, lambda: utils.delete_field(utils.find_element_by_id(mongo.cd[payload["collection"]], payload["_id"]), payload["path"], payload["field"], payload["index"]))

@eel.expose
def delete_entry(payload):
    if payload["collection"] == "track_entries":
        entry = utils.find_element_by_id(mongo.cd[payload["collection"]], payload["_id"])
        if len(entry["file_details"]["drive_id"]):
            gdrive.delete_file(entry["file_details"]["drive_id"])
        
    delete_query = {"_id": ObjectId(payload["_id"])}
    ret = mongo.delete_entry(delete_query, payload["collection"])
    if ret and ret.deleted_count:
        logging.info(f"""Deleted entry with id: {payload["_id"]} , {ret.deleted_count  if ret else 0}""")
    else:
        logging.info(f"""NO entry deleted with id: {payload["_id"]} , {ret.deleted_count  if ret else 0}""")
    
    other_collection = ""; other_collection_entry_name = ""
    if payload["collection"] == "track_entries":
        other_collection = "upload_sessions"
        other_collection_entry_name = "session_entry_id"
        collection_entry_name = "track_entry_id"
    elif  payload["collection"] == "upload_sessions":
        other_collection = "track_entries"
        other_collection_entry_name = "track_entry_id"
        collection_entry_name = "session_entry_id"

    if len(other_collection):    
        attempts_filtered = [item for item in mongo.cd["upload_attempts"] if item.get(collection_entry_name) == payload["_id"]]
        def check(attempt):
#            for attempt in attempts_:
            for item in mongo.cd[other_collection]:
                if attempt[other_collection_entry_name] == item["_id"]:
                    return True
            return False
        for attempt in attempts_filtered:
            ret = check(attempt)
            if not ret:
                deleted = mongo.delete_entry({"_id": ObjectId(attempt["_id"])}, "upload_attempts")
                logging.info(f"--->deleting unreferenced upload attempt with id  {attempt['_id']} {deleted.deleted_count if deleted else 'delete fail'}")
        
        #utils.check_field_presence(mongo.cd["track_entries"], mongo.cd["upload_attempts"], "upload_attempts", "track_ids")


    eel.setCompState(get_track_entries())

@eel.expose
def create_entry(payload):
    logging.info("---create_entry")

    collection = payload["collection"]
    del payload["collection"]
    new_entry_id = mongo.create_entry(payload, collection, mongo.schemas[collection])
    logging.info(f"""created entry with id: {new_entry_id} """)
    eel.setCompState(get_track_entries())



def update_task(payload, fun):
    entry = utils.find_element_by_id(mongo.cd[payload["collection"]], payload["_id"])
    if not type(fun) == list:
        fun = [fun]
    for f in fun:
        f()
    update_result = mongo.update_entry({"_id": ObjectId(payload["_id"])}, entry, payload["collection"], mongo.schemas[payload["collection"]])
    logging.info(f"update_result { update_result.modified_count if update_result else 'Nothing updated'} {  'op id:' + str(uuid.uuid1())  }")#'value: ' +  str(payload['value']) if payload['value'] else
    eel.setCompState(get_track_entries())

@eel.expose
def hello(x):
    logging.info(f'Hello from python backend {x}')

@eel.expose
def trigger_provision(dummy):
    provision.provision(dummy)
    logging.info(f'Provision {"dummy" if dummy else "" }')
    
# @eel.expose
# def close_python(*args):
#     logging.info('closing python')
#     utils.stop  = True
#     sys.exit()

@eel.expose
def open_file_select_window(_id):
    logging.info(f'Opening file dialog {_id}')
    ret = utils.open_file_dialog()
    #def update_field(payload):
    if  ret:
        if not os.path.isfile(ret):
            #result = pyautogui.confirm(f'File doesnt could not be found {ret}', buttons=['OK'])
            process = subprocess.Popen(['python', 'file_not_found.py', ret if ret else "dummy"])
            process.wait()
        else:
            entry = utils.find_element_by_id(mongo.cd["track_entries"], _id)
            if len(entry["file_details"]["drive_id"]):
                gdrive.delete_file(entry["file_details"]["drive_id"])
            uploaded_id = gdrive.create_file(ret, os.path.basename(ret))
            p1 = {"collection": "track_entries", "_id": _id, "path": "file_details", "index": None, "field": "file_path", "value": ret}          
            p2 = {"collection": "track_entries", "_id": _id, "path": "file_details", "index": None, "field": "drive_id", "value": uploaded_id} 
            funs = [
                lambda: utils.update_nested_field(utils.find_element_by_id(mongo.cd[p1["collection"]], p1["_id"]), p1["path"], p1["index"], p1["field"], p1["value"]),
                lambda: utils.update_nested_field(utils.find_element_by_id(mongo.cd[p2["collection"]], p2["_id"]), p2["path"], p2["index"], p2["field"], p2["value"])
            ]
            update_task(p1, funs )

    return ret


@eel.expose
def get_track_entries():
    payload = {}
    for name in mongo.collection_names:
        mongo.cd[name]  =  mongo.fetch_entries(name, None)

    tracks = copy.deepcopy(mongo.cd["track_entries"])
    attempts =copy.deepcopy( mongo.cd["upload_attempts"])
    sessions =copy.deepcopy( mongo.cd["upload_sessions"] )
    
    payload["track_entries"] = tracks
    payload["upload_attempts"] = attempts
    payload["upload_sessions"] = sessions

    attempts_ = attempts.copy()
    s = len(attempts_)-1
    while s >= 0:
        attempt = attempts_[s]
        for track in tracks:
            if attempt["track_entry_id"] == track["_id"]:
                track["upload_attempts"].append(attempt)
                break
        for session in sessions:
            if attempt["session_entry_id"] == session["_id"]:
                session["upload_attempts"].append(attempt)
                break
        s-=1
    

    # utils.merge_arrays(mongo.cd["track_entries"] , mongo.cd["upload_attempts"], "upload_attempts", "_id")
    # utils.merge_arrays(mongo.cd["upload_sessions"] , mongo.cd["upload_attempts"], "upload_attempts", "session_entry_id")
    for upload_session in sessions:
        for upload_attempt in upload_session["upload_attempts"]:
            if not upload_attempt["track_entry_id"] in upload_session["track_ids"]:
                upload_session["track_ids"].append(upload_attempt["track_entry_id"])

    # utils.merge_arrays(mongo.cd["upload_sessions"] , mongo.cd["track_entries"], "track_entries", "_id")

    payload["upload_sites"] = mongo_schema.upload_sites
    return payload
 

if __name__ == '__main__':
    try:
        if  len(sys.argv)>1 and sys.argv[1] == '--develop':
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            eel.init('src')
            eel.start({"port": 3000}, host="localhost", port=8888, mode="edge")
        elif 0:
            # eel.init('build')
            # eel.start('index.html', host="localhost", port=8888, mode="edge")
            utils.start_node()
            utils.set_file_logging()
            logging.info("---init")

            eel.init('build')
            eel.start({"port": 3000}, host="localhost", port=8888)
            
            logging.info("---after eel start")
        else:
            eel.init('build', ['.tsx', '.ts', '.jsx', '.js', '.html'])
            eel_kwargs = dict(
            host='localhost',
            port=8888,
            size=(1280, 800),
            )   
            utils.set_file_logging()

            def test(a, b):
                logging.info(f"------------CLOSED {a}, {b}")
                # sys.exit()
            eel.start('index.html',  **eel_kwargs,  close_callback=test ) #mode= 'edge',

            #eel.start('index.html', block=True, options={'port': 80, 'host': '0.0.0.0', 'close_callback': lambda: print("------------CLOSE"), 'mode': False})
            logging.info("---after eel start")
    except Exception as e:
        logging.error(f"exception at index main function of index.py: {e}")



