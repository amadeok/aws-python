from avee_utils import name_storage
from configparser import ConfigParser
from avee_utils import *
import queue, app_logging, logging, shutil, sql_utils, aws_python, dav
import json
import app_env
import utils.process_videos as pv, math, tempfile
import subprocess
import unreal

class avee_fragment():
    def __init__(self, ctx, audio_start, audio_end) -> None:
        self.audio_start = audio_start 
        self.audio_end = audio_end 
        self.dur = self.audio_end - self.audio_start #ctx.time_per_beat*ctx.beats_per_bar*ctx.bars_per_template#  self.abs_end - self.abs_start 
        self.dur_fps = self.dur*ctx.fps
        self.frame_start = audio_start*ctx.fps
        self.frame_end =  audio_end*ctx.fps
    def __repr__(self) -> str:
        return " ".join([f'{key}: {value}' for key, value in vars(self).items() if not key.startswith('__')])
    
def find_file(folder, filename):
    for root, dirs, files in os.walk(folder):
        if filename in files:
            return os.path.join(root, filename)
    return None

class context():
    def __init__(s, instance_name, input_file, extra_frames, cloud_file_details = None, custom_video="", secondary_text="", input_f=None) -> None:
        s.instance_name = instance_name
        s.extra_frames = extra_frames
        s.out_fld = os.getenv('OUTPUT_FOLDER') #f"{app_env.output_folder}"
        s.input_f = input_f if input_f else  name_storage(input_file,  s.out_fld, s.instance_name)
        if not os.path.isdir(s.input_f.dirpath): os.makedirs(s.input_f.dirpath)
        if not os.path.isdir(s.input_f.out_fld): os.makedirs(s.input_f.out_fld)
        s.using_unreal = os.path.isfile(s.input_f.guessed_midi_file)
       
        if cloud_file_details == None:
            pass
            s.bpm = 60
            s.beats_per_bar = 4
            s.bars_per_template = 4
            s.bars = 4
            s.avee_custom_lenghts = {}
            # config = ConfigParser()
            # ini_file = s.input_f.dirpath + "\\" + s.input_f.basename + ".ini"
            # config.read(ini_file)
            # s.bpm = config.getint('main', 'bpm')
            # # s.s_m = config.getint('main', 's_m')
            # # s.s_sec = config.getint('main', 's_sec')
            # # s.s_ms = config.getint('main', 's_ms')
            # s.bars = config.getint('main', 'bars')
            # s.bars_per_template = config.getint('main', 'bars_per_template')
            # s.beats_per_bar = config.getint('main', 'beats_per_bar')
            # s.avee_custom_lenghts = json.loads(config.get('main', 'avee_custom_lenghts', fallback="{}"))
        else:
            s.bpm = cloud_file_details['bpm']
            s.bars =cloud_file_details['bars']
            s.bars_per_template = cloud_file_details['bars_per_template']
            s.beats_per_bar = cloud_file_details['beats_per_bar']
            s.avee_custom_lenghts = cloud_file_details['avee_custom_lenghts']
        
        s.custom_video = custom_video

        if len(custom_video):
            if custom_video == "random":
                s.custom_video = pv.get_random_sm_video()# random.choice(pv.get_sm_videos())
            elif not os.path.isfile(custom_video):
                p = os.path.basename(custom_video)
                found = find_file( os.getenv("SM_VIDEOS"), p)
                if not found:
                    raise Exception(f"""Unabled to find custom video {custom_video} in {os.getenv("SM_VIDEOS")}""")
                s.custom_video = found
                
                    
        s.custom_video_info = pv.get_video_info_cv(s.custom_video) if s.custom_video != "" else None
        s.secondary_text = secondary_text
        # s.td_start = datetime.timedelta(minutes=s.s_m, seconds=s.s_sec, milliseconds=s.s_ms)
        s.fps = s.custom_video_info[3] if custom_video != "" else 60 #59940/1000
        s.time_per_beat = (60/s.bpm) #its 60 not fps
        s.frames_per_beat = s.fps * s.time_per_beat
        s.frames_per_bar = s.frames_per_beat * s.beats_per_bar
        s.transition_delta = s.frames_per_bar * s.bars_per_template
        s.tot_transitions = s.bars // s.bars_per_template
        s.default_dur = s.time_per_beat*s.beats_per_bar*s.bars_per_template
        
        s.nb_tasks = s.bars//s.bars_per_template
        s.black_f = f"{s.input_f.out_fld}\\black_f.mp4".replace("\\\\", "\\")
        s.black_f = s.black_f.replace("\\\\", "\\")
        s.reboot_inst = 1
        s.stop_inst = 1
        s.text = None
        s.add_lyrics = True
        
        s.avee_fragment_lenghts = [None  for x in range(s.tot_transitions)]
        for key, value in s.avee_custom_lenghts.items():
            s.avee_fragment_lenghts[int(key)] = value["dur"]
            print(key, ':', value)
        s.avee_fragment_lenghts = [elem if elem else s.default_dur  for elem in s.avee_fragment_lenghts]
        s.avee_fragments_info = []
        
        stream_pos = 0
        for i, cur_dur in enumerate(s.avee_fragment_lenghts):
            s.avee_fragments_info.append( avee_fragment(s, stream_pos, stream_pos+cur_dur ))
            stream_pos+=cur_dur
        print()
            



