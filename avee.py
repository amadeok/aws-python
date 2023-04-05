import win32gui,pywintypes
import win32con,win32file,win32pipe,win32api, numpy, threading
import pygetwindow as gw
import time, subprocess as sp, mss
from PIL import Image
import logging
# time.sleep(1)

import win32gui
import win32ui
import random, traceback
import autopy as at
from autopy import background_screenshot, receive_screen_shot_from_phone
import urllib.parse

import time, shlex
import pywinauto, ctypes, os,win32process
from urllib.parse import quote
from collections import namedtuple

#!/usr/bin/env python

from avee_utils import *

#a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"

#background_screenshot(hwnd, wid, hei+52,True)
#ret = receive_screen_shot_from_phone(save_file=True)

#check_device_awake()



template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

nt = namedtuple("name_storage", "android_name win_name basename dirpath")

template_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(template_fld)]
audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

andr_input_fld = "/mnt/shared/Pictures/"


f = "00000(2).wav"
#f = random.choice(os.listdir(audio_fld))
input_file = audio_fld + "//" + f

#temp_file = "file:///mnt/sdcard/input/templates/AveeTemplate_normal/" + random.choice(template_list).android_name # CX%20liquify.viz"
#target_file =  random.choice(audio_list)
template =  "The fuzzy lear.viz"#random.choice(template_list).win_name 


try: os.mkdir("tmp")
except: pass

out = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\\"




def perform_avee_task(input_file, bpm, start, bars, bars_per_template, beats_per_bar=4):

    first_start = start[0]*60+ start[1] + start[2]/1000

    logging.info(f"- task: {input_file.input_path} |  {bpm}bpm | start {first_start} 00:{start[0]}:{start[1]}.{start[2]} | bars per template: {bars_per_template}, beats per bar: {beats_per_bar} " )
    time_per_beat = (60/bpm)
    dur = time_per_beat*beats_per_bar*bars_per_template

    nb_tasks = bars//bars_per_template

    for x in range(nb_tasks):
        for attempt_n in range(10):

            template = random.choice(template_list).win_name 

            logging.info(f"-- chunk {x} | start: {first_start + x*dur} | template: {template} | dur: {dur} | attempt: {attempt_n}" )
            try:
                out_file = f"{input_file.out_fld}\\tmp\\{input_file.basename}_{x:02d}.mp4"
                if os.path.isfile(out_file):
                    logging.info(f"Skipping chunk: {x}, already exists")
                    break
                avee_task(input_file, template, first_start + x*dur, f"{dur}", x)
                break
            except Exception as e:
                logging.info(f"Error during chunk {x}: {e} , traceback:\n {traceback.format_exc()}")
                time.sleep(1)


    if not os.path.isfile(input_f.avee_final_file):
        logging.info("Joining parts and adding audio")
        paths = [os.path.join(input_f.out_fld + "\\tmp", elem).replace("\\\\", "\\")  for elem in os.listdir(input_f.out_fld + "\\tmp")]
        paths = [elem.replace("\\\\", "\\")  for elem in paths]
        with open(input_f.out_fld + "\\file_list.txt" , "w") as ff:
            for p in paths:
                if ".mp4" in p:
                    pp = p.replace("\\", "\\\\")
                    ff.write("file " +  pp + "\n")
        #os.system(f"ffmpeg -i {target_file.input_path } -ss {start} -t {dur*bars} tmp\\{target_file.win_name} -y")
        os.system(f"ffmpeg  -f concat -safe 0 -i {input_f.out_fld}\\file_list.txt  -ss {first_start} -t {dur*bars} -i {input_f.input_path}   -c:v copy -map 0:v -map 1:a -c:a aac -b:a 128k {input_f.avee_final_file} -y")
        print()
    else:
        logging.info("Joined file already exists, skipping")



bpm = 80
s_m = 0
s_sec = 23
s_ms = 974
bars=8
bars_per_template=1
beats_per_bar = 4
input_f = name_storage(input_file, out)
fps = 60#59940/1000

