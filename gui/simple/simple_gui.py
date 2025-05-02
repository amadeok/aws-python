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
            folder_path = get_it_path()
            file_path = get_most_recent_file(folder_path)
            if file_path == None or not os.path.exists(file_path):
                flask.abort(404, description="Audio file not found")
        
            return flask.send_file(file_path, mimetype='audio/wav')

        @self.app.route('/open_folder')
        def open_folder():
            folder_path = get_it_path()
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

            if iteration:            
                if op_number is None or iteration is None:   flask.abort(400, description="Missing required parameters: 'op' and 'it'")
                folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{iteration}")
            else:
                if op_number is None:  flask.abort(400, description="Missing required parameters: 'op'")
                folder_path = os.path.join(folder, op_dir)
                
            return folder_path

        @self.app.route('/create_entry')
        def create_entry():
            try:
                #op_number = len(self.database)
                op_number = max(self.database, key=lambda x: x['op_number'])['op_number'] +1
                payload = mongo_schema.trackSchema.create(f"Op. {op_number}", op_number, 1, False, {}, "pending", [], datetime.datetime.utcnow().isoformat(), "")
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
                print (e)
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
                print("error", e)
                response = {"success": False, "error": str(e)}

            return flask.jsonify(response)

        print("Child initialized")
    
    def get_database(self):
        self.database = mongo_utils.get_track_entries_(self.mongo_client)["track_entries"]
        return self.database
        
    def custom_handle_api(self):

        data = flask.request.get_json()
        print("Custom API handler received:", data)
        try:
            if "key_to_update" in data:
                key = data["key_to_update"]
                new_val = data["elem"][key]
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
            print("Error", e)
            
            response = {
                'status': 'error',
                'error': e,
            }

        return flask.jsonify(response)

    
if __name__ == "__main__" or 1:
    #import settingsManager
    # parser = settingsManager.ArgParser( ("debug", bool, False), ("port", int, None), ("simple_gui:app", str, "None", False))
    # parser.parser.add_argument("simple_gui:app")
    print("getwd", os.getcwd())
    port = int(os.getenv("WAITRESS_PORT") or 8912)
    debug = int(os.getenv("WAITRESS_DEBUG") or True)

    load_dotenv(r"F:\all\GitHub\aws-python\.env")
    uri = os.getenv("MONGODB_URI")
    global client
    
    client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )

    database = mongo_utils.get_track_entries_(client)

    gui_app = MyCustomApp(mongo_client_=client, database=database["track_entries"],
                          html_path= os.path.dirname(os.path.abspath(__file__)),debug_mode=debug, port=port)
    if debug:
        gui_app.setup_browser_sync()
        gui_app.run()
    app = gui_app.app






# script_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_dir)
# print(f"Current working directory changed to: {os.getcwd()}")


# job = subprocessHelper.JobObject()
# job.assign_process(subprocessHelper.subprocess.Popen('browser-sync start --proxy localhost:5000 --files *.html,script.js,aux_.js,static/*'.split(" "), shell=True))

# app = Flask(__name__)



# # Serve HTML file
# @app.route('/')
# def serve_html():
#     return send_from_directory('.', 'index.html')

# @app.route('/script.js')
# def serve_script():
#     return send_from_directory('.', 'script.js')

# @app.route('/aux_.js')
# def serve_aux_():
#     return send_from_directory('.', 'aux_.js')


# # Handle API calls
# @app.route('/api', methods=['POST'])
# def handle_api():
#     data = request.get_json()
#     print("Received API call with data:", data)
    
#     # Process the data here
#     response = {
#         'status': 'success',
#         'data': data,
#         'message': 'API call processed successfully'
#     }
#     return jsonify(response)


# @app.route('/get-database', methods=['GET'])
# def handle_get():
#     print("Received API call with data get")
    
#     # Process the data here
#     response = {
#         'status': 'success',
#         'data': database,
#         'message': 'Database fetched successfully'
#     }
#     return jsonify(response)


# @app.route('/test', methods=['POST'])
# def handle_api_():
#     data = request.get_json()
#     print("Received API call with data:", data)
    
#     # Process the data here
#     response = {
#         'status': 'success',
#         'data': "TEST",
#         'message': 'API call processed successfully'
#     }
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(port=5000, debug=False)