avee_queue = queue.Queue()
dav_queue = queue.Queue()
aws_queue = queue.Queue()

def avee_worker(rows, input_file, fr_l, add_lyrics=True):
    logging.info("Avee worker started")
    shutil.copy(f"{app_env.ld_shared_folder}\00034.wav", f"{app_env.ld_shared_folder}\00001.wav")
    assert(get_duration(f"{app_env.ld_shared_folder}\00001.wav", "Audio") > 60*1000)

    sql =  sql_utils.sql_()
    for  i, row in enumerate(rows):
        ctx, do = init_task(row[3], input_file, sql, fr_l[i])
        ctx.add_lyrics = add_lyrics
        if not do:
            continue
        if os.path.isfile(ctx.input_f.dav_final_file) or os.path.isfile( os.path.isfile(ctx.input_f.avee_final_file)):
            logging.info("Dav or avee final files already exist, skipping avee task")
        else:
            perform_avee_task(ctx.input_f, ctx.bpm, ctx.bars, ctx.bars_per_template, extra_fames=fr_l[i],  beats_per_bar=ctx.beats_per_bar) # to do fix
        logging.info(f"Avee worker FINISHED task for instance {ctx.instance_name}")
        dav_queue.put(ctx)
    dav_queue.put(-1)
        

def dav_worker():
    logging.info("Dav worker started")
    while 1:
        logging.info("Dav worker waiting..")
        ctx = dav_queue.get()
        if ctx == -1:
            aws_queue.put(-1)
            logging.info(f"Dav worker received end signal, returning")
            return    
        logging.info(f"Dav worker GOT task for instance {ctx.instance_name}")
        davinci = dav.dav_handler(ctx)  
        logging.info(f"Dav worker FINISHED task for instance {ctx.instance_name}")
        aws_queue.put(ctx)

def aws_worker():
    logging.info("Aws worker started")
    aws = aws_python.aws_handler()
    while 1:
        logging.info("Aws worker waiting..")
        ctx = aws_queue.get()
        if ctx == -1:
            logging.info(f"Aws worker received end signal, returning")
            return    
        logging.info(f"Aws worker GOT task for instance {ctx.instance_name}")
        aws.aws_task( ctx, hashtags=app_logging.get_hashtags(random.randint(2,3)))
        logging.info(f"Dav worker FINISHED task for instance {ctx.instance_name}")
        

def init_task(instance, input_file, sql, extra_frames):
    #davinci = dav.dav_handler(ctx, "text")
    
    row = sql.get_row(instance) #aws_id, yt_id, region,  name, tt_mail, yt_mail , ch_name = row

    ctx = context(instance, input_file, extra_frames)

    do_tt, do_yt = aws_python.get_tt_and_ty_do(sql, ctx, instance, row)
    add_text  = row[9]
    
    logging.info("")
    if not do_tt and not do_yt and not '!' in row[3]:
        logging.info(f"No task to perform according to database for instance {instance} name {input_file}")
        return (ctx,False)
    else:
        logging.info(f"Performing general task instance {instance} name {input_file}")
    logging.info("")

    ctx.text = None if not add_text else random.choice(app_logging.possible_texts) 

    return (ctx, True)

def general_task_aws(instance, input_file, sql, extra_frames_, do_aws=False):

    t0 = time.time()

    ctx, do = init_task(instance, input_file, sql, extra_frames_)
    if not do: return

    perform_avee_task(ctx.input_f, ctx.bpm, ctx.bars, ctx.bars_per_template, ctx.extra_frames,  beats_per_bar=ctx.beats_per_bar)

    davinci = dav.dav_handler(ctx)
    if do_aws:
        aws = aws_python.aws_handler(sql)# aws.local=0
        aws.aws_task( ctx, hashtags=app_logging.get_hashtags(random.randint(2,3) )) #aws.aws_task( ctx, reboot_inst=1, stop_instance=False, hashtags=app_logging.get_hashtags(7), do_yt="f", yt_ch_id="UCRFWvTVdgkejtxqh0jSlXBg")

    t4 = time.time()

    logging.info(f"Times: total = {str(datetime.timedelta(seconds=t4-t0))} ")
    
