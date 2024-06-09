import random
import os, sys, subprocess, logging, threading, psutil
import time
from dotenv import load_dotenv
import tempfile
import app_logging
import utils.process_videos as pv
import pygetwindow as gw
from pydub import AudioSegment

def kill_ffmpeg_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "ffmpeg" in proc.info['name']:#== 'ffmpeg':
                print(f"Killing process {proc.info['pid']} ({proc.info['name']})")
                os.system(f"taskkill /PID {proc.info['pid']}")
                #os.kill(proc.info['pid'], 9)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle cases where the process no longer exists, cannot be accessed, or is a zombie
            pass
        
def update_config(file_path, variables_to_update, out_file):
    # Step 1: Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Step 2: Parse the content and update/add variables
    updated_lines = []
    existing_variables = set()
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith('#'):
            var_name, var_value = stripped_line.split('=', 1)
            var_name = var_name.strip()
            var_value = var_value.strip()
            if var_name in variables_to_update:
                var_value = variables_to_update[var_name]
                del variables_to_update[var_name]  # Remove it from the list once updated
            updated_lines.append(f"{var_name}={var_value}\n")
            existing_variables.add(var_name)
        else:
            updated_lines.append(line)
    
    # Step 3: Add the variables that were not found in the file
    for var_name, var_value in variables_to_update.items():
        updated_lines.append(f"{var_name}={var_value}\n")
    
    def remove_carriage_returns(string_list):
        return [s.replace('\r', '') for s in string_list]

    updated_lines = remove_carriage_returns(updated_lines)
        
    
    # Step 4: Write the updated content back to the file
    with open(out_file, 'w') as file:
        file.writelines(updated_lines)
        
    # with open(out_file, 'r') as file:
    #     data = file.readlines()


def remove_carriage_returns(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Remove all \r characters
        content = content.replace('\r', '')
        
        with open(file_path, 'w') as file:
            file.write(content)
        
        logging.info(f"All '\\r' characters have been removed from {file_path}.")
    except Exception as e:
        logging.info(f"An error occurred: {e}")


   
def error_checker():
    global stop
    global pid
    logging.info("error checker started")
    error_log_f = tempfile.gettempdir() + "/Temp/STREAM_PIANO_ERROR.txt"

    while not stop:
        if os.path.isfile(error_log_f):
            with open(error_log_f, 'r') as file:
                data = file.read()
                os.kill(pid, -9)
                raise Exception("Stream piano error: " + data)
        time.sleep(1)
    logging.info("error checker ended")



def get_audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    length_in_seconds = len(audio) / 1000.0
    return length_in_seconds


def unreal_task(input_video_file, input_midi_file, output_file, audio_file, keyBPrange=(0, 9), extra_settings ={}):
    global stop
    global pid
    stop = False
    logging.info(f"Performing unreal task, in video {input_video_file}, in midi, {input_midi_file},  out file, { output_file}")
    
    error_log_f = tempfile.gettempdir() + "/Temp/STREAM_PIANO_ERROR.txt"
    if os.path.isfile(error_log_f): os.remove(error_log_f)
    t = threading.Thread(target=error_checker)
    t.start()
    
    pianoKeyBP  = random.randint(keyBPrange[0], keyBPrange[1])
    #pianoKeyBP=9
    
    variables_to_update = {
    "r.InputAudioFilePath": audio_file,
    'r.InputMidiFilePath': input_midi_file,
    'r.InputVideoFilePath': input_video_file,
    "r.ffmpegOutFilePath": output_file,
    "r.pianoKeyBP":pianoKeyBP,
    "r.CustomMaxOutputVideoLenght": get_audio_length(audio_file)
    }
    variables_to_update.update(extra_settings)
    
    ini_defaults = os.environ['STREAM_PIANO_INI_VARS_FILE_DEFAULTS']
    
    update_config(ini_defaults, variables_to_update, "unreal.ini")

    load_dotenv()  
    unreal_ini = os.path.abspath("unreal.ini")
    assert(os.path.isfile(unreal_ini))
    os.environ['STREAM_PIANO_INI_VARS_FILE'] = unreal_ini# #r"C:\Users\%USERNAME%\Documents\Unreal Projects\stream_piano\Content\Debug\RuntimeVarsInit.ini"

    move_unreal = int(os.getenv("MOVE_UNREAL"))

    # uri = os.getenv("STREAM_PIANO_INI_VARS_FILE")
    bin = os.getenv("STREAM_PIANO_BIN")
    bin_dev = os.getenv("STREAM_PIANO_BIN_DEV")

    cmd = [bin,  "-windowed", "resx=1280", "resy=720"]
    proc = subprocess.Popen(cmd)
    pid = proc.pid
    if move_unreal:
        windows = []
        while not len(windows):
            windows = gw.getWindowsWithTitle("stream_piano")
        windows[0].moveTo(1921, 1080)

    proc.wait()
    stop = True
    t.join()


if __name__ == "__main__":
    #files = pv.get_sm_videos()
    # with open("get_sm_videos.txt", 'w') as file:
    #     for line in files:
    #         file.write(f"{line}\n")
            
    with open("get_sm_videos.txt", 'r') as file:
        files = file.readlines()
        
    index = 0
    tmp_index_file =  os.path.join(tempfile.gettempdir(), "tmp_index_file.txt")
    if not os.path.isfile(tmp_index_file):
        with open(tmp_index_file, 'w') as file:
            file.write(f"0")
    else:
        with open(tmp_index_file, 'r') as file:
            index =  int(file.read())
    index = 0
    midi_file = ""#r"C:\Users\%USERNAME%\Documents\dawd\Exported\00001 Forest Walk short.mid"
    video_file =  files[index] #r"random"
    audio_file = r"C:\Users\%USERNAME%\Downloads\00001 Forest Walk short.wav"
    #video_file = r"C:\Users\%USERNAME%\Videos\social_media_videos\vertical\183967\moon_trees_forest__183967-872226594_small.mp4"
    #video_file = r"C:\Users\%USERNAME%\Videos\social_media_videos\horizontal\150154\window_snow__150154-797999306_small.mp4"
    final_file = r"C:\Users\%USERNAME%\Videos\ptest.mp4"
    # pianoKeyBP  = random.randint(0, 9)
    
    # update_config('unreal_defaults.ini', variables_to_update, "unreal.ini")
    while 1:
        logging.info(f"Index {index}")
        video_file =  files[index] #r"random"
        kill_ffmpeg_processes()
        unreal_task(video_file, midi_file, final_file,audio_file,  (3, 3), {"r.InputMidiDevice":"clone 1", "r.InputMidiDevice":"clone 1", "r.bPrintRvars":"1", "r.fitKeysForShortFormat":"2" })
        index+=1
        with open(tmp_index_file, 'w') as file:
            file.write(str(index))
            
    