
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


class uploadAttemp():
    schema = {
    "type": "object",
    "properties":  { "date": {"type": "string"}, "error": {"type": "string"} },
    "required": ["date", "error"],"additionalProperties": False 
    }
    def create(date, error):  
        obj =  { "date": date,  "error": error   } 
        validate(obj, uploadAttemp.schema)
        return obj
    

class uploadSite(TypedDict):

    schema = {
    "type": "object",
    "properties":{
           # "name": {"type": "string"},
            "upload_attempts": {
                "type": "array",
                "items": uploadAttemp.schema
            }
        },
        "required": ["upload_attempts"],"additionalProperties": False 
    }
    def create( upload_attempts): 
        obj = { "upload_attempts":upload_attempts } 
        validate(obj, uploadSite.schema)
        return obj

class uploadSites(TypedDict):
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
    
    
class trackSchema(TypedDict):
    _dict = {}
    for i in upload_sites:
        _dict[i] = uploadSite.schema
    schema = {
        "type": "object",
        "properties": {
            "track_title": {"type": "string"},
            "grade": {"type": "string"},
            "for_distrokid": {"type": "boolean"},
            "uploads": uploadSites.schema,   #{ "type": "array", "items": uploadSite.schema}
            "_id": {"type": "string"},
        },
        "required": ["track_title", "uploads"],"additionalProperties": False 
    }
    def create(track_title, grade, for_distrokid, uploads ):  
        obj =  { "track_title": track_title,  "grade":grade, "for_distrokid": for_distrokid, "uploads": uploads  } 
        validate(obj, trackSchema.schema)
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
    example_track["uploads"]["youtube"]["upload_attempts"].append(uploadAttemp.create("2423" , "success"))
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

