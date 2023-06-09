from avee_utils import name_storage
from configparser import ConfigParser
from avee_utils import *
import queue, app_logging, logging, shutil, sql_utils, aws_python, dav

class context():
    def __init__(s, instance_name, input_file, extra_frames) -> None:
        s.instance_name = instance_name
        s.extra_frames = extra_frames
        s.out_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\\"
        s.input_f = name_storage(input_file,  s.out_fld, s.instance_name)
        config = ConfigParser()
        ini_file = s.input_f.dirpath + "\\" + s.input_f.basename + ".ini"
        config.read(ini_file)

        s.bpm = config.getint('main', 'bpm')
        s.s_m = config.getint('main', 's_m')
        s.s_sec = config.getint('main', 's_sec')
        s.s_ms = config.getint('main', 's_ms')
        s.bars = config.getint('main', 'bars')
        s.bars_per_template = config.getint('main', 'bars_per_template')
        s.beats_per_bar = config.getint('main', 'beats_per_bar')

        s.td_start = datetime.timedelta(minutes=s.s_m, seconds=s.s_sec, milliseconds=s.s_ms)
        s.fps = 60 #59940/1000
        s.time_per_beat = (60/s.bpm)
        s.frames_per_beat = s.fps * s.time_per_beat
        s.frames_per_bar = s.frames_per_beat * s.beats_per_bar
        s.transition_delta = s.frames_per_bar * s.bars_per_template
        s.tot_transitions = s.bars // s.bars_per_template

        s.nb_tasks = s.bars//s.bars_per_template
        s.black_f = f"{s.input_f.out_fld}\\black_f.mp4".replace("\\\\", "\\")
        s.black_f = s.black_f.replace("\\\\", "\\")
        s.reboot_inst = 1
        s.stop_inst = 1
        s.text = None
        s.add_lyrics = True



avee_queue = queue.Queue()
dav_queue = queue.Queue()
aws_queue = queue.Queue()

def avee_worker(rows, input_file, fr_l, add_lyrics=True):
    logging.info("Avee worker started")
    shutil.copy(r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\00034.wav", r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\00001.wav")
    assert(get_duration(r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\00001.wav", "Audio") > 60*1000)

    sql =  sql_utils.sql_()
    for  i, row in enumerate(rows):
        ctx, do = init_task(row[3], input_file, sql, fr_l[i])
        ctx.add_lyrics = add_lyrics
        if not do:
            continue
        if os.path.isfile(ctx.input_f.dav_final_file) or os.path.isfile( os.path.isfile(ctx.input_f.avee_final_file)):
            logging.info("Dav or avee final files already exist, skipping avee task")
        else:
            perform_avee_task(ctx.input_f, ctx.bpm, (ctx.s_m, ctx.s_sec, ctx.s_ms), ctx.bars, ctx.bars_per_template, extra_fames=fr_l[i],  beats_per_bar=ctx.beats_per_bar)
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

def general_task(instance, input_file, sql, extra_frames):

    t0 = time.time()

    ctx, do = init_task(instance, input_file, sql, extra_frames)
    if not do: return

    perform_avee_task(ctx.input_f, ctx.bpm, (ctx.s_m, ctx.s_sec, ctx.s_ms), ctx.bars, ctx.bars_per_template, extra_frames=ctx.extra_frames,  beats_per_bar=ctx.beats_per_bar)

    davinci = dav.dav_handler(ctx)
    
    aws = aws_python.aws_handler(sql)# aws.local=0
    aws.aws_task( ctx, hashtags=app_logging.get_hashtags(random.randint(2,3) )) #aws.aws_task( ctx, reboot_inst=1, stop_instance=False, hashtags=app_logging.get_hashtags(7), do_yt="f", yt_ch_id="UCRFWvTVdgkejtxqh0jSlXBg")

    t4 = time.time()

    logging.info(f"Times: total = {str(datetime.timedelta(seconds=t4-t0))} ")

