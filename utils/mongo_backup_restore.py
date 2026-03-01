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

# if __name__ == "__main__":
#     dotenv.load_dotenv()
#     uri = os.getenv("MONGODB_URI")
#     assert uri
#     mongodump_bin = os.path.expandvars( r"C:\Users\%username%\mongodb-database-tools-windows-x86_64-100.11.0\bin\mongodump.exe")
#     backup_folder = os.path.expandvars( r"C:\Users\%username%\Documents\Studio One\Songs\mongodb_backup")
#     backup_mongo_cluster(uri,backup_folder)


#!/usr/bin/env python3
import subprocess
import argparse
from pathlib import Path

def restore_mongodb(backup_path, uri, drop=False, gzip=True, archive_mode=False):
    """
    Restore MongoDB from backup using mongorestore
    
    Args:
        backup_path (str): Path to backup file or directory
        uri (str): MongoDB connection URI
        drop (bool): Drop collections before restore
        gzip (bool): Enable gzip compression
        archive_mode (bool): Whether backup is a single archive file
    """
    try:
        # Build the mongorestore command
        cmd = [bin_]
        
        if uri:
            cmd.extend(["--uri", uri])
        
        if drop:
            cmd.append("--drop")
        
        if gzip:
            cmd.append("--gzip")
        
        if archive_mode:
            cmd.extend([f"--archive={str(backup_path)}"])
        else:
            cmd.extend(["--dir", str(backup_path)])
        
        # Run the command
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Restore completed successfully!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Restore failed with error: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    bin_ = os.path.expandvars( r"C:\Users\%username%\mongodb-database-tools-windows-x86_64-100.11.0\bin\mongorestore.exe")
    uri = os.getenv("MONGODB_URI")
    file = os.path.expandvars( r"C:\Users\%username%\Documents\Studio One\Songs\mongodb_backup\ClusterBackup_2025-02-26_11.23.04.gz")
    
    parser = argparse.ArgumentParser(description="MongoDB Restore Script")
    parser.add_argument("--backup_path", help="Path to backup file or directory", default=None)
    parser.add_argument("--uri", help="MongoDB connection URI", default=None)
    parser.add_argument("--drop", help="Drop collections before restore", action="store_true", default=True)
    parser.add_argument("--gzip", help="Enable gzip compression", action="store_true", default=True)
    parser.add_argument("--archive", help="Backup is a single archive file", action="store_true", default=True)
    
    args = parser.parse_args()
    
    path = args.backup_path or file
    backup_path = Path(path)
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup path {backup_path} does not exist")
    
    restore_mongodb(
        backup_path=path,#args.backup_path,
        uri=args.uri or uri,
        drop=args.drop,
        gzip=args.gzip,
        archive_mode=args.archive
    )