time_per_beat = (60/bpm)
frames_per_beat = fps*time_per_beat
frames_per_bar = frames_per_beat*beats_per_bar
transition_delta = frames_per_bar*bars_per_template

perform_avee_task(input_f, bpm, (s_m, s_sec, s_ms), bars, bars_per_template, beats_per_bar=beats_per_bar)

#avee_task(input_file, template, f"00:{s_m}:{s_sec}.{s_ms}", f"{dur}" )#f"00:00:{e_sec}.{e_ms}")
#avee_task(input_file, template, s_s_tot, f"{dur}",  )#f"00:00:{e_sec}.{e_ms}")


import DaVinciResolveScript as dvr_script
import spline
resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()
f = fusion.GetGlobalPathMap()
#if __name__ == "__main__":
projectManager = resolve.GetProjectManager()

projectManager.LoadProject("empty") 
time.sleep(1)
ret = projectManager.CloseProject(input_f.basename)

ret = projectManager.DeleteProject(input_f.basename)
time.sleep(1)
projectManager.CreateProject(input_f.basename)

project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()

rootFolder = mediaPool.GetRootFolder()
folder = mediaPool.AddSubFolder(rootFolder, input_f.basename)
MediaStorage = resolve.GetMediaStorage()

ret = project.SetSetting("timelineResolutionWidth", '1080')
ret = project.SetSetting("timelineResolutionHeight", '1920')

ret= project.SetSetting("timelineFrameRate", str(fps))
ret=project.SetSetting("timelinePlaybackFrameRate", str(fps))
print(project.GetSetting("timelineResolutionWidth"), project.GetSetting("timelineResolutionHeight"), project.GetSetting("timelineFrameRate"))


#time.sleep(0.5)
clips = []
for x in range(10): 
    added = MediaStorage.AddItemListToMediaPool(input_f.avee_final_file)

    clips = folder.GetClipList()
    if len(clips) == 0:
        logging.info(f"error clip list is empty")
        time.sleep(0.5)
    else:
        break
# ordered_clips = [None for c in clips]
# for c in clips:
#     name =c.GetName()
#     split = os.path.splitext(name)[0].split("_")
#     split2 = split[len(split)-1]
#     ordered_clips[int(split2)] = c

# clips[1] = ordered_clips[7]
# clips[7] = ordered_clips[1]
time.sleep(0.5)

mediaPool.CreateTimelineFromClips("timeline_", clips)

#ret = project.SetSetting("timelineFrameRate", "65")


timeline = project.GetCurrentTimeline()
for x in range(10):
    timeline = project.GetCurrentTimeline() 
    if timeline:
        break
    print("waiting for timeline")
    time.sleep(0.5)
if not timeline:
    if project.GetTimelineCount() > 0:
        timeline = project.GetTimelineByIndex(1)
        project.SetCurrentTimeline(timeline)



clips = timeline.GetItemListInTrack("video", 1)
#comp =  clips[0].GetFusionCompByIndex(0)
clip = clips[0]	
print(clip.GetName())
clip_properties = clip.GetProperty()
ret = clip.SetProperty("ZoomX", 2.350) #3
#ret = clip.GetProperty("ZoomX")

time.sleep(1) #without this AddTool() fails
comp = None
while not comp:
    print("getting comp..")
    comp = clip.GetFusionCompByName("Composition 1")
    time.sleep(1)
    ll = clip.GetFusionCompNameList()
    if len(ll) == 0:
        clip.AddFusionComp()

pp = comp.GetCompPathMap()
if comp == None:
    logging.info("Error failed to get composition")
#ll = clips[0].GetFusionCompNameList()	
tools = []
for x  in range(10):
    tools = comp.GetToolList()
    if len(tools) >= 2:
        break
    else:
        logging.info(f"error tools list is empty")
        time.sleep(0.5)
media_in_tool = None
for key, tool in tools.items():
    if "MediaIn" in tool.Name: 
        media_in_tool = tool
comp.SetActiveTool(media_in_tool)
tr_tool = comp.AddTool("Merge", -32768, -32768)

