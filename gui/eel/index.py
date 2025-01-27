import logging

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Application started")
logging.debug("Debug information")
logging.error("An error occurred")

import subprocess
import sys, time, os
import uuid
#import threading
from bson import ObjectId

#import pyautogui
sys.path.append('../../')  # Adds the parent directory to the Python path
#sys.path.insert(1, r'F:\all\GitHub\Eel')
#import app_logging
import eel, copy, logging
logging.info("111")
import utils
logging.info("222")

from utils.cloud_utils.mongo_client import MongoDBClient
import utils.cloud_utils.mongo_schema as mongo_schema
import utils.cloud_utils.gdrive as gdrive
from utils.eel_utils import setMongoInstance, set_file_logging


formatter = '%(asctime)s - %(message)s' #- %(name)s - %(levelname)s 
handlers = []
#handlers.append(logging.FileHandler('app.log'))
handlers.append(logging.StreamHandler())
logging.basicConfig(    level=logging.INFO,    format=formatter,    handlers=handlers)

#import provision

from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("MONGODB_URI")
assert(uri)
if __name__ == '__main__':
    mongo = MongoDBClient(uri, 'social-media-helper',
                             {'track_entries': mongo_schema.trackSchema.schema, 
                              "upload_attempts": mongo_schema.uploadAttempt.schema,
                              "upload_sessions": mongo_schema.uploadSession.schema,
                              "settings": None} )

    if hasattr(sys, "_MEIPASS"): # if the script is started from an executable file
        with open("logs.txt", "a") as f_logs:
            sys.stdout = f_logs
            sys.stderr = f_logs
            
    setMongoInstance(mongo)

    try:
        
        mode = "None" #edge
        react_port = 3560
        if  len(sys.argv)>1 and sys.argv[1] == '--develop':
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            fld = "src" if os.path.isdir("src") else r"gui\eel\src"
            eel.init(fld)
            eel.start({"port": react_port}, host="localhost", port=8888, mode=mode)
        elif 0:
            # eel.init('build')
            # eel.start('index.html', host="localhost", port=8888, mode=mode)
            logging.info("---init")
            eel.init('build')
            eel.start({"port": react_port}, host="localhost", port=8888)          
            logging.info("---after eel start")
        else:
            eel.init('build', ['.tsx', '.ts', '.jsx', '.js', '.html'])
            eel_kwargs = dict(
            host='localhost',
            port=8888,
            size=(1280, 800),
            )   
            set_file_logging()

            def test(a, b):
                logging.info(f"------------CLOSED {a}, {b}")
                # sys.exit()
            eel.start('index.html',  **eel_kwargs,  close_callback=test, mode= mode)#,  browser="new window") #mode= 'edge',

            #eel.start('index.html', block=True, options={'port': 80, 'host': '0.0.0.0', 'close_callback': lambda: print("------------CLOSE"), 'mode': False})
            logging.info("---after eel start")
    except Exception as e:
        logging.error(f"exception at index main function of index.py: {e}")



