# coding: utf-8
import sys, threading, time, os
from mongo import MongoDBClient

#sys.path.insert(1, r'F:\all\GitHub\Eel')
import eel

uri = os.getenv("MONGODB_URI")
mongo_client = MongoDBClient(uri, 'social-media-helper', 'track-tasks')

if hasattr(sys, "_MEIPASS"): # if the script is started from an executable file
    with open("logs.txt", "a") as f_logs:
        sys.stdout = f_logs
        sys.stderr = f_logs
        


@eel.expose
def hello():
    print('hello23123123123')

@eel.expose
def get_track_entries():
    entries =  mongo_client.fetch_entries()
    return entries

def d():
    n = 0
    while 1:
        time.sleep(2)
        try:
            payload = {"count": n}
            #eel.console_log(payload)
            #eel.setCompState(payload)
            n+=1
        except Exception as e: print("e", e)
    
threading.Thread(target=d).start()

if __name__ == '__main__':
    if sys.argv[1] == '--develop':
        eel.init('src')
        eel.start({"port": 3000}, host="localhost", port=8888, mode="edge")
    else:
        eel.init('build')
        eel.start('index.html', host="localhost", port=8888, mode="edge")
