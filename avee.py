import webcolors
import win32gui,pywintypes
import win32con,win32file,win32pipe,win32api, numpy, threading
import pygetwindow as gw
import time, subprocess as sp, mss
from PIL import Image
import logging, math
# time.sleep(1)

import win32gui
import win32ui
import random, traceback
import autopy as at
from autopy import background_screenshot, receive_screen_shot_from_phone
import urllib.parse

import time, shlex, random, numpy as np
import pywinauto, ctypes, os,win32process
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns, webcolors

#!/usr/bin/env python

from avee_utils import *

#a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"

#background_screenshot(hwnd, wid, hei+52,True)
#ret = receive_screen_shot_from_phone(save_file=True)

#check_device_awake()



template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"
fonts = ['Open Sans', 'Arial Rounded MT Bold', 'Bauhaus 93', 'Berlin Sans FB', 'Cambria Math', 'Comic Sans MS', 'Eras Bold ITC', 'Eras Demi ITC', 'Gill Sans Ultra Bold Condensed', 'Harrington', 'High Tower Text', 'Imprint MT Shadow', 'Jokerman', 'Kristen ITC',"Maiandra GD","Matura MT Script Capitals","MS PGothic","MV Boli","Trebuchet MS","Tw Cen MT","Tw Cen MT Condensed Extra Bold","Ubuntu","Open Sans"]

nt = namedtuple("name_storage", "android_name win_name basename dirpath")

template_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(template_fld)]
audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

andr_input_fld = "/mnt/shared/Pictures/"


f = "00032.mp3"
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
s_sec = 26
s_ms = 824
bars=8
bars_per_template=1
beats_per_bar = 4
input_f = name_storage(input_file, out)
fps = 60#59940/1000

time_per_beat = (60/bpm)
frames_per_beat = fps*time_per_beat
frames_per_bar = frames_per_beat*beats_per_bar
transition_delta = frames_per_bar*bars_per_template
tot_transitions = bars//bars_per_template
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

ret = resolve.OpenPage("Edit")
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

raw_clips = folder.GetClipList()
raw_clip = raw_clips[0]
p = raw_clip.GetClipProperty()
clip_end = float(p["End"])
clip_fps = p["FPS"]

clips = timeline.GetItemListInTrack("video", 1)
#comp =  clips[0].GetFusionCompByIndex(0)
clip = clips[0]	
logging.info(f"clip name: {clip.GetName()}")
clip_properties = clip.GetProperty()
ret = clip.SetProperty("ZoomX", 1.45) #2.35 if source is 1080p, 1.4-1.5 if 1920x1920
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
#tr_tool = comp.AddTool("Merge", -32768, -32768)

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

def get_color_name(hex_code="", rgb=None, norm=False):
    xx = None; hex = None
    try:
        if len(hex_code):
            rgb = webcolors.hex_to_rgb(hex_code)
        xx = tuple(int(val*255) for val in rgb) if norm else rgb
        hex = '#{:02x}{:02x}{:02x}'.format(xx[0], xx[1], xx[2])
        color_name = webcolors.rgb_to_name(xx )
        return xx, color_name, hex
    except Exception as e:
        print(e)
        return xx, "", hex
    
def lum(v):
    v /= 255
    if v <= 0.03928:
        return  v / 12.92 
    else:
        return math.pow((v + 0.055) / 1.055, 2.4);
def luminance(r, g, b):
  a = [r, g, b] = lum(r), lum(g), lum(b)
  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;

def contrast(rgb1, rgb2):
  lum1 = luminance(rgb1[0], rgb1[1], rgb1[2]);
  lum2 = luminance(rgb2[0], rgb2[1], rgb2[2]);
  brightest = max(lum1, lum2);
  darkest = min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05)    
  
