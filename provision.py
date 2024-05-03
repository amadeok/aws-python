from itertools import groupby
import math
import os
import time
import traceback
from bson import ObjectId
from dotenv import load_dotenv
import app_logging
import logging, json, dateutil
from utils.cloud_utils.gdrive import download_file
from utils.eel_utils import get_track_entries, initMongoInstance
import utils.cloud_utils.mongo_schema as mongo_schema
import uploader, base
from datetime import timedelta, datetime
import datetime as datetime_parent
from utils.provision_utils import gs, break_down_delta, round_time, calculate_times_per_day, print_debug_setup_times, break_down_time_settings, start_processes

def provision(dummy=False, payload=None):
    print(f"provision {dummy}")
    if not payload:
        payload = get_track_entries()
    json_string = json.dumps(payload, indent=4)
    #json_data = json.loads(payload)

    print()
    logging.info(f"payload {json_string}")
    
    print()
    for e in payload["track_entries"]:
        ret = [attempt.get("error") != "" for attempt in e.get("upload_attempts", [])]
        #print(any(ret), ret)
    print()
    
    track_entries = payload["track_entries"]
    upload_sites = payload["upload_sites"]
    upload_sessions = payload["upload_sessions"]
    upload_attempts = payload["upload_attempts"]
    
    uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h = break_down_time_settings(payload) #minimum_upload_frequency_h

    #print_time_setup(uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h)

    logging.info("")
    
    for u in upload_attempts:
        u["date"] = dateutil.parser.parse(u["date"]) 
    for t in track_entries:
        t["insertion_date"] = dateutil.parser.parse(t["insertion_date"]) 
    for u in upload_sessions:
        u["date"] = dateutil.parser.parse(u["date"])      
        
    entries_with_no_upload_attempts = [entry for entry in track_entries if not entry.get("upload_attempts")]
    entries_with_no_upload_attempts_and_not_ready = [entry for entry in entries_with_no_upload_attempts if entry.get("entry_status") != "ready"]


    tracks_with_unresolved_errors = [] #tracks which have sites that failed to upload after all attempts
    for entry in track_entries:
        attempts = entry.get("upload_attempts", [])

        attempts.sort(key=lambda x: x['site'])

        grouped_data = {key: list(group) for key, group in groupby(attempts, key=lambda x: x['site'])}

        uploads_ended_with_error = []
        print(f'entry: {entry["track_title"]}')
        for site, values in grouped_data.items():
            #print(f"Site: {site}")
            sorted_attempts = sorted(values, key=lambda x: x.get("date", ""), reverse=True)
            most_recent_elem = sorted_attempts[0]
            if len(sorted_attempts) and len(most_recent_elem.get("error")):
                uploads_ended_with_error.append(site)#{"site":site, "error": most_recent_elem["error"]})
                print(f"site {site} ended with error {most_recent_elem['error']}")
                        
        if len(uploads_ended_with_error):
            tracks_with_unresolved_errors.append({"track_entry":entry, "sites": uploads_ended_with_error, "reason": "upload_with_errors"})
        
    tracks_missing_attempts = []

    for entry in track_entries:
        missing_sites = [site for site in upload_sites if not any(attempt.get("site") == site for attempt in entry.get("upload_attempts", []))]
        if missing_sites:
            tracks_missing_attempts.append({"track_entry" : entry, "sites":missing_sites, "reason": "missing_sites"})

    logging.info(f"tracks_missing_attempts  {  json.dumps(tracks_missing_attempts, indent=4,  sort_keys=True, default=str)}" )

    #logging.info(f"with errors {  json.dumps(track_entries_with_errors, indent=4)}" )
    #logging.info(f"no_upload {  json.dumps(entries_with_no_upload_attempts, indent=4)}" )

    logging.info(f"Number of tracks without upload attempts {len(entries_with_no_upload_attempts)}" )
    logging.info(f"Number of tracks without upload attempts and not ready {len(entries_with_no_upload_attempts_and_not_ready)}" )
    logging.info(f"Number of tracks with missing attempts {len(tracks_missing_attempts)}" )
    logging.info(f"Number of tracks with unresolved errors in upload attempts {len(tracks_with_unresolved_errors)}" )
    logging.info(f"" )

    most_recent_upload_times = {key:  timedelta(days=365) for key in upload_sites}#datetime.now() -

    upload_attempts.sort(key=lambda x: x['site'])
    upload_attempts_grouped_by_site = {key: list(group) for key, group in groupby(upload_attempts, key=lambda x: x['site'])}
    for site, values in upload_attempts_grouped_by_site.items():
        sorted_attempts = sorted(values, key=lambda x: x.get("date", ""), reverse=True)
        
        first_empty_error = next((item for item in sorted_attempts if item["error"] == ""), None)
        if not first_empty_error:
            logging.info(f"""->No upload attempt for {(site):<10} without error found""")
            continue
        date = first_empty_error.get("date")
        now = datetime.now(datetime_parent.timezone.utc)     
        delta = (now - date)
        years, months, days, hours, minutes, string = break_down_delta(delta)
        
        logging.info(f"""Most recent {(site):<10} upload attempt without error was {date.astimezone().strftime("%d-%m-%Y %H:%M")} ({string} ago)""")
        most_recent_upload_times[site] = delta
        
            
    for us in upload_sites:
        if not us in upload_attempts_grouped_by_site.keys():
            logging.info(f"->{(us):<10} has no recorded upload attempts")
    logging.info(f"" )

    upload_frequency_d = timedelta(hours=math.floor(minimum_upload_frequency_h), minutes=(minimum_upload_frequency_h*60)% 60 )
    logging.info(f"""Minimum upload frequency {gs(upload_frequency_d.days, "d")}{gs(upload_frequency_d.seconds // 3600, "h")}{gs((upload_frequency_d.seconds // 60) %60, "m")} """)
    logging.info(f"" )

    sites_available_for_upload = [ k for k, e in most_recent_upload_times.items() if e > upload_frequency_d]
        
    tracks_need_to_upload = tracks_missing_attempts + tracks_with_unresolved_errors
    
    for t in reversed(tracks_need_to_upload):
        if t["track_entry"]["entry_status"] == "pending":
            logging.info(f"""Discarding task({t["reason"]}) of track "{t["track_entry"]["track_title"]}" because track entry status is pending""")
            tracks_need_to_upload.remove(t)
            continue
        for s in reversed(t["sites"]):
            if not s in sites_available_for_upload:
                logging.info(f"""Discarding task({t["reason"]}) of track "{t["track_entry"]["track_title"]}" because site {s} is too soon to upload""")
                t["sites"].remove(s)
                
    
    tracks_need_to_upload_sorted_by_date = sorted(tracks_need_to_upload, key=lambda x: x["track_entry"]["insertion_date"])
    
    sites_already_set = []
    #[print(t["track_entry"]["insertion_date"]) for t in tracks_need_to_upload_sorted_by_date]
    for t in tracks_need_to_upload_sorted_by_date:
        #print(t["track_entry"]["insertion_date"])
        for s in reversed(t["sites"]):
            if not s in sites_already_set:
                sites_already_set.append(s)
            else:
                logging.info(f"""Discarding task({t["reason"]}) of track "{t["track_entry"]["track_title"]}" because there's already a task  for site {s} in this session""")
                t["sites"].remove(s)
           
    if not len(tracks_need_to_upload_sorted_by_date):
        logging.info("##### No tasks ####\n")
        return  payload, None
    
    processes = start_processes()

    upload_tasks_n = 0
    for t in tracks_need_to_upload_sorted_by_date: upload_tasks_n+= len(t["sites"])
    

    logging.info(f"##### {len(tracks_need_to_upload_sorted_by_date)} task group(s), {upload_tasks_n} available task(s) #####\n")
    #tasks = [uploadTaskGroup(uploader.taskPayload(track_title=t["track_entry"]["track_title"], upload_file=f'{tmp_fld}{os.path.basename(t["track_entry"]["file_details"]["file_path"])}', hashtag_map=hashtag_map), t["reason"], t["track_entry"], t["site"]) for t in tracks_need_to_upload_sorted]
    tmp_fld = "audio_input_tmp/"
    if not os.path.isdir(tmp_fld): os.mkdir(tmp_fld)
    
    # for t in tracks_need_to_upload_sorted_by_date:
    #     t["payload"]= uploader.taskPayload(track_title=t["track_entry"]["track_title"], upload_file=os.path.abspath(f'{tmp_fld}{os.path.basename(t["track_entry"]["file_details"]["file_path"])}'))
    for i, t in enumerate(tracks_need_to_upload_sorted_by_date):
        print_task_group(t, i)
