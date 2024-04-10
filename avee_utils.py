import traceback, datetime, pyautogui
import win32gui,pywintypes
import win32con,win32file,win32pipe,win32api, numpy, threading
import pygetwindow as gw
import time, subprocess as sp, mss
from PIL import Image
import logging
# time.sleep(1)
import os
os.environ['PATH'] = os.path.dirname('C:\Program Files\MediaInfo') + ';' + os.environ['PATH']
import MediaInfo
from pymediainfo import MediaInfo

import win32gui
import win32ui
import random
import autopyBot
at = autopyBot.autopy.autopy
#import autopy as at
#from autopy import background_screenshot, receive_screen_shot_from_phone

import time, shlex, shutil
import pywinauto, ctypes,win32process
from urllib.parse import quote
from collections import namedtuple
import app_env

def get_frame_count(file_path):
    # result = sp.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=nb_frames', '-of', 'default=nokey=1:noprint_wrappers=1', file_path], stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    # return int(result.stdout)
    import ffmpeg
    probe = ffmpeg.probe(file_path)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    return int(video_info['nb_frames'])

def join_video_files(folder_path, output_file, lengths, audio_file):
    files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
    if not files:
        print("No video files found in the folder.")
        return

    input_args = []
    filter_args = []
    input_index = 0
    for file in files:
        start_frame = 0#sum(get_frame_count(os.path.join(folder_path, f)) for f in files[:input_index])
        end_frame = lengths[input_index].dur_fps#start_frame + get_frame_count(os.path.join(folder_path, file))
        input_args.extend(['-i', os.path.join(folder_path, file)])
        filter_args.append(f'[{input_index}:v]trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS[v{input_index}]')
        input_index += 1
    
    # input_args.extend(["-i", audio_file])
    filter_complex = ';'.join(filter_args)
    concat_filter = f'{"".join([f"[v{i}]" for i in range(input_index)])}concat=n={input_index}:v=1:a=0[outv]'
    tmp_no_audio = "tmp//no_audio.mp4"
    cmd = ['ffmpeg']
    cmd.extend(input_args)
    cmd.extend(['-filter_complex', filter_complex+";"+concat_filter, '-map', '[outv]', tmp_no_audio, "-y"])
    print("cmd", cmd)
    print("cmd", " ".join(cmd))
    sp.run(cmd)
    cmd2 = [ "ffmpeg", "-i", tmp_no_audio,  "-i", audio_file,  "-map",  "0:v",  "-map", "1:a", "-c:v", "copy", output_file, "-y"]
    sp.run(cmd2)
    os.remove(tmp_no_audio)

    
# folder_path = f"{r"app_env.ld_shared_folder}\\output\\None_00024v2_s\\tmp"
# output_file = f"{r"app_env.ld_shared_folder}\\output\\None_00024v2_s\\"+'\\output.mp4'
#join_video_files(folder_path, output_file)
# #a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"


#nt = namedtuple("name_storage", "android_name win_name basename dirpath")
def get_duration(file, type="Video"):
    assert(type == "Video" or type == "Audio")
    media_info = MediaInfo.parse(file)
    for track in media_info.tracks:
        if track.track_type == type:
            print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "  "Format: {t.format}".format(t=track))
            return track.duration
           # print("Duration (raw value):", track.duration)
            #print("Duration (other values:")

class name_storage():
    def __init__(self, input_path, out, instance_name) -> None:
        self.input_path = input_path
        self.win_name = os.path.basename(input_path)
        self.android_name = shlex.quote(self.win_name)
        self.basename =  self.win_name.split(".")[0]
        self.android_basename =  shlex.quote(self.basename)
        self.dirpath = os.path.dirname(input_path)
        self.out_fld = f"{out}\\{instance_name}_{self.basename}\\".replace("\\\\", "\\")
        self.avee_final_file = f"{self.out_fld}\\{self.basename}_joined.mp4".replace("\\\\", "\\")
        self.avee_tmp_file = f"{self.out_fld}\\{self.basename}_tmp.mp4".replace("\\\\", "\\")

        self.dav_final_file = self.out_fld + "\\" +  f"{self.basename}_dav.mp4"
        self.instance_name = instance_name
        self.guessed_lyrics_file = self.dirpath + "\\" + self.basename + ".ass"
        print()

        


