import json
import logging, os
import loggingHelper, flask
APP_NAME = "track_monitor"
loggingHelper.Logger(APP_NAME, level=logging.INFO,ignore_strings=["GET /health"])
#, log_file=F"{os.path.dirname(os.path.abspath(__file__))}/logs/{APP_NAME}.log",
        # level=logging.INFO, max_bytes=1000*1000, backup_count=3,
        # format_ =  logging.Formatter(
        #     f'%(asctime)s - %(levelname)s - %(message)s'
        # ))

import datetime, sys
import objectGuiJsPy, os
from dotenv import load_dotenv
sys.path.insert(0, r"F:\all\GitHub\aws-python")

from utils.cloud_utils import mongo_client, mongo_schema
import utils.mongo_utils as mongo_utils    
import flask, glob
from bson.objectid import ObjectId

# from flask import Flask, request, jsonify, send_from_directory
# import os, subprocessHelper,sys

# from dotenv import load_dotenv
import utils.eel_utils as eel_utils

def get_most_recent_file(directory, pattern='*'):
    files = glob.glob(os.path.join(directory, pattern))
    if not files:  return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

class MyCustomApp(objectGuiJsPy.FlaskApp):
    def __init__(self, mongo_client_,  *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.mongo_client : mongo_client = mongo_client_
        
                    
        @self.app.route('/get_audio')
        def get_audio():
            folder_path, it = get_it_path()
            file_path = get_most_recent_file(folder_path)
            if file_path == None or not os.path.exists(file_path):
                flask.abort(404, description="Audio file not found")
            
            response = flask.send_file(file_path, mimetype='audio/wav')
            
            response.headers['X-Custom-Data'] = json.dumps({"file_path":  file_path.split(os.getenv("PLAY_WAV_FOLDER"))[1], "iteration_found": it })
            
            return response

        @self.app.route('/open_folder')
        def open_folder():
            folder_path, it = get_it_path()
            if  not os.path.exists(folder_path):
                flask.abort(404, description="folder not found")
            os.startfile(folder_path)
            response =  {
                'status': 'success',
                'message': 'folder opened successfully'
            }
            return flask.jsonify(response)
        
        def get_it_path():

            op_number = flask.request.args.get('op', type=int)
            iteration = flask.request.args.get('it', type=int)
            folder = os.getenv("PLAY_WAV_FOLDER")
            op_dir = f"{op_number:05d}" 
            highest_it= None
            if iteration == -1:
                highest_it = 1
                for x in range(1, 10):
                    folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{x}")
                    if os.path.isdir(folder_path) and os.listdir(folder_path).__len__()  > 0:
                        highest_it = x
                logging.info(f"Highest iteration for for op. {op_number}: {highest_it}")
                folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{highest_it}")
                
            elif iteration:            
                if op_number is None or iteration is None:   flask.abort(400, description="Missing required parameters: 'op' and 'it'")
                folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{iteration}")
            else:
                if op_number is None:  flask.abort(400, description="Missing required parameters: 'op'")
                folder_path = os.path.join(folder, op_dir)
                
            return folder_path, highest_it or iteration

        @self.app.route('/create_entry')
        def create_entry():
            try:
                #op_number = len(self.database)
                op_number = max(self.database, key=lambda x: x['op_number'])['op_number'] +1
                payload = mongo_schema.trackSchema.create(track_title=f"Op. {op_number}", op_number=op_number)
                # payload = {
                #     "op_number": op_number,
                #     "track_title": f"Op. {op_number}",
                #     "for_distrokid": False,
                #     "grade": 1,
                #     "entry_status": "pending",
                #     "insertion_date":  datetime.datetime.utcnow().isoformat()
                # }
                new_entry_id = self.mongo_client.create_entry(payload, "track_entries", mongo_schema.trackSchema.schema)#, mongo.schemas[collection])
                response = {
                    "new_entry_id":str(new_entry_id),
                    "success": True
                }
            except Exception as e:
                logging.error(f"error {e}")
                response  = {
                    "success": False, "error": str(e)
                }

            return flask.jsonify(response)
        
        @self.app.route('/delete_entry')
        def delete_entry():
            try:
                payload = {
                    "_id": flask.request.args.get('_id', type=str),
                    "collection":  flask.request.args.get('collection', type=str)
                }
                eel_utils.base_delete_entry(payload, self.mongo_client) 
                response = {"success": True}
            except Exception as e:
                logging.info(f"error: {e}")
                response = {"success": False, "error": str(e)}

            return flask.jsonify(response)
    
    def get_database(self):
        self.database = mongo_utils.get_track_entries_(self.mongo_client)["track_entries"]
        return self.database
        
    def custom_handle_api(self):

        data = flask.request.get_json()
        logging.info(f"Custom API handler received: {data}")
        try:
            if "key_to_update" in data:
                key = data["key_to_update"]
                new_val = data["elem"][key]
                try:
                    new_val
                except Exception as e:
                    pass
                # end try
                _id = ObjectId(data["elem"]["_id"])
                update_data = {key: new_val}
                update_result =  self.mongo_client.update_entry({"_id":_id}, update_data, "track_entries")

            response = {
                'status': 'success',
                'data': data,
                'message': 'Custom API processing complete',
                "update_count": update_result.modified_count
            }
            
        except Exception as e:
            logging.info(f"Error: {e}")
            
            response = {
                'status': 'error',
                'error': e,
            }

        return flask.jsonify(response)

    
if __name__ == "__main__" or 1:
    #import settingsManager
    # parser = settingsManager.ArgParser( ("debug", bool, False), ("port", int, None), ("simple_gui:app", str, "None", False))
    # parser.parser.add_argument("simple_gui:app")

    port = int(os.getenv("PROD_PORT") or 8912)
    debug = int(os.getenv("PROD_DEBUG") or True)
    os.environ["CLOSE_ON_CLIENT_DISCONNECT"]  = "0"
    
    load_dotenv(r"F:\all\GitHub\aws-python\.env")
    uri = os.getenv("MONGODB_URI")
    global client
    
    client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )


    
    database = mongo_utils.get_track_entries_(client)

    gui_app = MyCustomApp(mongo_client_=client, database=database["track_entries"], app_name=APP_NAME,
                          html_path= os.path.dirname(os.path.abspath(__file__)),debug_mode=debug, port=port)
    if debug:
        gui_app.setup_browser_sync()
        gui_app.run()
    elif gui_app.use_browser_sync:
        gui_app.setup_browser_sync()

    app = gui_app.app