def get_random_text_style(operator, min_contrast, font_list):
    font__ = random.choice(font_list)
    pastel_palette = sns.color_palette("pastel", 100)
    dark_palette = sns.color_palette("dark", 100)
    while 1: 
        p_cc = random.choice(pastel_palette)
        d_cc = random.choice(dark_palette)
        c = contrast([e*255 for e in p_cc]  , [e*255 for e in d_cc])
        if c > min_contrast:
            break
    rgb_tuple1, color_name, hex1 = get_color_name(rgb=p_cc, norm=True)
    operator.Red1, operator.Green1, operator.Blue1 =  p_cc
    rgb_tuple2, color_name, hex2 = get_color_name(rgb=d_cc, norm=True)
    operator.Red2, operator.Green2, operator.Blue2 =  d_cc
    operator.Thickness2 = 0.2
    operator.ElementShape2 = random.randint(1,2)
    operator.Level2 = 1# {1: 'Text', 2: 'Line', 3: 'Word', 4: 'Character'}
    operator.Round2 = 0.23
    time.sleep(1)

    operator.Font =  font__ 
    operator.Style = "Regular"

    logging.info(f" font {font__}, {operator.GetInput('Font')}, c1 {hex1} c2 {hex2} , Shape: {operator.GetInput('ElementShape2')}")

    #textp.ElementShape2 = 2 #{1: 'Text Fill', 2: 'Text Outline', 3: 'Border Fill', 4: 'Border Outline'}

def clamp(num, min, max):
    return min if num < min else max if num > max else num
    
tr_tool = add_transform_tool()
#tr_tool2 = add_transform_tool()
dblur = comp.AddTool("DirectionalBlur", -32768, -32768)
ret = dblur.AddModifier("Length", "BezierSpline")
ret = dblur.AddModifier("Glow", "BezierSpline")
ret = dblur.AddModifier("Angle", "BezierSpline")

main_shake = comp.AddTool("ofx.com.blackmagicdesign.resolvefx.CameraShake", -32768, -32768) #for rest
main_shake.MotionScale = 0.378
main_shake.SpeedScale = 0.126

textp = comp.AddTool("TextPlus", -32768, -32768)
ret = textp.AddModifier("Size", "BezierSpline")
ret = textp.AddModifier("AngleX", "BezierSpline")
ret = textp.AddModifier("AngleY", "BezierSpline")
ret = textp.AddModifier("AngleZ", "BezierSpline")
textp.Center = comp.Path()
time.sleep(0.5)
#ff = textp.GetInput("Font")
textp.Enabled2 = 1

get_random_text_style(textp, 6, fonts)
textp.StyledText = "Follow cristian_k_music\n" + "on IG"
textp.Center =  {1: 0.5, 2: 0.145 if random.randint(0,1) else 1-0.145, 3: 0.0}

time.sleep(0.2)
textp.Size = 0.08 #at 1080p 0.055

comp.SetActiveTool(textp)

textp_shake = comp.AddTool("CameraShake", -32768, -32768) #for text
textp_shake.XDeviation = 0.83
textp_shake.YDeviation = 0.83
textp_shake.RotationDeviation = 0.61
textp_shake.Randomness = 0.5
textp_shake.OverallStrength = 0.007
textp_shake.Speed = 0
textp_rays = comp.AddTool("Fuse.OCLRays", -32768, -32768) 
textp_rays.Blend = 0.055# 0.4
textp_shadow = comp.AddTool("ofx.com.blackmagicdesign.resolvefx.DropShadow", -32768, -32768) 

inputs = textp.GetInputList().values()

ease_funs = spline.ease_funs()
add_intro_outro = 1
# xx, yy = ease_funs.get_range_spline(ease_funs.easeOutBounce_yline.line, 0, 50, 0.8, 0.5)

# for i, elem in enumerate(yy):
#     tr_tool.Center[xx[i]] = {1: yy[i], 2: 0.5, 3: 0.0}
    #tr_tool.Size[xx[i]] = yy[i]*3
    #tr_tool.SetInput("Center", {1: 0.7 + x/100, 2: 0.2, 3: 0.0}, x)
    #tr_tool.Angle[x] = x/20 
    #tr_tool.Center =  {1: 0.7, 2: 0.2, 3: x}