#device = "ce041714f506223101" # emulator-5554




# exe = r"F:\LDPlayer\LDPlayer9\dnplayer.exe"
# command = ['schtasks', '/run', '/tn', exe]
# sp.Popen(["cmd.exe", '/c', 'start']+command)

#hwnd, ld_win= restart_ld_player(hwnd = None )
nt = namedtuple("name_storage", "android_name win_name basename dirpath")

def is_ffmpeg_installed():
    try:
        sp.run(['ffmpeg', '-version'], stdout=sp.PIPE, stderr=sp.PIPE)
        return True
    except FileNotFoundError:
        return False

def get_window_handles_with_title(titles):
    handles = []
    for title in titles:
        def callback(handle, data):
            if win32gui.IsWindowVisible(handle) and title.lower() in win32gui.GetWindowText(handle).lower():
                obj = gw.Window(handle)
                if not obj in data:
                    data.append(gw.Window(handle))
            return True
        win32gui.EnumWindows(callback, handles)
    return handles
    
class avee_context():
    template_fld = f"{app_env.ld_shared_folder}\\AveeTemplate_normal"
    template_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(template_fld) if ".viz" in elem]
    
    def __init__(s, wid, hei, prefix, autopyFld) -> None:
        s.wid = wid
        s.hei = hei
        s.hwnd, s.ld_win= s.restart_ld_player(hwnd = None )
        print(s.ld_win.width,s.ld_win.height )
        win32gui.MoveWindow(s.hwnd, 0, 0, s.ld_win.width, s.ld_win.height, True)
        print(s.ld_win.width,s.ld_win.height )
        resolve_handles = get_window_handles_with_title(["DaVinci", "resolve", "project manager"])
        for w in resolve_handles:
            win32gui.MoveWindow(w._hWnd, s.ld_win.width, 0, w.width, w.height, True)

        windows = pyautogui.getAllWindows()

        for window in windows:
            if window.left < s.ld_win.width and window._hWnd != s.hwnd:
                window.moveTo(window.left + s.ld_win.width, window.top)

        s.prefix = prefix
        s.rg = (s.ld_win.topleft.x, s.ld_win.topleft.y, s.wid, s.hei)

        s.a = at(autopyFld, ext_src=s.hwnd, img_prefix=s.prefix) #w._hWnd
        s.a.default_region = s.rg
        
        s.device = "emulator-5554"
        s.adb_binary =  app_env.config["ADB_BINARY"]
        assert(os.path.isfile(s.adb_binary))
        assert(is_ffmpeg_installed())
        s.base = f"{s.adb_binary}  -s {s.device} shell "

        s.sleep_t = 0.1


    def xcoor(s, x):
        xx = x - s.ld_win.topleft.x
        return xx
    def ycoor(s, y):
        yy = y - s.ld_win.topleft.y
        return yy
    
    def tap(s, xy, x_of=0, y_of=0):
        if xy:  s.adb(f'input tap {s.xcoor(xy[0]) + x_of} {s.ycoor(xy[1]) + y_of}')
    
    def tap_rel(s,  xy, x_of=0, y_of=0):
        s.adb(f'input tap {xy[0] + x_of} {xy[1] + y_of}')

            
    def double_tap(s, xy, x_of=0, y_of=0):
        x = s.xcoor(xy[0]) + x_of
        y = s.ycoor(xy[1]) + y_of
        s.adb(f'"input tap {x} {y}& sleep 0.1; input tap {x} {y}"')

    def templ_cmd(s, templ):
        template_file_path = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + shlex.quote(templ.win_name) # CX%20liquify.viz"
        return f'am start -a android.intent.action.VIEW -d "{template_file_path}" -n com.daaw.avee/.MainActivity'

    def start_adb_server(s):
        os.system(f"{s.adb_binary} start-server ")
        os.system(f"{s.adb_binary} start-server ")

    def restart_ld_player(s, hwnd=None):
        # if hwnd:
        #     threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
        #     os.system(f"taskkill /PID {pid}")
        #     time.sleep(0.5)
        # process = sp.Popen(r"F:\LDPlayer\LDPlayer9\dnplayer.exe")
        # ldplayer_pid = process.pid
        # time.sleep(1)
        l = gw.getWindowsWithTitle("LDPlayer")
        while len(l) == 0:
            l = gw.getWindowsWithTitle("LDPlayer")
            logging.info("waiting for lplayer..")
            time.sleep(1)
        ld_win = l[0]
        hwnd = ld_win._hWnd

        return hwnd, ld_win
