
import time, subprocess as sp
import logging, math, datetime, os
# time.sleep(1)
import random
import time, shlex, random, numpy as np
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns
import spline, webcolors
import matplotlib.pyplot as plt
from avee_utils import get_duration
#from base import context
import textwrap, ass

import DaVinciResolveScript as dvr_script

import cv2
from itertools import combinations

def euclidean_distance(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

def get_video_palette(video_path, start_frame=20, end_frame=40, num_colors=10):
    cap = cv2.VideoCapture(video_path)
    frame_colors = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:    break
        # Check if the current frame is within the specified range
        if frame_count >= start_frame and frame_count <= end_frame:
            # Convert the frame from BGR to RGB
            data = cv2.resize(frame, (100, 100)).reshape(-1, 3)

            #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Flatten the frame to a list of pixels
           # pixels = data.reshape((-1, 3))
            frame_colors.extend(data)
        frame_count += 1
        if frame_count > end_frame:
            break
    cap.release()
    # Convert the list to a NumPy array
    frame_colors = np.array(frame_colors)
    # Use k-means clustering to find the dominant colors
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(frame_colors.astype(np.float32), num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Convert centers to uint8
    centers = np.uint8(centers)
    return centers


def get_prominent_color(video_path):
    cap = cv2.VideoCapture(video_path)
    for x in range(10):
        ret, frame = cap.read()
    ret, frame = cap.read()
    #data = cv2.resize(frame, (100, 100)).reshape(-1, 3)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pixels = image_rgb.reshape((-1, 3))
    pixels = np.float32(pixels)
    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 3  # You can adjust the number of clusters (colors) here
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Convert back to uint8 and reshape to the original image shape
    centers = np.uint8(centers)
    prominent_color = centers[np.argmax(np.bincount(labels.flatten()))]
    return prominent_color

def get_contrasting_color(color):
    r, g, b = color
    # Calculate perceived brightness using luminance formula
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    # Threshold to determine whether the color is dark or light
    threshold = 0.5
    if brightness < threshold:  # Dark color
        # Lighten the color
        r = min(255, r + 100)
        g = min(255, g + 100)
        b = min(255, b + 100)
    else:  # Light color
        # Darken the color
        r = max(0, r - 100)
        g = max(0, g - 100)
        b = max(0, b - 100)
    
    return (r, g, b)

def get_contrasting_colors(palette):
    max_distance = 0
    contrasting_pair = None

    # Find all combinations of colors in the palette
    for color1, color2 in combinations(palette, 2):
        distance = euclidean_distance(color1, color2)
        if distance > max_distance:
            max_distance = distance
            contrasting_pair = (color1, color2)

    return contrasting_pair

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

def clamp(num, min, max):
    return min if num < min else max if num > max else num
def point_displacement(point, vec, disp):
    nn = np.linalg.norm(vec)
    unit_vec = vec / nn
    return point + disp * unit_vec

from fontTools.ttLib import TTFont

def get_available_fonts():
    available_fonts = []
    # Replace the directory path with the appropriate path for your system
    font_directory = "/usr/share/fonts"  # Example directory on Linux, could be different on other systems

    # Iterate over font files in the directory
    for font_file in os.listdir(font_directory):
        if font_file.endswith(".ttf"):  # Adjust if your fonts are in a different format
            font_path = os.path.join(font_directory, font_file)
            try:
                font = TTFont(font_path)
                font_name = font['name'].getName(1, 3, 1).string.decode('utf-16')
                available_fonts.append(font_name)
            except Exception as e:
                print(f"Error parsing {font_path}: {e}")

    return available_fonts


import winreg

def get_available_fonts_win():
    fonts_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
    num_fonts = winreg.QueryInfoKey(fonts_key)[1]
    available_fonts = []
    for i in range(num_fonts):
        font_name, font_path = winreg.EnumValue(fonts_key, i)[:2]
        available_fonts.append((font_name, font_path))
    winreg.CloseKey(fonts_key)
    return available_fonts

# available_fonts = get_available_fonts_win()
# print("Available fonts:")
# for font_name, font_path in available_fonts:
#     print(f"{font_name}: {font_path}")


class dav_handler():
    def __init__(s, ctx, codec="H264", overwrite=0) -> None:

        if os.path.isfile(ctx.input_f.dav_final_file) and not overwrite:
            logging.info("Dav file already exists, returning")
            return 
        s.input_video = ctx.input_f.avee_final_file if not len(ctx.custom_video) else ctx.input_f.custom_video_final_file
        
        assert(os.path.isfile(s.input_video))

        #s.input_video_palette = get_video_palette(s.input_video, start_frame=20, end_frame=25)
        s.prominent_color = get_prominent_color(s.input_video)
        s.contrasting_color = get_contrasting_color(s.prominent_color)
        logging.info(f"get_contrasting_color {s.prominent_color}, contrasting color {s.contrasting_color}")
        assert(codec == "H264" or codec== "H264_NVIDIA")

        t2 = time.time()

        s.ctx = ctx
        s.text = ctx.text

        s.init()

        black_list = s.get_font_black_list()

        s.font_list = s.fusion.FontManager.GetFontList()
        s.fonts = list(s.font_list.keys())
        s.fonts = [f for f in s.fonts if not f in black_list]
        # aa3 = s.project.GetCurrentRenderFormatAndCodec()

        s.ease_funs = spline.ease_funs()
        s.add_intro_outro = 0

        ret = s.resolve.OpenPage("Edit")

        s.AddMediaItem()

        s.get_clip_info()

        expected_clip_end = s.ctx.transition_delta*s.ctx.tot_transitions
        s.factor = s.clip_end / expected_clip_end
        logging.debug(f"s.factor {s.factor}")

        s.plot = 0
        if s.plot:
            s.init_plt()

        s.set_clip_properties()
        time.sleep(1) #without this AddTool() fails

        s.get_comp()

        s.tr_tool = s.add_transform_tool()
        
        s.add_tools_and_modifiers()

        #s.lyrics_text = [("it's true i forgot about us all", 0), ("it's true i did see you fall", 100)]

        if s.adding_lyrics():
            s.add_lyrics(ctx.input_f.guessed_lyrics_file)

        if len(s.ctx.secondary_text):
            s.add_secondary_text(s.ctx.secondary_text)

        if s.text:
            s.get_random_text_style(s.textp, 6, s.fonts)

            s.textp.StyledText =  s.text #"Follow cristian_k_music\n" + "on IG"
            time.sleep(0.2)
            s.add_text_effects(s.textp)

            s.apply_text_transitions()

        s.apply_video_transitions()
        projectManager = s.resolve.GetProjectManager()
        projectManager.SaveProject()
        s.render(codec)
        logging.info(f"Times: davinci = {str(datetime.timedelta(seconds=time.time()-t2))} ")

    def get_font_black_list(s):
        black_list = [ "Unispace", "AmpleSoundTab", "Blackadder ITC", "Bookshelf Symbol 7", "Edwardian Script ITC", "Freestyle Script", "Fusion Shapes", "Gill Sans MT Ext Condensed Bold", "HoloLens MDL2 Assets", "Javanese Text", "Juice ITC", "Kunstler Script", "Marlett", "MingLiU-ExtB", "MS Outlook", "MS Reference Specialty", "MT Extra", "Onyx", "Palace Script MT", "Parchment", "Playbill", "Sans Serif Collection", "Segoe Fluent Icons", "Segoe MDL2 Assets", "SWGamekeys MT", "Symbol", "Vladimir Script", "Webdings", "Wingdings", "Wingdings 2", "Wingdings 3", "Lucida Console", "Consolas", "Courier New", "Droid Sans Mono", "Footlight MT Light", "Niagara Solid", "Niagara Engraved", "Rage Italic", "UI Emoji"]

        black_list_too_big = ['Algerian', 'AmpleSoundTab', 'AniMe Matrix - MB_EN', 'Arial Rounded MT Bold', 'Blackadder ITC', 'Bookman Old Style', 'Broadway', 'Cascadia Code', 'Cascadia Mono', 'Castellar', 'Century', 'Century Schoolbook', 'Comic Sans MS', 'Consolas', 'Cooper Black', 'Copperplate Gothic Bold', 'Copperplate Gothic Light', 'Courier New', 'Edwardian Script ITC', 'Elephant', 'Engravers MT', 'Eras Bold ITC', 'Felix Titling', 'Fira Mono', 'Footlight MT Light', 'Franklin Gothic Heavy', 'Freestyle Script', 'Gill Sans MT Ext Condensed Bold', 'Gill Sans Ultra Bold', 'Goudy Stout', 'HoloLens MDL2 Assets', 'Ink Free', 'Javanese Text', 'Jokerman', 'Juice ITC', 'Kristen ITC', 'Kunstler Script', 'Lucida Bright', 'Lucida Console', 'Lucida Fax', 'Lucida Sans', 'Lucida Sans Typewriter', 'Lucida Sans Unicode', 'Matura MT Script Capitals', 'MS Reference Sans Serif', 'MV Boli', 'Niagara Engraved', 'Niagara Solid', 'OCR A Extended', 'Onyx', 'Palace Script MT', 'Parchment', 'Playbill', 'Rage Italic', 'Ravie', 'Rockwell Extra Bold', 'ROG Fonts', 'Sans Serif Collection', 'Segoe Fluent Icons', 'Segoe MDL2 Assets', 'Segoe Print', 'Segoe Script', 'Showcard Gothic', 'SimSun-ExtB', 'Snap ITC', 'Stencil', 'Verdana', 'Vladimir Script', 'Wide Latin', 'Neue Haas Grotesk Text Pro', 'Rockwell Nova', 'Verdana Pro', "Microsoft PhagsPa", "SimSun", "Yu Gothic", "Modern No. 20", "Symbola", "Brush Script MT", "Sylfaen"]
        return black_list+black_list_too_big

    def adding_lyrics(s):
        if s.ctx.add_lyrics and  os.path.isfile(s.ctx.input_f.guessed_lyrics_file):
            return True
        return False


    def add_secondary_text(s, which):
        import json
        with open(r'data\texts.json', 'r') as file:
            text_map = json.load(file)
            
        s.comp.SetActiveTool(s.main_shake)
        s.lyrics_textp = s.comp.AddTool("TextPlus", -32768, -32768)
        time.sleep(0.5)
        s.lyrics_textp.Enabled2 = 1
        s.lyrics_textp.Center =  {1: 0.5, 2: 1-0.145, 3: 0.0}
        w_is_larger = s.clip_w > s.clip_h
        size = 0.031 if w_is_larger else 0.07 
        s.lyrics_textp.Size[0] =  size
        ret = s.lyrics_textp.AddModifier("StyledText", "BezierSpline")
        s.get_random_text_style(s.lyrics_textp, 6, font_list=s.fonts)

        outp = s.lyrics_textp.FindMainOutput(1)
        inps = outp.GetConnectedInputs()
        merge_tool = inps[1].GetTool()
        ret2 = merge_tool.AddModifier("Blend", "BezierSpline")
        merge_tool.Blend[0] = 0

        max_chars_per_line = 31# it's true i forgot about us all
        wrapper = textwrap.TextWrapper(width=max_chars_per_line)

        doc=None
        # with open(lyrics_file, encoding='utf_8_sig') as f:
            # doc = ass.parse(f)
        secs_per_text = 7
        frames_per_text = secs_per_text*  s.ctx.fps
        texts_n = math.floor(s.clip_end / frames_per_text)
        texts = random.sample(text_map[which], texts_n)
        
        for i, text in enumerate(texts):
            fade_frames = 0.5 * s.clip_fps #seconds
            #raise Exception("To do:   ev.start - s.ctx.td_start , wtf? ")
            # start =   ev.start - s.ctx.td_start 
            # start_secs = start.total_seconds()
            # if start_secs < 0: start_secs = 0

            start_frame = i*frames_per_text# start_secs*s.clip_fps
            if start_frame >= s.clip_end:
                break
            wrapped =  wrapper.wrap(text=text)
            s.lyrics_textp.StyledText[start_frame] =  "\n".join(wrapped)

            #end = ev.end - s.ctx.td_start
            #end_secs = end.total_seconds()
            end_frame = (i+1)*frames_per_text
            if end_frame > s.clip_end: end_frame = s.clip_end - fade_frames
            
            merge_tool.Blend[start_frame] = 0
            merge_tool.Blend[start_frame+fade_frames] = 1
            merge_tool.Blend[end_frame-fade_frames] = 1
            merge_tool.Blend[end_frame] = 0
            
        s.add_text_effects(s.lyrics_textp, 0.001)

                
    def add_lyrics(s, lyrics_file):

        s.comp.SetActiveTool(s.main_shake)
        s.lyrics_textp = s.comp.AddTool("TextPlus", -32768, -32768)
        time.sleep(0.5)
        s.lyrics_textp.Enabled2 = 1
        s.lyrics_textp.Center =  {1: 0.5, 2: 0.145, 3: 0.0}
        s.lyrics_textp.Size[0] =  0.033 
        ret = s.lyrics_textp.AddModifier("StyledText", "BezierSpline")
        s.get_random_text_style(s.lyrics_textp, 6, font_list=s.fonts)

        outp = s.lyrics_textp.FindMainOutput(1)
        inps = outp.GetConnectedInputs()
        merge_tool = inps[1].GetTool()
        ret2 = merge_tool.AddModifier("Blend", "BezierSpline")
        merge_tool.Blend[0] = 0

        max_chars_per_line = 31# it's true i forgot about us all
        wrapper = textwrap.TextWrapper(width=max_chars_per_line)

        doc=None
        with open(lyrics_file, encoding='utf_8_sig') as f:
            doc = ass.parse(f)

        for ev in doc.events:
            fade_frames = 0.5 * s.clip_fps #seconds
            raise Exception("To do:   ev.start - s.ctx.td_start , wtf? ")
            start =   ev.start - s.ctx.td_start 
            start_secs = start.total_seconds()
            if start_secs < 0: start_secs = 0

            start_frame = start_secs*s.clip_fps
            if start_frame >= s.clip_end:
                break
            wrapped =  wrapper.wrap(text=ev.text)
            s.lyrics_textp.StyledText[start_frame] =  "\n".join(wrapped)

            end = ev.end - s.ctx.td_start
            end_secs = end.total_seconds()
            end_frame = end_secs*s.clip_fps
            if end_frame > s.clip_end: end_frame = s.clip_end - fade_frames
            
            merge_tool.Blend[start_frame] = 0
            merge_tool.Blend[start_frame+fade_frames] = 1
            merge_tool.Blend[end_frame-fade_frames] = 1
            merge_tool.Blend[end_frame] = 0


            
        
    def plot_center(s, transition_frame):
        ti = int((s.ctx.transition_delta-20)+transition_frame)
        for ii in range(  ti):
            v = s.tr_tool.Center[ii]
            s.x_plot[ii] = v[1]
            s.y_plot[ii] = v[2]

        for ii in range(  ti, int(s.clip_end)):
            s.x_plot[ii] = s.x_plot[  ti]
            s.y_plot[ii] = s.y_plot[  ti]
        s.line1.set_ydata(s.x_plot)
        s.line2.set_ydata(s.y_plot)

        s.figure.tight_layout()
        #s.ax.set_aspect('auto')#, adjustable='box')
        s.figure.canvas.draw()
        s.figure.canvas.flush_events()

    def init_plt(s):
        x = np.linspace(0, int(s.clip_end), int(s.clip_end))
        y = np.sin(x)
        x2 = np.linspace(0, int(s.clip_end), int(s.clip_end))
        y2 = np.sin(x) #dont do x2.copy()
         # to run GUI event loop
        plt.ion()
        s.figure, s.ax = plt.subplots(figsize=(10, 8))
        s.line1, = s.ax.plot(x, y, label="X")
        s.line2, = s.ax.plot(x2, y2, label="Y")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=3)

        s.plot_time = [ii for ii in range(int(s.clip_end))]
        s.line1.set_xdata(s.plot_time)
        s.line2.set_xdata(s.plot_time)
        s.x_plot =s.plot_time[:]
        s.y_plot = s.plot_time[:]
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")

    def init(s):
        s.resolve = dvr_script.scriptapp("Resolve")
        s.fusion = s.resolve.Fusion()
        f = s.fusion.GetGlobalPathMap()
        #if __name__ == "__main__":
        projectManager = s.resolve.GetProjectManager()

        ret = projectManager.LoadProject("empty") 
        if not ret:
            raise Exception("""Davinci error: empty project not found, create an empty project and call it "empty" """) 
        time.sleep(1)
        ret = projectManager.CloseProject(s.ctx.input_f.basename)
        time.sleep(1)
        ret = projectManager.DeleteProject(s.ctx.input_f.basename)
        time.sleep(1)
        projectManager.CreateProject(s.ctx.input_f.basename)

        s.project = projectManager.GetCurrentProject()
        s.mediaPool = s.project.GetMediaPool()

        rootFolder = s.mediaPool.GetRootFolder()
        s.folder = s.mediaPool.AddSubFolder(rootFolder, s.ctx.input_f.basename)
        s.MediaStorage = s.resolve.GetMediaStorage()

        ret = s.project.SetSetting("timelineResolutionWidth", '1080')
        ret = s.project.SetSetting("timelineResolutionHeight", '1920')

        ret= s.project.SetSetting("timelineFrameRate", str(s.ctx.fps))
        ret= s.project.SetSetting("timelinePlaybackFrameRate", str(s.ctx.fps))
        print(s.project.GetSetting("timelineResolutionWidth"), s.project.GetSetting("timelineResolutionHeight"), s.project.GetSetting("timelineFrameRate"))

#time.sleep(0.5)
    def AddMediaItem(s):
        clips = []
        for x in range(10): 
            added = s.MediaStorage.AddItemListToMediaPool(s.input_video)
            # added2 = s.MediaStorage.AddItemListToMediaPool(s.ctx.black_f)
            # assert(len(added2))
            clips = s.folder.GetClipList()
            if len(clips) == 0:
                logging.info(f"error clip list is empty")
                time.sleep(0.5)
            else:
                break

        time.sleep(0.5)
        s.mediaPool.CreateTimelineFromClips("timeline_", clips)

    def set_clip_properties(s):
        timeline = s.project.GetCurrentTimeline()
        for x in range(10):
            timeline = s.project.GetCurrentTimeline() 
            if timeline:
                break
            print("waiting for timeline")
            time.sleep(0.5)

        clips = timeline.GetItemListInTrack("video", 1)
        #comp =  clips[0].GetFusionCompByIndex(0)
        s.clip = clips[0]	
        logging.info(f"clip name: {s.clip.GetName()}")
        clip_properties = s.clip.GetProperty()
        s.ctx.custom_video_info
        ret = s.clip.SetProperty("ZoomX", 3.15 if s.clip_w > s.clip_h else 1) #2.35 if source is 1080p, 1.4-1.5 if 1920x1920 # 3.15 fills the whole screen for 16/9 ratio

    def get_clip_info(s):
        raw_clips = s.folder.GetClipList()
        raw_clip = raw_clips[0]
        p = raw_clip.GetClipProperty()
        s.clip_end = float(p["End"])
        s.clip_fps = p["FPS"]
        s.clip_info = p
        s.clip_w , s.clip_h = map(int, p["Resolution"].split('x'))




    def get_comp(s):
        s.comp = None
        while not s.comp:
            logging.info("getting comp..")
            s.comp = s.clip.GetFusionCompByName("Composition 1")
            time.sleep(1)
            ll = s.clip.GetFusionCompNameList()
            if len(ll) == 0:
                s.clip.AddFusionComp()

        pp = s.comp.GetCompPathMap()
        if s.comp == None:
            logging.info("Error failed to get composition")
        #ll = s.clips[0].GetFusionCompNameList()	
        tools = []
        for x  in range(10):
            tools = s.comp.GetToolList()
            if len(tools) >= 2:
                break
            else:
                logging.info(f"error tools list is empty")
                time.sleep(0.5)
        media_in_tool = None
        for key, tool in tools.items():
            if "MediaIn" in tool.Name: 
                media_in_tool = tool
        s.comp.SetActiveTool(media_in_tool)
#tr_tool = s.comp.AddTool("Merge", -32768, -32768)

    def add_transform_tool(s):
        tr_tool = s.comp.AddTool("Transform", -32768, -32768)
        ret = tr_tool.Edges[0]
        tr_tool.Edges = 3
        
        # tr_tool.SetInput("Center", {1: 0.8, 2: 0.2, 3: 0.0}, 0)
        # tr_tool.SetInput("Center", {1: 0.5, 2: 0.4, 3: 0.0}, 5)
        tr_tool.AddModifier("Size", "BezierSpline")
        tr_tool.AddModifier("Angle", "BezierSpline")
        tr_tool.AddModifier("Aspect", "BezierSpline")

        tr_tool.Center = s.comp.Path()
        tr_tool.MotionBlur = 1
        #t = tr_tool.GetInput("ShutterAngle")
        tr_tool.Quality = 8
        tr_tool.ShutterAngle = 270
        return tr_tool


  
    def get_random_text_style(s, operator, min_contrast, font_list):
        font__ = random.choice(font_list)

        # s.contrasting_pair = get_contrasting_colors(s.input_video_palette)
        c = contrast(s.prominent_color  ,s.contrasting_color)
        if c > min_contrast:
            logging.info(f"Not enough contrast ({c}), using sns color text color")
            pastel_palette = sns.color_palette("pastel", 100)
            dark_palette = sns.color_palette("dark", 100)
            while 1: 
                p_cc = random.choice(pastel_palette)
                d_cc = random.choice(dark_palette)
                c = contrast([e*255 for e in p_cc]  , [e*255 for e in d_cc])
                if c > min_contrast:
                    break
        else:
            p_cc = [e/255 for e in s.prominent_color] 
            d_cc = [e/255 for e in s.contrasting_color] 
        # else:
        #     min = [random.choice(s.input_video_palette), random.choice(s.input_video_palette), 100]
        #     while 1: 
        #         p_cc = random.choice(s.input_video_palette)
        #         d_cc = random.choice(s.input_video_palette)
        #         c = contrast(p_cc  ,d_cc)
        #         if c < min[2]:
        #             min =  [p_cc, d_cc, c]
        #             if c < 2:
        #                 p_cc = [e/255 for e in p_cc]
        #                 d_cc = [e/255 for e in d_cc]
        #                 break
                
            #p_cc, d_cc = s.contrasting_pair

        rgb_tuple1, color_name, hex1 = get_color_name(rgb=p_cc, norm=True)
        operator.Red1, operator.Green1, operator.Blue1 =  p_cc
        rgb_tuple2, color_name, hex2 = get_color_name(rgb=d_cc, norm=True)
        operator.Red2, operator.Green2, operator.Blue2 =  d_cc
        operator.Thickness2 = 0.2
        operator.ElementShape2 = random.randint(1,1)
        operator.Level2 = 1# {1: 'Text', 2: 'Line', 3: 'Word', 4: 'Character'}
        operator.Round2 = 0.23
        time.sleep(1)
        
        f = s.font_list[font__]
        if not "Regular" in f.keys():
            style = list(f)[0]
        else: style = "Regular"
        operator.Style = style
        operator.Font =  font__
        logging.info(f"name {operator.Name},  font {font__}, {operator.GetInput('Font')}, c1 {hex1} c2 {hex2} , Shape: {operator.GetInput('ElementShape2')}")

        #textp.ElementShape2 = 2 #{1: 'Text Fill', 2: 'Text Outline', 3: 'Border Fill', 4: 'Border Outline'}

    def add_tools_and_modifiers(s):
        if len(s.ctx.custom_video):
            s.glow = s.comp.AddTool("Glow", -32768, -32768)
            s.glow.AddModifier("Glow", "BezierSpline")


        s.dblur = s.comp.AddTool("DirectionalBlur", -32768, -32768)
        ret = s.dblur.AddModifier("Length", "BezierSpline")
        ret = s.dblur.AddModifier("Glow", "BezierSpline")
        ret = s.dblur.AddModifier("Angle", "BezierSpline")

        s.main_shake = s.comp.AddTool("ofx.com.blackmagicdesign.resolvefx.CameraShake", -32768, -32768) #for rest
        s.main_shake.MotionScale = 0.378
        s.main_shake.SpeedScale = 0.126
        if s.text:
            s.textp = s.comp.AddTool("TextPlus", -32768, -32768)
            ret = s.textp.AddModifier("Size", "BezierSpline")
            ret = s.textp.AddModifier("AngleX", "BezierSpline")
            ret = s.textp.AddModifier("AngleY", "BezierSpline")
            ret = s.textp.AddModifier("AngleZ", "BezierSpline")
            s.textp.Center = s.comp.Path()
            time.sleep(0.5)
            #ff = s.textp.GetInput("Font")
            s.textp.Enabled2 = 1
        else:
            print()

    def add_text_effects(s, comp, shake_streght=0.007):
        s.comp.SetActiveTool(comp)
        time.sleep(0.9)
        name = f"text_shake{random.Random(100)}"
        setattr(s, name, s.comp.AddTool("CameraShake", -32768, -32768))
        textp_shake = getattr(s, name)
        #s.textp_shake = s.comp.AddTool("CameraShake", -32768, -32768) #for text
        textp_shake.XDeviation = 0.83
        textp_shake.YDeviation = 0.83
        textp_shake.RotationDeviation = 0.61
        textp_shake.Randomness = 0.5
        textp_shake.OverallStrength = shake_streght
        textp_shake.Speed = 0
        
        name = f"text_rays1{random.Random(100)}"
        setattr(s, name, s.comp.AddTool("Fuse.OCLRays", -32768, -32768) )
        textp_rays = getattr(s, name)        
        # textp_rays = s.comp.AddTool("Fuse.OCLRays", -32768, -32768) 
        textp_rays.Blend = 0.2# 0.4 055
        
        name = f"text_DropShadow{random.Random(100)}"
        setattr(s, name, s.comp.AddTool("ofx.com.blackmagicdesign.resolvefx.DropShadow", -32768, -32768) )
        textp_shadow = getattr(s, name)
        

    def apply_curve(s, line, x_start, x_end, y_start, y_end, operator, line_name):
        logging.debug(f"Applying curve line: {line_name} xstart: {x_start} xend: {x_end} ystart: {y_start} yend: {y_end} operator: {operator.Name} ")
        d=20 # 10 will cause problems in the beginning ? 
        if type(y_start) != tuple: 
            xx, yy = s.ease_funs.get_range_spline(line, x_start, x_end, y_start, y_end)
            if xx.min() >= 0:
                for i, elem in enumerate(yy):
                    if xx[i] >= 0:
                        operator[round(xx[i])] = yy[i]
            elif s.add_intro_outro:
                for i, elem in enumerate(yy):
                    new_x = round(xx[i]+ s.clip_end)
                    if math.ceil(new_x) < s.clip_end-d:
                        #print(new_x)
                        operator[new_x] = yy[i]

        else:
            xx0, yy0 = s.ease_funs.get_range_spline(line, x_start, x_end, y_start[0], y_end[0])
            xx1, yy1 = s.ease_funs.get_range_spline(line, x_start, x_end, y_start[1], y_end[1])
            if xx0.min() >= 0:
                for i, elem in enumerate(yy0):
                    if xx0[i] >= 0:
                        operator[round(xx0[i])] = {1: yy0[i], 2: yy1[i], 3: 0.0}
                        #print(f"{xx0[i]:>3}   {yy0[i]:>3}  | {yy1[i]:>3}")
            elif s.add_intro_outro:
                for i, elem in enumerate(yy0):
                    new_x = round(xx0[i]  + s.clip_end)
                    if math.ceil(new_x) < s.clip_end-d:
                        #print(f"{new_x:>3}   {yy0[i]:>3}  | {yy1[i]:>3}")
                        #print(new_x)
                        operator[new_x] =  {1: yy0[i], 2: yy1[i], 3: 0.0}
                #time.sleep(0.005)
            

    def apply_transition(s, transition_frame, operator, delta_secs, y_start, y_end, line):    
        #delta_frames = delta_secs*fps
        s.apply_curve(line.line, transition_frame-delta_secs*s.ctx.fps, transition_frame, 
                    y_start, y_end, operator, line_name= line.name + "_line" )
        s.apply_curve(line.opposite, transition_frame, transition_frame+delta_secs*s.ctx.fps, 
                    y_end, y_start, operator, line_name= line.name + "_opposite")
        
    def random_curve(s):
        return getattr(s.ease_funs, random.choice(s.ease_funs.function_l[0:10]) + "_yline")

    def text_curve(s):
        ll = ['easeInCirc', 'easeInElastic', 'easeInExpo', 'easeInBack', 'easeInBounce']
        return getattr(s.ease_funs, random.choice(ll) + "_yline")

    def apply_random_transition(s, i, transition_frame, dir, cur_list):
        # expected_clip_end = s.ctx.transition_delta*s.ctx.tot_transitions
        # factor = s.clip_end / expected_clip_end
        # transition_frame = transition_frame*factor
        logging.info(f"Applying transition {i}, at frame {transition_frame}, direction: {dir}")
        r = random.uniform; r2 = random.randint
        t_d = r(0.5, 0.8)
        t_b = r(0.25, 0.45)
        t_size = (r(0.9, 1.1), r(2.0, 2.6))
        #dir = random.choice([(0,0),(1,0),(1,1),(0,1)])
        t_center = ((r(0.4, 0.6), r(0.4, 0.6)), (r(dir[0]-0.1, dir[0]+0.1), r(dir[1]-0.1, dir[1]+0.1)))
        t_angle = (r(-5, 5), r(30, 40)*(-1 if i%2 == 0 else 1 ))
        i = max(i, 0)
        s.apply_transition(transition_frame, s.tr_tool.Size,   t_d, t_size[0], t_size[1], cur_list[0][i])
        s.apply_transition(transition_frame, s.tr_tool.Center, t_d, t_center[0] , t_center[1], s.ease_funs.easeInQuart_yline) #cur_list[1][i])
        if s.plot:
            s.plot_center(transition_frame)
        s.apply_transition(transition_frame, s.tr_tool.Angle,  t_d,  t_angle[0], t_angle[1], cur_list[2][i])
        s.apply_transition(transition_frame, s.dblur.Length,   t_b, 0, 0.06, cur_list[3][i])
        s.apply_transition(transition_frame, s.dblur.Glow,     t_b, 0, 0.3, cur_list[4][i])
        s.apply_curve(np.linspace(dir[2],dir[2],100), transition_frame-t_b*s.ctx.fps, transition_frame+t_b*s.ctx.fps, dir[2], dir[2], s.dblur.Angle, f"dir {dir[2]}")


    def apply_text_transitions(s):
        text_dirs_l = [(1,0), (-1, 0), (0, 1), (0, -1), (1,1), (-1,-1), (-1,1), (1,-1) ]

        s.textp.Size[0] =  0.033 if s.clip_w > s.clip_h else 0.07    #at 1080p 0.055 #at 1920x1920 0.08
        t_size = s.textp.Size[0]

        s.textp.Center =  {1: 0.5, 2: 0.145 if random.randint(1,1) else 0.855, 3: 0.0} if not s.adding_lyrics() else {1: 0.5, 2: 0.855, 3: 0.0}
        t_center = s.textp.Center[0]
        t_center = (t_center[1], t_center[2])
        dir =  random.choice(text_dirs_l)
        ext_point = point_displacement(t_center, dir, 0.74)

        text_frame =  max(101, s.clip_end*0.05) #//2
        s.textp.Center[text_frame-101]  =  {1: -10, 2: -10, 3: 0.0}
        s.textp.Center[0]  = {1: -10, 2: -10, 3: 0.0}
        # for ii in range(0, int(text_frame)):
        #     s.textp.Center[ii] = {1: -10, 2: -10, 3: 0.0}
            #s.textp.Size[ii ] = t_size
        logging.info(f"Applying text transitions..")
        cc1 = s.text_curve()
        s.apply_curve(cc1.opposite, text_frame-100, text_frame, (ext_point[0], ext_point[1]), t_center, s.textp.Center, line_name=cc1.name + "_opposite")
        cc2 = s.text_curve()
        s.apply_curve(cc2.opposite, text_frame-100, text_frame, random.uniform(0.25, 0.25), t_size, s.textp.Size,  line_name=cc2.name + "_opposite")

        angle_dict = [ s.textp.AngleX, s.textp.AngleY, s.textp.AngleZ]
        angle_l = [iii for iii in range(random.randint(1,3))]
        angle_l = [0,1,2]

        cc3 = s.text_curve()
        random.shuffle(angle_l)
        r = random.uniform
        for i, angle in enumerate(angle_l):
            t_angle =   r(30, 60) * (-1 if random.randint(0,1) else 1 )
            angle_dict[angle][text_frame-101] = 0
        # apply_transition(text_frame, angle_dict[angle], 1,  0, t_angle, cc3)
            s.apply_curve(cc3.line,     text_frame-100, text_frame, t_angle, -t_angle, angle_dict[angle], cc3.name + "_line")
            s.apply_curve(cc3.opposite, text_frame, text_frame+100, -t_angle, 0, angle_dict[angle],  cc3.name + "_opposite")

            #s.apply_curve(cc3.line, text_frame, text_frame+60, t_angle, 0, angle_dict[angle])
            
        s.textp.Center[s.clip_end-200] =  {1: t_center[0], 2: t_center[1], 3: 0.0}

        s.textp.Center[s.clip_end-100] =  {1: -0, 2: -2, 3: 0.0}

    def apply_video_transitions(s):
        dir_list = []
        dirs_l = [(0.0, 0.0, 225), (1.0, 0.0, 315), (1.0, 1.0, 45), (0.0, 1.0, 135), 
                (0.5, 0.0, 270), (1.0, 0.5, 0), (0.5, 1.0, 90), (0.0, 0.5, 180) ]
        for x in range(math.ceil(s.ctx.tot_transitions/len(dirs_l))): #4 directions
            random.shuffle(dirs_l)
            dir_list+= dirs_l[:]

        curve_list = []
        for y in range(5): #need 5 curves per transition
            shuffled_l = []
            for x in range(math.ceil(s.ctx.tot_transitions/10)): # 10 ease in curves.
                tmp = s.ease_funs.function_l[0:10]
                random.shuffle(tmp)
                shuffled_l += tmp

            curve_list.append([getattr(s.ease_funs, elem + "_yline") for elem in shuffled_l] )
            
        
        if len(s.ctx.custom_video) == 0:
            for i in range(0, s.ctx.tot_transitions):
                s.apply_random_transition(i, s.ctx.avee_fragments_info[i].frame_end, dir_list[i], curve_list) # i*s.ctx.transition_delta
        else:
            #s.apply_random_transition(0, int(-s.clip_fps*2), dir_list[random.randint(0, len(dir_list)-1)], curve_list)
            s.apply_random_transition(0, int(s.clip_end), dir_list[random.randint(0, len(dir_list)-1)], curve_list) 
            s.apply_curve(s.ease_funs.easeOutSine_yline.line, 0, 5*s.ctx.fps, 0.93, 0.3, s.glow.Glow, f"dir easeInExpo")
            #easeOutExpo easeOutQuart 
            

                

    def render(s, codec):
        s.project.SetRenderSettings({"SelectAllFrames" : 1, "TargetDir" : s.ctx.input_f.out_fld, "CustomName": f"{s.ctx.input_f.basename}_dav.mp4", "AudioSampleRate": random.choice([48000, 44100]) })
        #s.project.SetRenderSettings({"MarkIn" : 0, "MarkOut" : 20, "TargetDir" : s.ctx.input_f.out_fld, "CustomName": f"{s.ctx.input_f.basename}_dav.mp4"})int(s.clip_end-1)
        # aa = s.project.GetRenderCodecs()
        # aa2 = s.project.GetRenderFormats()
        # aa3 = s.project.GetCurrentRenderFormatAndCodec()
        ret = s.project.SetCurrentRenderFormatAndCodec("mp4",  codec)
        ret= s.project.AddRenderJob()
        logging.info(f"Starting render..")

        s.project.StartRendering()
        while s.project.IsRenderingInProgress():
            logging.info("Waiting for render to finish..")
            time.sleep(1)

        with open(s.ctx.input_f.out_fld + "\\lenght.txt", "w") as fff:
            dur = get_duration(s.ctx.input_f.dav_final_file)
            fff.write(str(dur))

        import metadata
        metadata.randomize_metadata(s.ctx.input_f.dav_final_file)

if __name__ == "__main__3":
    print("hello")
    audio_fld = f"{app_env.ld_shared_folder}\\"

    nt = namedtuple("name_storage", "android_name win_name basename dirpath")

    audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

    f = "00019v2_s.wav"
    input_file_ = audio_fld + "//" + f

    ctx = context("lond1", input_file_, 24)
    ctx.text = "gel"
    dav = dav_handler(ctx, overwrite=1)



