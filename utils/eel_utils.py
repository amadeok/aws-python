
import os, sys, eel
from bson import ObjectId
import logging, uuid, subprocess, copy
import utils.cloud_utils.mongo_client as mongo_client
import utils.cloud_utils.gdrive as gdrive
import utils.cloud_utils.mongo_schema as mongo_schema
import utils.mongo_utils as mu

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
    current, last_key = get_field_current(obj, path)
    check_type(current[last_key])

    if field is None:
        current[last_key].append(value)
    else:
        current[last_key][field].append( value)
    
def delete_field(obj, path, field, index):
    current, last_key = get_field_current(obj, path)
    check_type(current[last_key])

    if field is None:
        del current[last_key][index]
    else:
        del current[last_key][field][index]

    
def find_element_by_id(array, target_id):
    return next((element for element in array if element.get('_id') == target_id), None)


def set_file_logging():
    logging.basicConfig(filename='python_.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

# class eelHandler():
#     def __init__(self) -> None:
#         pass
mongo = None
def setMongoInstance(mongo_):
    global mongo
    mongo = mongo_
    
def getMongoInstance():
    global mongo
    return mongo

def initMongoInstance(connection_string, database_name, collection_schemas):
    global mongo
    mongo = mongo_client.MongoDBClient(connection_string, database_name,  collection_schemas)
    return mongo

@eel.expose
def update_field(payload):
    update_task(payload, lambda: update_nested_field(find_element_by_id(mongo.cd[payload["collection"]], payload["_id"]), payload["path"], payload["index"], payload["field"], payload["value"]))

@eel.expose
def add_field(payload):
    update_task(payload, lambda: add_to_field(find_element_by_id(mongo.cd[payload["collection"]], payload["_id"]), payload["path"], payload["field"], payload["value"]))

@eel.expose
def delete_field(payload):
    update_task(payload, lambda: delete_field(find_element_by_id(mongo.cd[payload["collection"]], payload["_id"]), payload["path"], payload["field"], payload["index"]))

@eel.expose
def delete_entry(payload):
    if payload["collection"] == "track_entries":
        entry = find_element_by_id(mongo.cd[payload["collection"]], payload["_id"])
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
    entry = find_element_by_id(mongo.cd[payload["collection"]], payload["_id"])
    if not type(fun) == list:
        fun = [fun]
    for f in fun:
        f()
    update_result = mongo.update_entry({"_id": ObjectId(payload["_id"])}, entry, payload["collection"], mongo.schemas[payload["collection"]])
    logging.info(f"update_result { update_result.modified_count if update_result else 'Nothing updated'} {  'op id:' + str(uuid.uuid1())  }")#'value: ' +  str(payload['value']) if payload['value'] else
    eel.setCompState(get_track_entries())

def open_file_dialog():
    file = "utils/file_dialog.py"
    assert os.path.isfile(file)
    
    process = subprocess.Popen(['python', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stdout:
        ret = stdout.decode()
        ret2 = ret.split("|")
        if len(ret2) > 1:
            file = ret2[1].replace("\n", "").replace("\r", "")
            logging.info("Selected file: { file}")
            return file
        else: return None
        
    if stderr:
        logging.info("Error:")
        logging.info(stderr.decode())

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
    ret = open_file_dialog()
    #def update_field(payload):
    if  ret:
        if not os.path.isfile(ret):
            file = "utils/file_not_found.py"
            assert os.path.isfile(file)
            #result = pyautogui.confirm(f'File doesnt could not be found {ret}', buttons=['OK'])
            process = subprocess.Popen(['python', file, ret if ret else "dummy"])
            process.wait()
        else:
            entry = find_element_by_id(mongo.cd["track_entries"], _id)
            if len(entry["file_details"]["drive_id"]):
                gdrive.delete_file(entry["file_details"]["drive_id"])
            uploaded_id = gdrive.create_file(ret, os.path.basename(ret))
            p1 = {"collection": "track_entries", "_id": _id, "path": "file_details", "index": None, "field": "file_path", "value": ret}          
            p2 = {"collection": "track_entries", "_id": _id, "path": "file_details", "index": None, "field": "drive_id", "value": uploaded_id} 
            funs = [
                lambda: update_nested_field(find_element_by_id(mongo.cd[p1["collection"]], p1["_id"]), p1["path"], p1["index"], p1["field"], p1["value"]),
                lambda: update_nested_field(find_element_by_id(mongo.cd[p2["collection"]], p2["_id"]), p2["path"], p2["index"], p2["field"], p2["value"])
            ]
            update_task(p1, funs )

    return ret


@eel.expose
def get_track_entries():
    return mu.get_track_entries_(mongo)
    assert mongo
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