# wid = 540 
# hei = 960 +50
# r = (ld_win.topleft.x, ld_win.topleft.y, wid, hei)
#a.ext_src_buffer =  bytearray(wid*hei*3)

    def adb_output(s, cmd):
        process = sp.Popen(s.base + cmd,
                            shell=True,
                            stdout=sp.PIPE, 
                            stderr=sp.PIPE)

        out, err = process.communicate()
        errcode = process.returncode
        return out if len(out) else err

    def sub_output(s, cmd):
        process = sp.Popen(cmd, shell=True,  stdout=sp.PIPE, stderr=sp.PIPE)
        out, err = process.communicate()
        return out if len(out) else err

    def is_avee_running(s):
        ret =  s.adb_output(f"pidof com.daaw.avee")
        if ret != b'':
            return True
        return False
        
    def check_avee_running(s):
        
        if not s.is_avee_running():
            logging.debug("Avee not running, starting")
            os.system(f"{s.base} am start -a android.intent.action.VIEW -n com.daaw.avee/.MainActivity")
            ret = s.a.find(s.a.i.speaker, timeout=40, loop=3, region=s.rg, check_avee_running=False)
            time.sleep(4)
        else:
            logging.debug("Avee running")

    def reset_settings(s):
        settings_f = f"{app_env.ld_shared_folder}\\shared_prefs"
        for f in os.listdir(settings_f):
            bb = f"{s.adb_binary}  -s emulator-5554 shell" + f" su -c 'cp /storage/emulated/0/Pictures/shared_prefs/{f} /data/data/com.daaw.avee/shared_prefs;'"
            os.system(bb)

    def adb(s, cmd, shell=True):
        cmd_ =  (s.base if shell else  f"{s.adb_binary}  -s {s.device} ") + cmd
        os.system(cmd_)

    def is_device_awake(s):
        ret = s.adb_output('dumpsys power | find "mWakefulness="')
        if "Awake" in str(ret): return True
        return False

    def check_device_awake(s):
        if not s.is_device_awake():
            s.adb("input keyevent 26") #power
            logging.debug("powering up device")

    def is_device_ready(s):
        ret = s.adb_output("qwx")
        if "'emulator-5554' not found" in str(ret):
            return False
        return True

    def wait_for_device(s):
        while not s.is_device_ready():
            print("device not ready..")
            time.sleep(1)
        os.system(f"{s.adb_binary} start-server ")
        os.system(f"{s.adb_binary} start-server ")
        
    def update_file_system(s):
        s.adb("am start -n com.android.gallery3d/.app.GalleryActivity")

    def tab_scroll(s, target_file, suffix):
        global t0; 
        logging.debug(f"Tab scrolling ")
        
        #found  = s.a.find(s.a.i.end_check, loop=1, region=s.rg, grayscale=True)
        #if not found: raise Exception("End time of avee is not 1:55")

        found = s.a.find(s.a.i.file_name, loop=3, region=s.rg, grayscale=True)
        x =s.xcoor(found.found[0]+141)
        y = s.ycoor(found.found[1])
        cmd = f'"input tap {x} {y}& sleep 0.1; input tap {x} {y}"'
        s.adb(cmd)
        time.sleep(0.6)

        cmd = "input text " + f'{shlex.quote(f"{target_file.basename}_{suffix:02d}" )}'
        s.adb(cmd)

        if s.scroll(s.a.i.export2): return 

        logging.debug(f"Failed to find export button after pressing tab 20 times")

    def scroll(s, obj, click_it=True):
        found = None
        for x in range(20):
            s.adb(f" input keyevent 61") #tab
            found = s.a.find(obj, grayscale=True)
            if found:
                if click_it:
                    s.adb(f'input tap {s.xcoor(found.found[0])} {s.ycoor(found.found[1])}')
                t0 = time.time()
                return True
            time.sleep(0.1)
        return False

    def get_vars(s):
        return s.adb_binary, s.sub_output, s.base, s.wait_for_device, s.adb, s.device, s.reset_settings, s.check_avee_running, s.tab_scroll, s.a, s.is_avee_running

