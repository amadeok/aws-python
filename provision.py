import os
import time
from dotenv import load_dotenv
import app_logging
import logging, json
from utils.eel_utils import get_track_entries, initMongoInstance
import utils.cloud_utils.mongo_schema as mongo_schema
import uploader

def provision(dummy=False, payload=None):
    print(f"provision {dummy}")
    if not payload:
        payload = get_track_entries()
    json_string = json.dumps(payload, indent=4)
    #json_data = json.loads(payload)

    print()
    print("payload", json_string)
    
    print()
    for e in payload["track_entries"]:
        ret = [attempt.get("error") != "" for attempt in e.get("upload_attempts", [])]
        print(any(ret), ret)
    print()
    
    track_entries = payload["track_entries"]
    upload_sites = payload["upload_sites"]

    entries_with_no_upload_attempts = [entry for entry in track_entries if not entry.get("upload_attempts")]
    entries_with_no_upload_attempts_and_not_ready = [entry for entry in entries_with_no_upload_attempts if entry.get("entry_status") != "ready"]

    track_entries_with_errors = [
        entry for entry in track_entries 
        if any(len(attempt.get("error")) for attempt in entry.get("upload_attempts", []))
    ]
    
    tracks_missing_attempts = []

    for entry in track_entries:
        missing_sites = [site for site in upload_sites if not any(attempt.get("site") == site for attempt in entry.get("upload_attempts", []))]
        if missing_sites:
            tracks_missing_attempts.append({"track_entry" : entry, "missing_sites":missing_sites})

    logging.info(f"tracks_missing_attempts  {  json.dumps(tracks_missing_attempts, indent=4)}" )

    #logging.info(f"with errors {  json.dumps(track_entries_with_errors, indent=4)}" )
    #logging.info(f"no_upload {  json.dumps(entries_with_no_upload_attempts, indent=4)}" )

    logging.info(f"Number of tracks without upload attempts {len(entries_with_no_upload_attempts)}" )
    logging.info(f"Number of tracks without upload attempts and not ready {len(entries_with_no_upload_attempts_and_not_ready)}" )
    logging.info(f"Number of tracks with missing attempts {len(tracks_missing_attempts)}" )
    logging.info(f"Number of tracks with error in upload attempts {len(track_entries_with_errors)}" )
    
    #prepare tasks
    logging.info("Dowloading file from drive..")
    
    with open('data\hashtag_map.json', 'r') as file:
        hashtag_map = json.load(file)
    
        
    task_payload = uploader.taskPayload(hashtag_map=hashtag_map)
    
    logging.info("Preparing upload tasks..")
     
  
    
    

if __name__ == '__main__':
    load_dotenv(dotenv_path=r"gui/eel/.env")    
    uri = os.getenv("MONGODB_URI")
    

    

    mongo =  initMongoInstance(uri, 'social-media-helper',
                             {'track_entries': mongo_schema.trackSchema.schema, 
                              "upload_attempts": mongo_schema.uploadAttempt.schema,
                              "upload_sessions": mongo_schema.uploadSession.schema} )
    #time.sleep(5)
    provision()

    
