
from bson import ObjectId
import eel_utils
import mongo_utils
import cloud_utils.mongo_schema as mongo_schema
import cloud_utils.mongo_client as mongo_client, os, sys
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":


    uri = os.getenv("MONGODB_URI")

    client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )
    
    database = mongo_utils.get_track_entries_(client)
    entries = database["track_entries"]
    for entry in entries:
        try:
            entry["grade"] = float(entry["grade"])
        except Exception as e: 
            print("Error", e)
            entry["grade"] =  -10.0

    for entry in entries:
        query = {"_id": ObjectId(entry["_id"])}
        data = {"grade": entry["grade"]}
        client.update_entry(query, data, "track_entries")# mongo_schema.trackSchema.schema)

