import os, sys
sys.path.insert(0, r"F:\all\GitHub\aws-python")

from bson import ObjectId
import utils.mongo_utils as mongo_utils
import utils.cloud_utils.mongo_schema as mongo_schema
import utils.cloud_utils.mongo_client as mongo_client, os, sys
from dotenv import load_dotenv
load_dotenv()





def find_folders_with_mixdown_files(root_dir, iterations=3, subfolder="Mixdown"):

    folders_with_files = []
    
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        
        if not os.path.isdir(folder_path):
            continue
            
        for x in range(1, iterations + 1):
            iteration_path = os.path.join(folder_path, subfolder, f"it{x}")
            
            if os.path.exists(iteration_path) and os.path.isdir(iteration_path):
                if any(os.path.isfile(os.path.join(iteration_path, f)) for f in os.listdir(iteration_path)):
                    folders_with_files.append(f"{folder_name}, {x}{'' if x == 1 else ' - '}")
                    break
                    
    return folders_with_files

def find_duplicates(items):
    seen = set()
    duplicates = [item for item in items if item in seen or seen.add(item)]
    duplicate_counts = {item: items.count(item) for item in set(duplicates)}
    return duplicates, duplicate_counts

def print_results(folders_with_files, duplicates, duplicate_counts):
    if folders_with_files:
        print("Folders containing files in Mixdown\\itX:")
        for folder in sorted(set(folders_with_files)):
            print(f"- {folder}")
    else:
        print("No folders found with files in Mixdown\\itX.")

    if duplicates:
        print("\nDuplicates found in folders_with_files:")
        for dup in sorted(set(duplicates)):
            print(f"- {dup} (appeared {duplicate_counts[dup]} times)")
    else:
        print("\nNo duplicates found in folders_with_files.")
        
    print(f"Total folders found: {len(folders_with_files)}")

def main():
    root_dir = os.path.expandvars( r"C:\Users\%username%\Documents\Studio One\Songs\newstart")
    folders_with_files = find_folders_with_mixdown_files(root_dir)
    duplicates, duplicate_counts = find_duplicates(folders_with_files)
    print_results(folders_with_files, duplicates, duplicate_counts)
    
    uri = os.getenv("MONGODB_URI")

    client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )
    
    database = mongo_utils.get_track_entries_(client)
    entries = database["track_entries"]
    missing = []
    for folder in folders_with_files:
        fld_n = int(folder.split(",")[0])
        found = False
        for entry in entries:
            if entry["op_number"] == fld_n:
                found = True
        if not found:
            missing.append(fld_n)
            
    print("missing", missing)
    

if __name__ == "__main__":
    main()