def add_transform_tool():
    tr_tool = comp.AddTool("Transform", -32768, -32768)
    ret = tr_tool.Edges[0]
    tr_tool.Edges = 3
    
    # tr_tool.SetInput("Center", {1: 0.8, 2: 0.2, 3: 0.0}, 0)
    # tr_tool.SetInput("Center", {1: 0.5, 2: 0.4, 3: 0.0}, 5)
    tr_tool.AddModifier("Size", "BezierSpline")
    tr_tool.AddModifier("Angle", "BezierSpline")
    tr_tool.AddModifier("Aspect", "BezierSpline")

    tr_tool.Center = comp.Path()
    tr_tool.MotionBlur = 0#1
    #t = tr_tool.GetInput("ShutterAngle")
    tr_tool.Quality = 8
    tr_tool.ShutterAngle = 270
    return tr_tool

tr_tool = add_transform_tool()
tr_tool2 = add_transform_tool()
dblur = comp.AddTool("DirectionalBlur", -32768, -32768)
ret = dblur.AddModifier("Length", "BezierSpline")
ret = dblur.AddModifier("Glow", "BezierSpline")
main_shake = comp.AddTool("ofx.com.blackmagicdesign.resolvefx.CameraShake", -32768, -32768) #for rest
main_shake.MotionScale = 0.378
main_shake.SpeedScale = 0.126

textp = comp.AddTool("TextPlus", -32768, -32768)
time.sleep(0.5)
textp.StyledText = "Follow cristian_k_music\non IG"
textp.Center =  {1: 0.5, 2: 0.145, 3: 0.0}
ff = textp.GetInput("Font")
textp.Enabled2 = 1
textp.ElementShape2 = 2 #{1: 'Text Fill', 2: 'Text Outline', 3: 'Border Fill', 4: 'Border Outline'}
textp.Level2 = 1# {1: 'Text', 2: 'Line', 3: 'Word', 4: 'Character'}
textp.Round2 = 0.23
textp.Red2 = 0.0
textp.Blue2 = 0.0
textp.Green2 = 1.0
textp.Size = 0.055 #0.08

comp.SetActiveTool(textp)
textp_shake = comp.AddTool("CameraShake", -32768, -32768) #for text
textp_shake.OverallStrength = 0.1
textp_shake.Speed = 0
textp_rays = comp.AddTool("Fuse.OCLRays", -32768, -32768) 
textp_rays.Blend = 0.4
textp_shadow = comp.AddTool("ofx.com.blackmagicdesign.resolvefx.DropShadow", -32768, -32768) 
inputs = textp.GetInputList().values()

ease_funs = spline.ease_funs()

xx, yy = ease_funs.get_range_spline(ease_funs.easeOutBounce_yline.line, 0, 50, 0.8, 0.5)

for i, elem in enumerate(yy):
    tr_tool.Center[xx[i]] = {1: yy[i], 2: 0.5, 3: 0.0}
    #tr_tool.Size[xx[i]] = yy[i]*3
    #tr_tool.SetInput("Center", {1: 0.7 + x/100, 2: 0.2, 3: 0.0}, x)
    #tr_tool.Angle[x] = x/20 
    #tr_tool.Center =  {1: 0.7, 2: 0.2, 3: x}

transition_delta

def apply_curve(line, x_start, x_end, y_start, y_end, operator):
    if type(y_start) != tuple: 
        xx, yy = ease_funs.get_range_spline(line, x_start, x_end, y_start, y_end)
        for i, elem in enumerate(yy):
            operator[xx[i]] = yy[i]
    else:
        xx0, yy0 = ease_funs.get_range_spline(line, x_start, x_end, y_start[0], y_end[0])
        xx1, yy1 = ease_funs.get_range_spline(line, x_start, x_end, y_start[1], y_end[1])
        for i, elem in enumerate(yy0):
            operator[xx0[i]] = {1: yy0[i], 2: yy1[i], 3: 0.0}
        