def general_task(input_file, extra_frames_=[], add_text=False, upload=False, cloud_file_details=None, custom_video="", secondary_text="", input_f=None):

    t0 = time.time()

    ctx = context(None, input_file, extra_frames_, cloud_file_details=cloud_file_details, custom_video=custom_video, secondary_text=secondary_text, input_f=input_f)

    ctx.text = None if not add_text else random.choice(app_logging.possible_texts) 

    if not len(ctx.custom_video):
        perform_avee_task(ctx.input_f, ctx.bpm, ctx.bars, ctx.bars_per_template, ctx.avee_fragments_info, ctx.extra_frames,  beats_per_bar=ctx.beats_per_bar, fps=ctx.fps)
    else:
        logging.info(f"Using custom video {ctx.custom_video}")
        if not os.path.isfile(ctx.input_f.custom_video_final_file):
            info = pv.get_video_info_cv(ctx.custom_video)
            #info2 = pv.get_video_info_ffmpeg(ctx.custom_video)
            dur = pv.get_video_duration_ffmpeg(ctx.input_f.input_path, "audio")  
            
            pre_file = ctx.custom_video
            if dur > info[0]:
                
                pre_file = os.path.join(tempfile.gettempdir(), "0output.mp4")
                times = math.ceil(dur/info[0])
                logging.info(f"Custom video has shorter length than input audio, looping with reverse {dur} {info[0]}")
                #cmd = f"""ffmpeg -i {ctx.custom_video}  -filter_complex "[0]reverse[r];[0][r]concat,loop={math.floor(times/2)}:{(info[0]*2)*info[3]},setpts=N/{info[3]}/TB" {pre_file}   -y""" #os.path.dirname(custom_vi) #

                bin = r"ffmpeg.exe"
                #cmd = f"""{bin} -i {ctx.custom_video}  -filter_complex "[0]reverse[r];[0][r]concat,loop={math.floor(times/2)}:{(info[0]*2)*info[3]}" {pre_file}   -y"""
                cmd = [ bin, "-i", ctx.custom_video, "-filter_complex", f"[0]reverse[r];[0][r]concat,loop={math.floor(times/2)}:{(info[0]*2)*info[3]}", pre_file, "-y" ]
                logging.info(f"loop reverse cmd {cmd}")
                subprocess.run(cmd, check=True)
                #os.system(cmd)
            
            #cmd = f'ffmpeg -i {pre_file}  -i {ctx.input_f.input_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest "{ctx.input_f.custom_video_final_file}" -y'
            audio_offset = os.getenv("AUDIO_OFFSET") #-0.028
            if ctx.using_unreal:
                if os.path.isfile(ctx.input_f.unreal_final_file):
                   logging.info(f"Unreal final file already exists, skipping")
                else:
                    tmp_unreal_file =  os.path.join(tempfile.gettempdir(), "temp_unreal_video.mp4")
                    unreal.unreal_task(pre_file, ctx.input_f.guessed_midi_file, tmp_unreal_file, input_file)
                    addAudio(input_file, ctx, pre_file, tmp_unreal_file, audio_offset)
            else: 
                addAudio(input_file, ctx, pre_file, tmp_unreal_file, audio_offset)

            #os.system(cmd)
        else:
            logging.info(f"Custom video final file already exists, skipping ")
            
    davinci = dav.dav_handler(ctx)
    if upload:
        pass #TO DO
        # aws = aws_python.aws_handler(sql)# aws.local=0
        # aws.aws_task( ctx, hashtags=app_logging.get_hashtags(random.randint(2,3) )) 

    t4 = time.time()

    logging.info(f"Times: total = {str(datetime.timedelta(seconds=t4-t0))} ")
    return ctx

def addAudio(input_file, ctx, pre_file, tmp_unreal_file, audio_offset):
    cmd = ["ffmpeg","-i", tmp_unreal_file if ctx.using_unreal else  pre_file, 
                    "-itsoffset", str(audio_offset), "-i", input_file, "-c:v", "copy","-c:a", "aac","-map", "0:v:0","-map", "1:a:0","-shortest",
                    ctx.input_f.unreal_final_file if ctx.using_unreal else ctx.input_f.custom_video_final_file,"-y" ]
            
    subprocess.run(cmd, check=True)
    logging.info(f"Adding audio cmd {cmd}")
