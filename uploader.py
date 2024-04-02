import shlex
import time
import autoChromePy
import autopyBot
import random
from avee_utils import avee_context

ac = autoChromePy.autoChrome.autoChromePy()
_del = autopyBot.autopy.fun_delegate
import app_logging, logging

#ap = autopyBot.autopy.autopy()

def procHash(title_hashs, add_short):
    title_hashs_ = title_hashs.split(" ")
    if add_short:
        title_hashs_.append("#shorts")
    random.shuffle(title_hashs_)
    title_hashs = " ".join(title_hashs_)
    return title_hashs

def insta_task(title_hashs="#music #piano", upload_file=r"C:\Users\amade\Videos\20240318_170455.mp4", track_title="Op. 42 - Cristian Kusch"):
    title_hashs = procHash(title_hashs, True)

    actx = avee_context(hei= 960+50, wid=540, prefix="540p_", autopyFld="images_insta_avee")
    at: autopyBot.autopy.autopy = actx.a

    actx.start_adb_server()
    #actx.hwnd, actx.ld_win= actx.restart_ld_player()
    actx.wait_for_device()

    adb = actx.adb
    
    adb(" am force-stop com.instagram.android")
    adb(f"""push  "{upload_file}" /mnt/shared/Pictures/ainsta/1234.mp4""", False)
    time.sleep(0.5)
    actx.update_file_system()
    time.sleep(1)
    adb("am start -a android.intent.action.VIEW -n com.instagram.android/.activity.MainTabActivity")
    
    ret = at.find([at.i.plus, at.i.plus_black], loop=2, click_function= actx.tap, confidence=0.95)
        
    ret = at.find([at.i.menu_reel, at.i.menu_reel_bold], loop=2, confidence=0.95)
    if ret == at.i.menu_reel: actx.tap(ret.found)
    
    ret = at.find([at.i.recents, at.i.videos, at.i.ainsta_black], loop=2, confidence=0.95)
    if ret != at.i.ainsta_black:
        actx.tap(ret.found)
        ret = at.find([at.i.ainsta], loop=2, confidence=0.95, click_function= actx.tap)
        ret = at.find([at.i.ainsta_black], loop=2, confidence=0.95, click_function=[actx.tap, 0, 200])
    else:
        actx.tap(ret.found, 0, 200)

    ret = at.find([at.i.next], loop=2, confidence=0.95, click_function= actx.tap)
    
    ret = at.find([at.i.new_reel], loop=2, confidence=0.95)

    #actx.scroll(at.i.advanced_settings, False)
    
    ret = at.find([at.i.write_a_caption_or], loop=2, confidence=0.95, click_function= actx.tap)

    adb("input text " + f'{shlex.quote(title_hashs )} ')
    time.sleep(1)    
    adb(f" input keyevent 61") #tab
    
    ret = at.find([at.i.rename_audio], loop=2, confidence=0.95, click_function=actx.tap)
    
    ret = at.find([at.i.original_audio], loop=2, confidence=0.95, do_until=_del(actx.tap, [ret.found], 2))
    [adb(f" input keyevent 67") for x in range(25) ] #del

    adb("input text " + f'{shlex.quote(track_title )}')

    ret = at.find([at.i.audio_name_tick], loop=2, confidence=0.95, click_function=actx.tap)
    
    time.sleep(0.5)
    ret = at.find(at.i.share_to_reels_label, confidence=0.95)
    if ret:
        ret = at.find([at.i.also_share_to_reels_off, at.i.also_share_to_reels_on], loop=2, confidence=0.95)
        if ret == at.i.also_share_to_reels_on: actx.tap(ret.found)

    ret = at.find([at.i.share], loop=2, confidence=0.95, click_function=actx.tap)

    actx.adb("input swipe 200 20 220 500")    
    ret = at.find([at.i.battery], loop=2, confidence=0.95)
    
    ret = at.find([at.i.reel_uploaded], loop=2, timeout=600, confidence=0.95)
    
    if ret: logging.info("INSTA_SUCCESS")

    adb(" am force-stop com.instagram.android")
    adb(f" input keyevent 4") #back
    if not ret: raise Exception("Instagram task failed")


insta_task()