transition_delta
d=3
def apply_curve(line, x_start, x_end, y_start, y_end, operator):
    if type(y_start) != tuple: 
        xx, yy = ease_funs.get_range_spline(line, x_start, x_end, y_start, y_end)
        for i, elem in enumerate(yy):
            if xx[i] >= 0:
                operator[xx[i]] = yy[i]
            elif add_intro_outro:
                new_x = xx[i]+ clip_end
                if math.ceil(new_x) < clip_end-d:
                    #print(new_x)
                    operator[new_x] = yy[i]

    else:
        xx0, yy0 = ease_funs.get_range_spline(line, x_start, x_end, y_start[0], y_end[0])
        xx1, yy1 = ease_funs.get_range_spline(line, x_start, x_end, y_start[1], y_end[1])
        for i, elem in enumerate(yy0):
            if xx0[i] >= 0:
                operator[xx0[i]] = {1: yy0[i], 2: yy1[i], 3: 0.0}
            elif add_intro_outro:
                new_x = xx0[i]+ clip_end
                if math.ceil(new_x) < clip_end-d:
                    #print(new_x)
                    operator[new_x] =  {1: yy0[i], 2: yy1[i], 3: 0.0}
        

def apply_transition(transition_frame, operator, delta_secs, y_start, y_end, line):    
    #delta_frames = delta_secs*fps
    apply_curve(line.line, transition_frame-delta_secs*fps, transition_frame, 
                y_start, y_end, operator)
    apply_curve(line.opposite, transition_frame, transition_frame+delta_secs*fps, 
                y_end, y_start, operator)
    
def random_curve():
    return getattr(ease_funs, random.choice(ease_funs.function_l[0:10]) + "_yline")

def text_curve():
    ll = ['easeInCirc', 'easeInElastic', 'easeInExpo', 'easeInBack', 'easeInBounce']
    return getattr(ease_funs, random.choice(ll) + "_yline")

def apply_random_transition(i, transition_frame, dir, cur_list):
    expected_clip_end = transition_delta*tot_transitions
    factor =  clip_end/expected_clip_end
    transition_frame = transition_frame*factor
    logging.info(f"Applying transition {i}, at frame {transition_frame}, direction: {dir}")
    r = random.uniform; r2 = random.randint
    t_d = r(0.5, 0.8)
    t_b = r(0.25, 0.45)
    t_size = (r(0.9, 1.1), r(2.0, 2.6))
    #dir = random.choice([(0,0),(1,0),(1,1),(0,1)])
    t_center = ((r(0.4, 0.6), r(0.4, 0.6)), (r(dir[0]-0.1, dir[0]+0.1), r(dir[1]-0.1, dir[1]+0.1)))
    t_angle = (r(-5, 5), r(30, 40)*(-1 if i%2 == 0 else 1 ))

    apply_transition(transition_frame, tr_tool.Size,   t_d, t_size[0], t_size[1], cur_list[0][i])
    apply_transition(transition_frame, tr_tool.Center, t_d, t_center[0] , t_center[1], cur_list[1][i])
    apply_transition(transition_frame, tr_tool.Angle,  t_d,  t_angle[0], t_angle[1], cur_list[2][i])
    apply_transition(transition_frame, dblur.Length,   t_b, 0, 0.06, cur_list[3][i])
    apply_transition(transition_frame, dblur.Glow,     t_b, 0, 0.3, cur_list[4][i])
    apply_curve(np.linspace(dir[2],dir[2],100), transition_frame-t_b*fps, transition_frame+t_b*fps, dir[2], dir[2], dblur.Angle)

def point_displacement(point, vec, disp):
    nn = np.linalg.norm(vec)
    unit_vec = vec / nn
    return point + disp * unit_vec

# for inp in inputs:
    
#     name = inp.GetAttrs()["INPS_Name"]
#     print("### " + name)
#     if name == "Layout Center" or name == "Round 2":
#         attrs =inp.GetAttrs ()
#         for key, val in attrs.items():
#             print("###### ", key.ljust(30), " ", val)

dir_list = []
dirs_l = [(0.0, 0.0, 225), (1.0, 0.0, 315), (1.0, 1.0, 45), (0.0, 1.0, 135), 
          (0.5, 0.0, 270), (1.0, 0.5, 0), (0.5, 1.0, 90), (0.0, 0.5, 180) ]
