from flask import Flask, request, jsonify, send_from_directory
import os, subprocessHelper

from dotenv import load_dotenv

from utils.cloud_utils import mongo_client, mongo_schema
import utils.mongo_utils as mongo_utils
 
load_dotenv()

uri = os.getenv("MONGODB_URI")

client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                        {'track_entries': mongo_schema.trackSchema.schema, 
                        "upload_attempts": mongo_schema.uploadAttempt.schema,
                        "upload_sessions": mongo_schema.uploadSession.schema, 
                        "settings": None} )

database = mongo_utils.get_track_entries_(client)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Current working directory changed to: {os.getcwd()}")


job = subprocessHelper.JobObject()
job.assign_process(subprocessHelper.subprocess.Popen('browser-sync start --proxy localhost:5000 --files *.html,script.js,aux_.js,static/*'.split(" "), shell=True))

app = Flask(__name__)



# Serve HTML file
@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def serve_script():
    return send_from_directory('.', 'script.js')

@app.route('/aux_.js')
def serve_aux_():
    return send_from_directory('.', 'aux_.js')


# Handle API calls
@app.route('/api', methods=['POST'])
def handle_api():
    data = request.get_json()
    print("Received API call with data:", data)
    
    # Process the data here
    response = {
        'status': 'success',
        'data': data,
        'message': 'API call processed successfully'
    }
    return jsonify(response)


@app.route('/get-database', methods=['GET'])
def handle_get():
    print("Received API call with data get")
    
    # Process the data here
    response = {
        'status': 'success',
        'data': database,
        'message': 'Database fetched successfully'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000, debug=False)