def avee_task(target_file, template_file, start, dur, suffix):
    
    actx = avee_context(hei= 960+50, wid=540, prefix="540p_", autopyFld="images_avee")
    adb_binary, sub_output, base, wait_for_device, adb, device, reset_settings, check_avee_running, tab_scroll, a, is_avee_running = actx.get_vars()

    
    os.system(f"{adb_binary} start-server ")
    os.system(f"{adb_binary} start-server ")

    while "'emulator-5554' not found" in str(sub_output(base + " ls")):
        time.sleep(1)
    if not os.path.isdir(os.path.join(target_file.out_fld, "tmp")): os.makedirs(os.path.join(target_file.out_fld, "tmp"))
   # os.makedirs(os.path.join(target_file.out_fld, ""))

    #target_file =  nt(shlex.quote(basef),basef, basef.split(".")[0], os.path.dirname(basef))
  
    file = "/mnt/shared/Pictures/" + target_file.android_name #file = "file:///mnt/shared/Pictures/" + random.choice(audio_list).android_name #00024.wav"
    #new_name_spl =  target_file.win_name.split(".")
    #new_name = new_name_spl[0] + "_new_." + new_name_spl[1]
    ex_file = "00000.mp3" if "mp3" in file else "00001.wav"
    file = "file:///mnt/shared/Pictures/" + ex_file# quote(new_name)

    file_cmd = f'{base} am start -a android.intent.action.VIEW -d "{file}" -n com.daaw.avee/.MainActivity'

    #template_file_path = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + template_file # shlex.quote(template_file)# CX%20liquify.viz"
    #f'{base} am start -a android.intent.action.VIEW -d "{template_file_path}" -n com.daaw.avee/.MainActivity'

    wait_for_device()
    os.system(f"ffmpeg -i {target_file.input_path } -ss {start} -t {dur} tmp\\{target_file.win_name} -y")
    assert(os.path.isfile(f"tmp\\{target_file.win_name}" ))
    adb("mkdir /mnt/sdcard/Pictures/output ")
    adb("mkdir /mnt/shared/Pictures/input ")
    adb("mkdir /mnt/shared/Pictures/input/audio ")
    adb("mkdir /mnt/shared/Pictures/input/templates")
    
    cmd = f'{adb_binary} -s {device} push ' +  "tmp\\"+ target_file.win_name   + ' /mnt/sdcard/Pictures/'+ex_file #(' /mnt/sdcard/Pictures/' +shlex.quote(ex_file))
    #print("####->", cmd)
    os.system(cmd)

    # actx.hwnd, actx.ld_win= actx.restart_ld_player()
    wait_for_device()
    #actx.a.ext_src = actx.hwnd

    adb("am force-stop com.daaw.avee")
    time.sleep(0.1)
    reset_settings()
    actx.update_file_system()
    time.sleep(1)
    check_avee_running()

    time.sleep(actx.sleep_t)

    check_avee_running()
    os.system(file_cmd)
    ret = a.find(a.i.pause, timeout=15, loop=0.5, region=actx.rg)
    adb(f'input tap {actx.xcoor(ret.found[0])} {actx.ycoor(ret.found[1])}')
    time.sleep(actx.sleep_t)

    check_avee_running()
    adb(actx.templ_cmd(template_file))
    time.sleep(actx.sleep_t)
    
    if not is_avee_running():
        logging.info(f" template crash? {template_file.win_name}")
    t0 = time.time()

    #find either the button to open export menu("export") or 
    # the final first line export video text("export tovideo file")
    found = a.find([a.i.export_to_video_file, a.i.export], timeout=40, loop=1, region=actx.rg, grayscale=True)
    if found:
        if  found == a.i.export_to_video_file:
            adb(f"input keyevent 4") #back
        found = a.find([a.i.export], loop=1, region=actx.rg, grayscale=True)
        if found:
            adb(f'input tap  {actx.xcoor(found.found[0])} {actx.ycoor(found.found[1])}')
    #    else:
    #scroll to find final export button
    adb('"cd /mnt/sdcard/Download && rm -rf *.mp4"')
    tab_scroll(target_file, suffix)

    found = a.find([a.i.blue_cross], loop=1, region=actx.rg, grayscale=True)

    #wait for encode to finish and click the ad cross button
    found = a.find([a.i.exporting_finished, a.i.export2], loop=5, timeout=5*60, region=actx.rg, grayscale=True)
    logging.info(f"encode took aprox {time.time() - t0}secs")
    ex_file_spl =  ex_file.split(".")

    inst_name =  target_file.instance_name #shlex.quote(target_file.instance_name)
    adb(f"mkdir /mnt/shared/Pictures/output/ ") 
    adb(f"mkdir /mnt/shared/Pictures/output/tmp ")
    #{inst_name}_{target_file.android_basename }/

    cmd = "mv " + f'"/mnt/sdcard/Download/{target_file.android_basename }_{suffix:02d}_0.mp4"' +  f" /mnt/shared/Pictures/output/tmp/"+ target_file.android_basename  + f"_{suffix:02d}.mp4" 
    #cmd = "mv " + f'"/mnt/sdcard/Pictures/output/{target_file.android_basename }_{suffix:02d}_0.mp4"' +  f" /mnt/shared/Pictures/output/{target_file.android_basename }/tmp/"+ target_file.android_basename  + f"_{suffix:02d}.mp4" 

    adb(cmd)
    src = f"{app_env.ld_shared_folder}\\output\\tmp\\{target_file.android_basename}_{suffix:02d}.mp4"
    dst = f"{app_env.output_folder}\\{inst_name}_{target_file.android_basename }\\tmp\\{target_file.android_basename}_{suffix:02d}.mp4"
    shutil.move(src, dst)
    if found: #and  
        if found == a.i.exporting_finished:
            time.sleep(1)
            adb(f" input keyevent 61") #back
            adb(f'input tap  {actx.xcoor(found.found[0]) +240 } {actx.ycoor(found.found[1] + 158)}')

        adb(f'input tap  {440} {610}')

    adb(f'input keyevent KEYCODE_HOME')




