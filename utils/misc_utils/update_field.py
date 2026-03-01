import json
import os, sys
sys.path.insert(0, r"F:\all\GitHub\aws-python")
from bson import ObjectId

import utils.mongo_utils as mongo_utils
import utils.cloud_utils.mongo_schema as mongo_schema
import utils.cloud_utils.mongo_client as mongo_client, os, sys
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient

import requests

def revalidate_page(id_value, secret_token=None):
    secret_token = secret_token or os.getenv("CRISTIANK_REV_TOKEN")
    params = {
        "secret": secret_token,
        "id": id_value
    }
    host = "https://cristiank.com"
    # host = "http://localhost:3000"
    url = f"{host}/api/revalidate"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

# Example usage:
# result = revalidate_page("music")
# print(result)
   

if __name__ == "__main__":


    uri = os.getenv("MONGODB_URI")

    client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )
    # client.update_field_value_or_range("album_number", new_value=1, exact_value=8 , collection_name="track_entries",  )#min_value=3, max_value=7)
    

    database = mongo_utils.get_track_entries_(client)
    entries = database["track_entries"]
    entries_to_change = []
    file = r"F:\all\GitHub\socials_api\yt_data.json"
    with open(file, "r") as f:
        json_data = json.loads(f.read())
        
    website_sheet_dir =  r"F:\all\GitHub\cristiank_website\public\sheet_music"



    for entry in entries:
        try:
            # op_num = entry["op_number"]
            # op_str = f"{op_num:05d}"
            # for f in os.listdir(website_sheet_dir):
            #     if f.startswith(op_str):
            #         print("found", op_str)
            #         data = {"sheet": f"/sheet_music/{f}"}
            #         query = {"_id": ObjectId(entry["_id"])}
            #         ret = client.update_entry(query, data, "track_entries")# mongo_schema.trackSchema.schema)
            #         print(entry["op_number"], ret)
            # str_ = str(entry["op_number"])
            # if str_ in json_data:
            #     op_num = entry["op_number"]
            #     query = {"_id": ObjectId(entry["_id"])}
            #     data = {"links.youtube": json_data[str_]}
            #     ret = client.update_entry(query, data, "track_entries")# mongo_schema.trackSchema.schema)
            #     print(entry["op_number"], ret)
        
            # if not "album_number" in entry:
            query = {"_id": ObjectId(entry["_id"])}
            an  = entry ["album_number"]
            if  an == 1 or an == 2:
                # ret = client.update_entry(query, {"entry_status": "ready"}, "track_entries")
                ret = revalidate_page(f'sheet/{entry["op_number"]}')

                print("updated ", entry["op_number"], f"\n{ret}")#, ret.modified_count)
            # if not "links" in entry:
            #     query = {"_id": ObjectId(entry["_id"])}
            #     data = {"links": obj}
            #     ret = client.update_entry(query, data, "track_entries")
            #     print("updated ", entry["op_number"], ret.modified_count)
                #print(entry["links"])
            # if not "Op. " in entry["track_title"]:
            # entry["track_title"] = f"""Piece {entry["op_number"]}"""
            # print("op changed", entry["op_number"])
            # entries_to_change.append(entry)
            # entry["grade"] = float(entry["grade"])
            # assert str(entry["op_number"]) in entry["track_title"]
        except Exception as e: 
            print("Error", e)
            # entry["grade"] =  -10.0

    # for entry in entries_to_change:
        # query = {"_id": ObjectId(entry["_id"])}
        # data = {"track_title": entry["track_title"]}
        # ret = client.update_entry(query, data, "track_entries")# mongo_schema.trackSchema.schema)
        # print(entry["op_number"], ret)

