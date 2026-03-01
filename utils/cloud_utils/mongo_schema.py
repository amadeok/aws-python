
import datetime
import json
import  os
import time
from bson import ObjectId
from utils.cloud_utils.mongo_client import MongoDBClient
from jsonschema import validate
from typing import TypedDict
from typing import List, Dict



default_links_sites = ["youtube", "spotify", "apple_music", "soundcloud", "tidal", "amazon_music", "deezer", "pandora", "google_play_music"]
upload_sites = ["youtube", "tiktok", "instagram", "threads", "twitter", "facebook", "tumblr" ]

base_schema = {
    "type": "object",
    "properties": { },
    "required": []
}

class fileDetailsSchema():
    schema = {
    "type": "object",
    "properties":  { "file_path": {"type": "string"}, "bpm": {"type": "number"},
                      "bars": {"type": "number"},  
                      "bars_per_template": {"type": "number"},
                      "beats_per_bar": {"type": "number"},
                      "avee_custom_lenghts": {"type": "object"},
                      "drive_id": {"type": "string"},
                      "midi_drive_id": {"type": "string"},
                      "custom_video":  {"type": "string"},
                      "has_midi_file": {"type": "boolean"}
                    },
    
    "required": ["file_path", "bpm", "bars", "bars_per_template", "beats_per_bar", "avee_custom_lenghts", "drive_id", "has_midi_file"], "additionalProperties": False 
    }
    def create(file_path, bpm, bars, bars_per_template, beats_per_bar, avee_custom_lenghts, has_midi_file,midi_drive_id, custom_video=None):  
        obj =  { "file_path": file_path, "bpm": bpm,  "bars": bars, "bars_per_template": bars_per_template,  "beats_per_bar": beats_per_bar, "avee_custom_lenghts":avee_custom_lenghts, custom_video: custom_video, "has_midi_file": has_midi_file, "midi_drive_id": midi_drive_id   } 
        validate(obj, fileDetailsSchema.schema)
        return obj

class uploadAttempt():
    schema = {
    "type": "object",
    "properties":  { "track_entry_id": {"type": "string"}, "session_entry_id": {"type": "string"},
                    "site": {"type": "string"},  "date": {"type": "string"}, "error": {"type": "string"},
                    "_id": {"type": "string"},
                    },
    
    "required": ["track_entry_id", "session_entry_id", "site", "date", "error"],"additionalProperties": False 
    }
    def create(track_entry_id, session_entry_id, site, date, error):  
        obj =  { "track_entry_id": track_entry_id, "session_entry_id": session_entry_id, 
                "site": site, "date": date,  "error": error   } 
        validate(obj, uploadAttempt.schema)
        return obj
    

class uploadSite(TypedDict):

    schema = {
    "type": "object",
    "properties":{
           # "name": {"type": "string"},
            "upload_attempts": {
                "type": "array",
                "items": uploadAttempt.schema
            }
        },
        "required": ["upload_attempts"],"additionalProperties": False 
    }
    def create( upload_attempts): 
        obj = { "upload_attempts":upload_attempts } 
        validate(obj, uploadSite.schema)
        return obj

class uploadSites():
    obj = {}
    for i in upload_sites:
        obj[i] = uploadSite.schema
    schema = {
        "type": "object",
        "properties": obj,
        "required": upload_sites,"additionalProperties": False 
    }
    def create(populate=False ):  
        obj =  {  } 
        for i in upload_sites:
            obj[i] = uploadSite.create([])
        validate(obj, uploadSites.schema)
        return obj
    
    
class trackSchema():
    links_obj_default = {
        "youtube": "",
        "spotify":"",
        "apple_music" :"",
        "soundcloud" :"",
        "tidal" :"",
        "amazon_music" :"",
        "deezer" :"",
        "pandora" :"",
        "google_play_music" :""
        }
    schema = {
        "type": "object",
        "properties": {
            "track_title": {"type": "string"},
            "op_number": {"type": "number"},
            "grade": {"type": "number"},
            "for_distrokid": {"type": "boolean"},
            # "file_name": {"type": "string"},
            "entry_status": {"type": "string"},
             "upload_attempts": {"type": "array", "default": []},   #{ "type": "array", "items": uploadSite.schema}
             "file_details": {"type": "object"},# fileDetailsSchema.schema,#{ "type": fileDetailsSchema.schema},
             "insertion_date": {"type": "string"},
             "secondary_text": {"type": "string"},
             "album_number": {"type": "number", "default": -1},
            # "uploads": uploadSites.schema,   #{ "type": "array", "items": uploadSite.schema}
            "_id": {"type": "string"},
            "links": {"type" : "object"}
        },
        "required": ["track_title", "op_number", "grade", "for_distrokid", "links",
                     "entry_status", "upload_attempts", "file_details", "insertion_date", "secondary_text",  "album_number"], "additionalProperties": False 
    }
    def create(track_title, op_number, grade=1, for_distrokid=False, file_details={}, entry_status="pending", upload_attempts=[], insertion_date=None, secondary_text="", album_number=-1, links=links_obj_default ):  
        
        obj =  { "track_title": track_title, "op_number":op_number,  "grade":grade, "for_distrokid": for_distrokid, 
                "file_details": file_details, "entry_status": entry_status, "upload_attempts":upload_attempts, 
                "insertion_date": insertion_date or datetime.datetime.utcnow().isoformat(), 
                "secondary_text": secondary_text, "album_number": album_number, "links":links}#,  "uploads": uploads  } 
        validate(obj, trackSchema.schema)
        return obj