def handle_extra_frames(extra_fames, input_file, nb_tasks, black_f):

    if extra_fames > 0 or 1:
        cmd = f"ffmpeg.exe -loop 1 -i 1920x1080_black.png -t {0.016*abs(extra_fames*2)} -video_track_timescale 90k -s 1920x1080 -r 59.860 {black_f} -y "
        os.system(cmd)
    else:
        f = f"{input_file.out_fld}\\tmp\\{input_file.basename}_{nb_tasks-1:02d}.mp4"
        f2 = f"{input_file.out_fld}\\tmp\\{input_file.basename}_{nb_tasks-1:02d}_.mp4"
        dur = get_duration(f)
        os.rename(f, f2)
        #cmd =   f"ffmpeg -sseof -$ -i {f2} {f}"
        cmd = f"ffmpeg -ss 0 -t {(dur/1000) - 0.016*abs(extra_fames)} -i {f2} -profile:v baseline -level:v 4.1 {f}"

        os.system(cmd)
        os.remove(f2)

def perform_avee_task(input_file, bpm,  bars, bars_per_template, avee_fragments_info, extra_fames=0, beats_per_bar=4, fps=60):

    t1 = time.time()

    #first_start = start[0]*60+ start[1] + start[2]/1000

    logging.info(f"- task: {input_file.input_path} |  {bpm}bpm | custom_durs {[f'{e.dur:4.2f}' for e in avee_fragments_info]} | bars per template: {bars_per_template}, beats per bar: {beats_per_bar} " )
    time_per_beat = (fps/bpm)
    # dur = time_per_beat*beats_per_bar*bars_per_template
    # if dur > 110:
    #     raise Exception("duration is greater than 27 seconds, you'll have to fix the 'End at' bug in avee player again")
    nb_tasks = bars//bars_per_template
    
    black_f = f"{input_file.out_fld}\\black_f.mp4"

    for x in range(nb_tasks):
        for attempt_n in range(10):

            template = random.choice(avee_context.template_list) 

            logging.info(f"-- chunk {x} | start: {avee_fragments_info[x].audio_start} | template: {template.win_name} | dur: {avee_fragments_info[x].dur} | attempt: {attempt_n}" )
            try:
                out_file = f"{input_file.out_fld}\\tmp\\{input_file.basename}_{x:02d}.mp4"
                if os.path.isfile(out_file):
                    logging.info(f"Skipping chunk: {x}, already exists")
                    break
                avee_task(input_file, template, avee_fragments_info[x].audio_start, avee_fragments_info[x].dur*1.5, x)
                if x == nb_tasks-1:
                    handle_extra_frames(extra_fames, input_file, nb_tasks, black_f)
                break
            except Exception as e:
                logging.info(f"Error during chunk {x}: {e} , traceback:\n {traceback.format_exc()}")
                time.sleep(1)



    

    if not os.path.isfile(input_file.avee_final_file):
        if 1:
            join_video_files(input_file.out_fld + "\\tmp", input_file.avee_final_file, avee_fragments_info, input_file.input_path )
        else:
            handle_extra_frames(extra_fames, input_file, nb_tasks, black_f)
            logging.info("Joining parts and adding audio")
            paths = [os.path.join(input_file.out_fld + "\\tmp", elem).replace("\\\\", "\\")  for elem in os.listdir(input_file.out_fld + "\\tmp")]
            paths = [elem.replace("\\\\", "\\")  for elem in paths]
            with open(input_file.out_fld + "\\file_list.txt" , "w") as ff:
                for p in paths:
                    if ".mp4" in p:
                        pp = p.replace("\\", "\\\\")
                        ff.write("file " +  pp + "\n")
            #os.system(f"ffmpeg -i {target_file.input_path } -ss {start} -t {dur*bars} tmp\\{target_file.win_name} -y")
            tot_duration = avee_fragments_info[-1].audio_end - avee_fragments_info[0].audio_start 
            os.system(f"ffmpeg  -f concat -safe 0 -segment_time_metadata 1 -i {input_file.out_fld}\\file_list.txt  -ss {0} -t {tot_duration} -i {input_file.input_path}   -c:v copy -map 0:v -map 1:a -c:a aac -b:a 128k {input_file.avee_final_file} -y")
            print()
    else:
        logging.info("Joined file already exists, skipping")

    # if os.path.isfile(black_f):
    #     paths = [input_file.avee_tmp_file, black_f]
    #     with open(input_file.out_fld + "\\file_list.txt" , "w") as ff:
    #         for p in paths:
    #             if ".mp4" in p:
    #                 pp = p.replace("\\", "\\\\")
    #                 ff.write("file " +  pp + "\n")
    #     os.system(f"ffmpeg  -f concat -safe 0 -segment_time_metadata 1 -i {input_file.out_fld}\\file_list.txt  -ss {first_start} -t {dur*bars} -i {input_file.input_path}   -c:v copy -map 0:v -map 1:a -c:a aac -b:a 128k {input_file.avee_final_file} -y")



    

    t2 = time.time()
    logging.info(f"Time: avee= {str(datetime.timedelta(seconds=t2 -t1))}")


if __name__ == "__main__":
    
    print("")