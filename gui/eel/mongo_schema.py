
import json
import  os
import time
from bson import ObjectId
from mongo import MongoDBClient
from jsonschema import validate
from typing import TypedDict
from typing import List, Dict



upload_sites = ["youtube", "tiktok", "instagram", "threads", "twitter", "facebook", "tumblr" ]

base_schema = {
    "type": "object",
    "properties": { },
    "required": []
}


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
    _dict = {}
    for i in upload_sites:
        _dict[i] = uploadSite.schema
    schema = {
        "type": "object",
        "properties": {
            "track_title": {"type": "string"},
            "grade": {"type": "string"},
            "for_distrokid": {"type": "boolean"},
            "file_name": {"type": "string"},
            "entry_status": {"type": "string"},
             "upload_attempts": {"type": "array", "default": []},   #{ "type": "array", "items": uploadSite.schema}
            # "uploads": uploadSites.schema,   #{ "type": "array", "items": uploadSite.schema}
            "_id": {"type": "string"},
        },
        "required": ["track_title", "grade", "for_distrokid", "entry_status", "upload_attempts"], "additionalProperties": False 
    }
    def create(track_title, grade, for_distrokid, uploads, file_name, entry_status ):  
        obj =  { "track_title": track_title,  "grade":grade, "for_distrokid": for_distrokid, "file_name": file_name, "entry_status": entry_status}#,  "uploads": uploads  } 
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
    def create( date): 
        obj = { "date":date } 
        validate(obj, uploadSession.schema)
        return obj
    
    
if __name__ == "__main__":
    
    example_track = {
        "track_title": "My Track",
        "grade": "A",
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
    
    
    mongo_client = MongoDBClient(uri, 'social-media-helper', 'track-tasks')
    
    #obj = trackSchema.create("op 32", "b", False,   {"youtube":uploadSite.create("tt", [uploadAttemp.create("2023" , "fail")])})
    example_track = trackSchema.create("op 32", "b", False,  uploadSites.create())
    
    print(json.dumps(example_track, indent=4))

    mongo_client.validate_document(example_track, trackSchema.schema )

    mongo_client.delete_all_in_collection()

    entries = mongo_client.fetch_entries()
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

