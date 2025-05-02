
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
    entries_to_change = []
    for entry in entries:
        try:
            if not "links" in entry:
                query = {"_id": ObjectId(entry["_id"])}
                data = {"links": obj}
                ret = client.update_entry(query, data, "track_entries")
                print("updated ", entry["op_number"], ret.modified_count)
                #print(entry["links"])
            # if not "Op. " in entry["track_title"]:
            #     entry["track_title"] = f"""Op. {entry["track_title"]}"""
            #     print("op changed", entry["op_number"])
            #     entries_to_change.append(entry)
            # # entry["grade"] = float(entry["grade"])
            # assert str(entry["op_number"]) in entry["track_title"]
        except Exception as e: 
            print("Error", e)
            # entry["grade"] =  -10.0

    for entry in entries_to_change:
        query = {"_id": ObjectId(entry["_id"])}
        data = {"track_title": entry["track_title"]}
        ret = client.update_entry(query, data, "track_entries")# mongo_schema.trackSchema.schema)
        print(entry["op_number"], ret)