def apply_transition(transition_frame, operator, delta_secs, y_start, y_end, line):    
    #delta_frames = delta_secs*fps
    apply_curve(line.line, transition_frame-delta_secs*fps, transition_frame, 
                y_start, y_end, operator)
    apply_curve(line.opposite, transition_frame, transition_frame+delta_secs*fps, 
                y_end, y_start, operator)


for inp in inputs:
    
    name = inp.GetAttrs()["INPS_Name"]
    print("### " + name)
    if name == "Layout Center" or name == "Round 2":
        attrs =inp.GetAttrs ()
        for key, val in attrs.items():
            print("###### ", key.ljust(30), " ", val)

apply_transition(180, tr_tool.Size, 0.666, 1, 2.5, ease_funs.easeInExpo_yline)
apply_transition(180, tr_tool.Center, 0.666, (0.5, 0.5) , (0.0, 0.5), ease_funs.easeInExpo_yline)
apply_transition(180, tr_tool.Angle, 0.666,  0, 30, ease_funs.easeInBack_yline)
apply_transition(180, dblur.Length, 0.3333, 0, 0.06, ease_funs.easeInSine_yline)
apply_transition(180, dblur.Glow, 0.3333, 0, 0.3, ease_funs.easeInSine_yline)

# apply_curve(ease_funs.easeInExpo_yline, 140, 180, 1, 2.5, tr_tool.Size)
# apply_curve(ease_funs.easeOutExpo_yline, 180, 220, 2.5, 1, tr_tool.Size)



    #time.sleep(1)
clips = folder.GetClipList()

for clip in clips:
    print(type(clip))
    p = clip.GetClipProperty()
    print(p)
    if clip.GetClipProperty()["Video Codec"] != "" or 1:
        subClip = {
            "mediaPoolItem": clip,
            "startFrame": 50,
            "endFrame": 73,
        }

        if mediaPool.AppendToTimeline([ subClip ]):
            print("added subclip (first 24 frames) of \"" + clip.GetName() + "\" to current timeline.")




#x = tr_tool.GetInputList().values()

# print(len(tot_data))
# with open("f.png", "wb") as f_o:
#     f_o.write(arr[0:pos])

# def send_page_down(handle, param):
#     if win32gui.GetClassName(handle) == param or 1:
#         win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
#         win32gui.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_UP, 0)

# G = gw.getWindowsWithTitle("Avee Player")
# G[0].moveTo(0, 0)
# window_id = win32gui.FindWindow(None, "Avee Player")
# win32gui.EnumChildWindows(window_id, send_page_down, 'FoxitDocWnd')


# tr_tool.SetAttrs({"TOOLS_Name" : "mytransform"})
# tr_tool.Center.SetAttrs({"INPS_Name" : "mycenter"})
# tr_tool.Center.SetAttrs({"INPN_OffsetControl_ValueX" : "0.6"})

# #tr_tool.SetInput("Center", 25, 5)
# tr_tool.Angle = 0.5
# while 1:
#     inputs = tr_tool.GetInputList("Point").values()

#     for inp in inputs:
        
#         name = inp.GetAttrs()["INPS_Name"]
#         if name != "Center": continue
#         attrs =inp.GetAttrs()
#         for key, val in attrs.items():
#             print(key.ljust(30), " ", val)

#         d = { "INPN_OffsetControl_ValueX": 0.7  }
#         ret = inp.SetAttrs(d  )

#         print(name)
#         inputID = inp.GetAttrs()["INPS_ID"]
#         inputName = inp.GetAttrs()["INPS_Name"]
#         inputDataType = inp.GetAttrs()["INPS_DataType"]
#         print('\t[Registry ID] {0}\t[Data Type] {1}'.format(inputName, inputDataType))
#         time.sleep(1)
# if tr_tool.AddModifier("Center", "BezierSpline"):
#     tr_tool.Center[0] = 1.0
#     tr_tool.Center[100] = 0.0
# #timeline.InsertFusionCompositionIntoTimeline()
# #timeline.InsertFusionGeneratorIntoTimeline()
# get the clip object
clip = resolve.ProjectManager.GetCurrentProject().GetCurrentTimeline().GetItemByIndex(0)

# set the position of the clip
clip.setPosition(100, 150)