class uploadSession():
    schema = {
    "type": "object",
    "properties":{
            "date": {"type": "string"},
            "pre_upload_errors": {"type": "array", "default": []},
            "upload_attempts": { "type": "array", "default": [] },
            "track_ids": { "type": "array", "default": [] },
            "_id": {"type": "string"},
        },
        "required": ["date", "pre_upload_errors", "upload_attempts", "track_ids" ],"additionalProperties": False 
    }
    def create( date, pre_upload_errors, upload_attempts, track_ids): 
        obj = { "date":date, "pre_upload_errors": pre_upload_errors, "upload_attempts":upload_attempts, "track_ids": track_ids  } 
        validate(obj, uploadSession.schema)
        return obj
    
    
if __name__ == "__main__":
    #o = trackSchema.create("title", "b", False, fileDetailsSchema.create("c:\\path", 120, 15, 2, 4, []), "pending", [] )
    #print(o)
    example_track = {
        "track_title": "My Track",
        "grade": 1,
        "for_distrokid": True,
        "uploads": [
            {
                "name": "yt 1",
                "upload_attempts": [
                    {"date": "2024-04-01", "error": ""},
                    {"date": "2024-04-02", "error": "Failed"}
                ]
            },
            {
                "name": "tt 1",
                "upload_attempts": [
                    {"date": "2025-04-01", "error": ""},
                    {"date": "2025-04-02", "error": "Failed"}
                ]
            }
        ]
    }
    
    uri = os.getenv("MONGODB_URI")
    
    mongo_client = MongoDBClient(uri, 'cristiank_website', {"newsletter_emails":None}  )
    
    # mongo_client = MongoDBClient(uri, 'social-media-helper',
    #                          {'track_entries': trackSchema.schema, 
    #                           "upload_attempts": uploadAttempt.schema,
    #                           "upload_sessions": uploadSession.schema} )
    
    time.sleep(1)
    #obj = trackSchema.create("op 32", "b", False,   {"youtube":uploadSite.create("tt", [uploadAttemp.create("2023" , "fail")])})
    # example_track = trackSchema.create("op 32", "b", False,  uploadSites.create())
    
    # print(json.dumps(example_track, indent=4))

    # mongo_client.validate_document(example_track, trackSchema.schema )

    # mongo_client.delete_all_in_collection()
    # entries = list(mongo_client.client["newsletter_emails"].find({}))
        
    # Step 2: Access the database
    db = mongo_client.client["cristiank_website"]

    # Step 3: Access the collection
    collection = db["newsletter_emails"]

    # Step 4: Retrieve all documents
    documents = collection.find({})

    # Step 5: Print or process the documents
    for doc in documents:
        print(doc)
    # entries = mongo_client.fetch_entries("newsletter_emails")
    print("Existing entries:", entries)

    new_entry_id = mongo_client.create_entry(example_track)
    print("New entry ID:", new_entry_id)

    entries_after_insertion = mongo_client.fetch_entries()
    print("Entries after insertion:", entries_after_insertion)

    update_query = {"track_title": "op 32"}
    example_track["uploads"]["youtube"]["upload_attempts"].append(uploadAttempt.create("youtube", "2423" , "success"))
    update_result = mongo_client.update_entry(update_query, example_track, trackSchema.schema)
    example_track["uploads"]["youtube"]["upload_attempts"][0]["date"] = "4323"

    update_result = mongo_client.update_entry(update_query, example_track, trackSchema.schema)

    if update_result:
        print("Update result:", update_result.modified_count)

    # Fetch entries after update
    entries_after_update = mongo_client.fetch_entries()
    print("Entries after update:", entries_after_update)

    # Delete entry
    delete_query = {"_id": ObjectId("65fc32319baf6eeae3d8e352")}
    delete_result = mongo_client.delete_entry(delete_query)
    print("Delete result:", delete_result.deleted_count)

    # Fetch entries after deletion
    entries_after_deletion = mongo_client.fetch_entries()
    print("Entries after deletion:", entries_after_deletion)
    
    # Close connection
    mongo_client.client.close()