#        print(t) 
        
    logging.info(f"##### #### #####")
    logging.info("")
    
    uploadSessionObj =  mongo_schema.uploadSession.create( datetime.now(datetime_parent.timezone.utc).isoformat(), [], [], [])
    new_session_res = mongo.create_entry(uploadSessionObj, "upload_sessions", mongo.schemas["upload_sessions"])
    logging.info(f"""Created upload session entry with id  {new_session_res.inserted_id}""")

    logging.info("Starting tasks..")

    for i, t in enumerate(tracks_need_to_upload_sorted_by_date):
        print_task_group(t, i)
        input_audio_file = os.path.abspath(f'{tmp_fld}{os.path.basename(t["track_entry"]["file_details"]["file_path"])}')
        if not download_file(t["track_entry"]["file_details"]["drive_id"], input_audio_file):
            logging.error("Failed to download file from drive, skipping")
            continue
        assert(os.path.isfile(input_audio_file))
        try:
            ctx = base.general_task(input_audio_file, add_text=True, cloud_file_details=t["track_entry"]["file_details"])
        except Exception as e:
            logging.error(f"Error during general task {traceback.format_exc()}")
            uploadSessionObj["pre_upload_errors"].append({"error": str(traceback.format_exc()), "session_entry_id": str(new_session_res.inserted_id)})
            update_result = mongo.update_entry({"_id": ObjectId(new_session_res.inserted_id)}, uploadSessionObj, "upload_sessions", mongo.schemas["upload_sessions"])
            logging.info(f"Update operation for upload session with pre-upload error { update_result.modified_count if update_result else 'Nothing updated'}")
            continue
        main_yt_id = "UCdeGgQuczwgU8H-GaMrdLzw"

        t["payload"]= uploader.taskPayload(channel_id=main_yt_id, track_title=t["track_entry"]["track_title"], upload_file=os.path.normpath(ctx.input_f.dav_final_file) )
        mongo_context = {"client": mongo, "session_id": new_session_res.inserted_id, "track_id": t["track_entry"]["_id"]}
        uploader.perform_upload_tasks(t["payload"], t["sites"], mongo_context )
        
    logging.info("All tasks returned")
    
    return payload, processes




