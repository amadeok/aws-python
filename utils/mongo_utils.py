
import os, sys, eel
from bson import ObjectId
import logging, uuid, subprocess, copy
import utils.cloud_utils.mongo_client as mongo_client
import utils.cloud_utils.gdrive as gdrive
import utils.cloud_utils.mongo_schema as mongo_schema


def get_track_entries_(mongo):
    assert mongo
    payload = {}
    for name in mongo.collection_names:
        mongo.cd[name]  =  mongo.fetch_entries(name, None)

    tracks = copy.deepcopy(mongo.cd["track_entries"])
    attempts =copy.deepcopy( mongo.cd["upload_attempts"])
    sessions =copy.deepcopy( mongo.cd["upload_sessions"] )
    settings =copy.deepcopy( mongo.cd["settings"] )

    payload["track_entries"] = tracks
    payload["upload_attempts"] = attempts
    payload["upload_sessions"] = sessions
    payload["settings"] = settings

    attempts_ = attempts.copy()
    s = len(attempts_)-1
    while s >= 0:
        attempt = attempts_[s]
        for track in tracks:
            if attempt["track_entry_id"] == track["_id"]:
                track["upload_attempts"].append(attempt)
                break
        for session in sessions:
            if attempt["session_entry_id"] == session["_id"]:
                session["upload_attempts"].append(attempt)
                break
        s-=1
    

    # utils.merge_arrays(mongo.cd["track_entries"] , mongo.cd["upload_attempts"], "upload_attempts", "_id")
    # utils.merge_arrays(mongo.cd["upload_sessions"] , mongo.cd["upload_attempts"], "upload_attempts", "session_entry_id")
    for upload_session in sessions:
        for upload_attempt in upload_session["upload_attempts"]:
            if not upload_attempt["track_entry_id"] in upload_session["track_ids"]:
                upload_session["track_ids"].append(upload_attempt["track_entry_id"])

    # utils.merge_arrays(mongo.cd["upload_sessions"] , mongo.cd["track_entries"], "track_entries", "_id")

    payload["upload_sites"] = mongo_schema.upload_sites
    return payload