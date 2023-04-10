
import time, subprocess as sp
import logging, math
# time.sleep(1)
import random
import time, shlex, random, numpy as np
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns
import spline, webcolors
import matplotlib.pyplot as plt

import DaVinciResolveScript as dvr_script


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



class dav_handler():
    def __init__(s, ctx) -> None:



        s.fonts = ['Open Sans', 'Arial Rounded MT Bold', 'Bauhaus 93', 'Berlin Sans FB', 'Cambria Math', 'Comic Sans MS', 'Eras Bold ITC', 'Eras Demi ITC', 'Gill Sans Ultra Bold Condensed', 'Harrington', 'High Tower Text', 'Imprint MT Shadow', 'Jokerman', 'Kristen ITC',"Maiandra GD","Matura MT Script Capitals","MS PGothic","MV Boli","Trebuchet MS","Tw Cen MT","Tw Cen MT Condensed Extra Bold","Ubuntu","Open Sans"]
        s.ctx = ctx
        s.init()
        
        s.ease_funs = spline.ease_funs()
        s.add_intro_outro = 0

        ret = s.resolve.OpenPage("Edit")

        s.AddMediaItem()

        s.get_clip_info()

        s.plot = 1
        if s.plot:
            s.init_plt()

        s.set_clip_properties()
        time.sleep(1) #without this AddTool() fails

        s.get_comp()

        s.tr_tool = s.add_transform_tool()
        
        s.add_tools_and_modifiers()

        s.get_random_text_style(s.textp, 6, s.fonts)

        s.textp.StyledText = "Follow cristian_k_music\n" + "on IG"
        time.sleep(0.2)
        s.add_text_effects()

        s.apply_text_transitions()

        s.apply_video_transitions()

        s.render()
        
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

        projectManager.LoadProject("empty") 
        time.sleep(1)
        ret = projectManager.CloseProject(s.ctx.input_f.basename)

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
            added = s.MediaStorage.AddItemListToMediaPool(s.ctx.input_f.avee_final_file)

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
        ret = s.clip.SetProperty("ZoomX", 2.35) #2.35 if source is 1080p, 1.4-1.5 if 1920x1920

    def get_clip_info(s):
        raw_clips = s.folder.GetClipList()
        raw_clip = raw_clips[0]
        p = raw_clip.GetClipProperty()
        s.clip_end = float(p["End"])
        s.clip_fps = p["FPS"]


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

    def add_tools_and_modifiers(s):
        s.dblur = s.comp.AddTool("DirectionalBlur", -32768, -32768)
        ret = s.dblur.AddModifier("Length", "BezierSpline")
        ret = s.dblur.AddModifier("Glow", "BezierSpline")
        ret = s.dblur.AddModifier("Angle", "BezierSpline")

        s.main_shake = s.comp.AddTool("ofx.com.blackmagicdesign.resolvefx.CameraShake", -32768, -32768) #for rest
        s.main_shake.MotionScale = 0.378
        s.main_shake.SpeedScale = 0.126

        s.textp = s.comp.AddTool("TextPlus", -32768, -32768)
        ret = s.textp.AddModifier("Size", "BezierSpline")
        ret = s.textp.AddModifier("AngleX", "BezierSpline")
        ret = s.textp.AddModifier("AngleY", "BezierSpline")
        ret = s.textp.AddModifier("AngleZ", "BezierSpline")
        s.textp.Center = s.comp.Path()
        time.sleep(0.5)
        #ff = s.textp.GetInput("Font")
        s.textp.Enabled2 = 1

    def add_text_effects(s):
        s.comp.SetActiveTool(s.textp)

        s.textp_shake = s.comp.AddTool("CameraShake", -32768, -32768) #for text
        s.textp_shake.XDeviation = 0.83
        s.textp_shake.YDeviation = 0.83
        s.textp_shake.RotationDeviation = 0.61
        s.textp_shake.Randomness = 0.5
        s.textp_shake.OverallStrength = 0.007
        s.textp_shake.Speed = 0
        s.textp_rays = s.comp.AddTool("Fuse.OCLRays", -32768, -32768) 
        s.textp_rays.Blend = 0.055# 0.4
        s.textp_shadow = s.comp.AddTool("ofx.com.blackmagicdesign.resolvefx.DropShadow", -32768, -32768) 


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
                        print(f"{xx0[i]:>3}   {yy0[i]:>3}  | {yy1[i]:>3}")
            elif s.add_intro_outro:
                for i, elem in enumerate(yy0):
                    new_x = round(xx0[i]  + s.clip_end)
                    if math.ceil(new_x) < s.clip_end-d:
                        print(f"{new_x:>3}   {yy0[i]:>3}  | {yy1[i]:>3}")
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
        expected_clip_end = s.ctx.transition_delta*s.ctx.tot_transitions
        factor =  s.clip_end/expected_clip_end
        transition_frame = transition_frame*factor
        logging.info(f"Applying transition {i}, at frame {transition_frame}, direction: {dir}")
        r = random.uniform; r2 = random.randint
        t_d = r(0.5, 0.8)
        t_b = r(0.25, 0.45)
        t_size = (r(0.9, 1.1), r(2.0, 2.6))
        #dir = random.choice([(0,0),(1,0),(1,1),(0,1)])
        t_center = ((r(0.4, 0.6), r(0.4, 0.6)), (r(dir[0]-0.1, dir[0]+0.1), r(dir[1]-0.1, dir[1]+0.1)))
        t_angle = (r(-5, 5), r(30, 40)*(-1 if i%2 == 0 else 1 ))

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

        s.textp.Center =  {1: 0.5, 2: 0.145 if random.randint(1,1) else 0.855, 3: 0.0}
        s.textp.Size[0] =  0.050 #at 1080p 0.055 #at 1920x1920 0.08
        t_size = s.textp.Size[0]
        t_center = s.textp.Center[0]
        t_center = (t_center[1], t_center[2])
        dir =  random.choice(text_dirs_l)
        ext_point = point_displacement(t_center, dir, 0.74)

        text_frame =  s.clip_end//2
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

        for i in range(0, s.ctx.tot_transitions):
            s.apply_random_transition(i, i*s.ctx.transition_delta, dir_list[i], curve_list)

    def render(s):
        s.project.SetRenderSettings({"SelectAllFrames" : 1, "TargetDir" : s.ctx.input_f.out_fld, "CustomName": f"{s.ctx.input_f.basename}_dav.mp4"})
        ret= s.project.AddRenderJob()
        logging.info(f"Starting render..")

        s.project.StartRendering()
        while s.project.IsRenderingInProgress():
            logging.info("Waiting for render to finish..")
            time.sleep(1)