def print_task_group(t, i):
    #json_string = json.dumps(t, indent=4, sort_keys=True, default=str)
    entry = t["track_entry"]
    logging.info(f"""Task group {i} | track title: {entry["track_title"]} | _id: {entry["_id"]} | reason: {(t["reason"]):<20} | ins. date: {entry["insertion_date"].astimezone().strftime("%d-%m-%Y %H:%M")}""" )#| sites: {t["sites"]}
    logging.info(f"""Task group {i} | sites {t["sites"]}\n""" )     
  
    
def do_provision():
    global mongo
    load_dotenv()  
    uri = os.getenv("MONGODB_URI")
    
    # with open('data\hashtag_map.json', 'r') as file:
    #     hashtag_map = json.load(file)

    mongo =  initMongoInstance(uri, 'social-media-helper',
                             {'track_entries': mongo_schema.trackSchema.schema, 
                              "upload_attempts": mongo_schema.uploadAttempt.schema,
                              "upload_sessions": mongo_schema.uploadSession.schema, 
                              "settings" : None} )
    #time.sleep(5)
    return provision()

if __name__ == '__main__':
    do_provision()
    

# class uploadTaskGroup():
#     def __init__(self, p, r, t, s) -> None:
#         self.payload = p
#         self.reason= r
#         self.track_entry = t
#         self.sites = s
#     def __str__(self) -> str:
#         pass
