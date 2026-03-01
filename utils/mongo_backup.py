import subprocess
import datetime
import os
import dotenv

def backup_mongo_cluster(uri,  backup_dir="C:\\MongoBackups"):

    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H.%M.%S")
        
    backup_path = os.path.join(backup_dir, f"ClusterBackup_{dt_string}") + ".gz"
    backup_path_sl = backup_path.replace("\\", "/")
    # os.makedirs(backup_path, exist_ok=True)

    command = [
        mongodump_bin,
        "--uri="+f'{uri}',
        "--archive=" +f'"{backup_path_sl}"',
        "--gzip"
    ]

    try:
        subprocess.run(command,  check=True)
        print(f"Backup successful! Stored at: {backup_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    uri = os.getenv("MONGODB_URI")
    assert uri
    mongodump_bin = os.path.expandvars( r"C:\Users\%username%\mongodb-database-tools-windows-x86_64-100.11.0\bin\mongodump.exe")
    backup_folder = os.path.expandvars( r"C:\Users\%username%\Documents\Studio One\Songs\mongodb_backup")
    backup_mongo_cluster(uri,backup_folder)