for x in range(math.ceil(tot_transitions/len(dirs_l))): #4 directions
    random.shuffle(dirs_l)
    dir_list+= dirs_l[:]

curve_list = []
for y in range(5): #need 5 curves per transition
    shuffled_l = []
    for x in range(math.ceil(tot_transitions/10)): # 10 ease in curves.
        tmp = ease_funs.function_l[0:10]
        random.shuffle(tmp)
        shuffled_l += tmp

    curve_list.append([getattr(ease_funs, elem + "_yline") for elem in shuffled_l] )



text_dirs_l = [(1,0), (-1, 0), (0, 1), (0, -1), (1,1), (-1,-1), (-1,1), (1,-1) ]

textp.Center =  {1: 0.5, 2: 0.145 if random.randint(1,1) else 0.855, 3: 0.0}
textp.Size =  0.08
t_size = textp.Size[0]
t_center = textp.Center[0]
t_center = (t_center[1], t_center[2])
dir =  random.choice(text_dirs_l)
ext_point = point_displacement(t_center, dir, 0.74)

text_frame =  clip_end//2
textp.Center[text_frame-101]  =  {1: -10, 2: -10, 3: 0.0}
textp.Center[0]  = {1: -10, 2: -10, 3: 0.0}
# for ii in range(0, int(text_frame)):
#     textp.Center[ii] = {1: -10, 2: -10, 3: 0.0}
    #textp.Size[ii ] = t_size
logging.info(f"Applying text transitions..")
cc1 = text_curve()
apply_curve(cc1.opposite, text_frame-100, text_frame, (ext_point[0], ext_point[1]), t_center, textp.Center)
cc2 = text_curve()
apply_curve(cc2.opposite, text_frame-100, text_frame, random.uniform(0.25, 0.25), t_size, textp.Size)

angle_dict = [ textp.AngleX, textp.AngleY, textp.AngleZ]
angle_l = [iii for iii in range(random.randint(1,3))]
angle_l = [0,1,2]

cc3 = text_curve()
random.shuffle(angle_l)
r = random.uniform
for i, angle in enumerate(angle_l):
    t_angle =   r(30, 60) * (-1 if random.randint(0,1) else 1 )
    angle_dict[angle][text_frame-101] = 0
   # apply_transition(text_frame, angle_dict[angle], 1,  0, t_angle, cc3)
    apply_curve(cc3.line,     text_frame-100, text_frame, t_angle, -t_angle, angle_dict[angle])
    apply_curve(cc3.opposite, text_frame, text_frame+100, -t_angle, 0, angle_dict[angle])

    #apply_curve(cc3.line, text_frame, text_frame+60, t_angle, 0, angle_dict[angle])
    
textp.Center[clip_end-200] =  {1: t_center[0], 2: t_center[1], 3: 0.0}

textp.Center[clip_end-100] =  {1: -0, 2: -2, 3: 0.0}

for i in range(0, tot_transitions):
    apply_random_transition(i, i*transition_delta, dir_list[i], curve_list)


# if not project.SetCurrentRenderFormatAndCodec(renderFormat, renderCodec):
#     return False
p = r"F:\davinci2\\"
project.SetRenderSettings({"SelectAllFrames" : 1, "TargetDir" : p, "CustomName": f"{input_f.basename}_dav.mp4"})
ret= project.AddRenderJob()
logging.info(f"Starting render..")

project.StartRendering()
while project.IsRenderingInProgress():
    logging.info("Waiting for render to finish..")
    time.sleep(1)
#fusion.Quit() #quites davinci
# apply_transition(180, tr_tool.Size, 0.666, 1, 2.5, ease_funs.easeInExpo_yline)
# apply_transition(180, tr_tool.Center, 0.666, (0.5, 0.5) , (0.0, 0.5), ease_funs.easeInExpo_yline)
# apply_transition(180, tr_tool.Angle, 0.666,  0, 30, ease_funs.easeInBack_yline)
# apply_transition(180, dblur.Length, 0.3333, 0, 0.06, ease_funs.easeInSine_yline)
# apply_transition(180, dblur.Glow, 0.3333, 0, 0.3, ease_funs.easeInSine_yline)

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