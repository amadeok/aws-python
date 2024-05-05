import datetime
import json
import shlex
import autoChromePy
from bson import ObjectId
from avee_utils import avee_context
import hashlib
import asyncio,logging,pyautogui as pg, subprocess as sp, os
import threading
import uuid
import traceback
import random
import time
from autoChromePy.autoChrome import  autoChromePy, htmlE, fun_delegate as async_fun_delegate, run_as_async
import autopyBot
import pygetwindow as gw
import win32gui
import win32process
import re, psutil
import inspect, copy
import arduino.turn.arduino_helper as arduino_helper
import string
import app_logging

test_file =  r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\None_00022v2_s\00022v2_s_dav.mp4"
#test_file = r"C:\Users\amade\Videos\20240318_170455.mp4"
test_yt_id = "UCRFWvTVdgkejtxqh0jSlXBg" # ak@g

ab = autopyBot.autopy.autopy("uploader_imgs")
ab.find_fun_timeout = 30
adel_ = async_fun_delegate
del_ = autopyBot.autopy.fun_delegate
#htmlE = autoChrome.htmlE
#test_file =  r"C:\Users\amade\Videos\002_sky pm 12 30.mkv"
ac = autoChromePy("")
_del = autopyBot.autopy.fun_delegate

#ap = autopyBot.autopy.autopy()

with open('data\hashtag_map.json', 'r') as file:
    hashtag_map = json.load(file)

def procHash(title_hashs, add_short):
    title_hashs_ = copy.deepcopy(title_hashs)
    #title_hashs_ = title_hashs.split(" ")
    if add_short:
        title_hashs_.append("#shorts")
    random.shuffle(title_hashs_)
    title_hashs_ = " ".join(title_hashs_)
    return title_hashs_



def instagram_task_avee(title_hashs = ["#piano, #originalmusic"], channel_id="", b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):
    title_hashs = procHash(title_hashs, False)

    actx = avee_context(hei= 960+50, wid=540, prefix="540p_", autopyFld="images_insta_avee")
    if actx.move_wins:
        actx.move_windows_out_the_way()

    at: autopyBot.autopy.autopy = actx.a
    at.find_fun_timeout = 40

    actx.start_adb_server()
    #actx.hwnd, actx.ld_win= actx.get_ld_player_handle()
    actx.wait_for_device()
    
    adb = actx.adb
    

    adb(" am force-stop com.instagram.android")
    
    adb("rm /mnt/shared/Pictures/ainsta/*")
    time.sleep(0.5)
    actx.update_file_system()
    time.sleep(0.5)
    # adb("am start -a android.intent.action.VIEW -n com.instagram.android/.activity.MainTabActivity")
    # time.sleep(0.5)

    name = ''.join(random.choices(string.ascii_letters + string.digits + "_-.", k=5))
    adb(f"""push  "{upload_file}" /mnt/shared/Pictures/ainsta/{name}.mp4""", False)
    time.sleep(0.5)
    actx.update_file_system()
    actx.restart_ld_player()
    actx.wait_for_device()
    #actx.check_app_running("com.instagram.android", f"{actx.base} am start -a android.intent.action.VIEW -n com.instagram.android/.activity.MainTabActivity", [at.i.plus, at.i.plus_black])
    for x in range(60):
        adb("am start -a android.intent.action.VIEW -n com.instagram.android/.activity.MainTabActivity")
        ret = at.find([at.i.plus, at.i.plus_black], click_function= actx.tap, confidence=0.95)
        if ret: break
        time.sleep(1)
    else: raise Exception("failed to open insta?")
        
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

    # actx.adb("input swipe 200 20 220 500")    
    # ret = at.find([at.i.battery], loop=2, confidence=0.95)
    t0 = time.time()
    while 1:
        ret = at.find([at.i.reel_uploaded], confidence=0.95)
        if ret: 
            break
        if time.time() - t0 > 800: 
            logging.info("insta task uploaded image search breakout because of timeout 800 seconds")
            break
        time.sleep(1)
        ret = at.find([at.i.battery], confidence=0.95)
        if not ret:
            logging.info("insta task swiping")
            actx.adb("input swipe 200 20 220 500")    
        time.sleep(1)
    
    if ret: logging.info("INSTA_SUCCESS")

    adb(" am force-stop com.instagram.android")
    adb(f" input keyevent 4") #back
    for x in range(2):
        time.sleep(2)
        adb(f'input keyevent KEYCODE_HOME')
    if not ret: raise Exception("Instagram task failed")

async def task():
    await asyncio.sleep(2)  # Sleep for 1 second
    # ret = await ac.getElementById("avatar-btn")
    # box = await ret.getBoundingBox()
    
    # field = await ret.getField("textContent")
    # await ret.click()

    # rets = await ac.getElementsByClassName("ytd-topbar-logo-renderer")
    ret = await ac.querySelector("""[aria-label="Select file"]""")
    #ret = await ac.querySelectorAll(""".style-scope .ytd-rich-grid-media""")
    ret = await ac.getElement("/html/body/div[1]/div/div/div/div[1]/div/div/div/div/div[4]/button", "xpath")
    ret = await ac.find(htmlE('[id="contents"]', "querySelectorAll", ac), loop=1)
    logging.info(f"""----------->ret {str(ret)}""", )
    #await self.websocket.close()
    #self.server_task.cancel()
#ac.start(None)


async def instagram_task(title_hashs = ["#piano, #originalmusic"], channel_id="", b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):
    title_hashs = procHash(title_hashs, False)
          
    args = ["https://www.instagram.com/?hl=en", f'--profile-directory={edge_profile}']
    
    if b_start_browser:   await start_browser(args)
    
    create_new = await ac.find(htmlE('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]', "xpath", ac, label="create_new"), loop=2,timeout=80, timeout_exception="instgram page didn't open", do_until=adel_(start_browser, [args], 30 ), click=True)
    
    select_from_computer = await ac.find([htmlE('/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/div', "xpath", ac, label="select_from_computer"), htmlE("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/div/button", "xpath", ac, label="select_from_computer")], loop=2, click=1)#, do_until=adel_(create_new.clickCursor, [], 1, True ), click=1)
    
    await operate_file_popup( upload_file, select_from_computer.clickCursor)
    
    crop = await ac.find(htmlE("""[aria-label="Select crop"]""", "querySelector", ac, label="crop"), timeout=600, loop=2, click=1)
    
    nine_sixteen = await ac.find(htmlE("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div", "xpath", ac, label="nine_sixteen"), loop=2, click=1)
    
    for x in range(2):
        next = ab.find(ab.i.insta_next, loop=2)
        ac.ard_click.move_mouse_s(next.found[0:2])
        await asyncio.sleep(1)  
    # next = await ac.find(htmlE('/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div', "xpath", ac, label="next"), loop=2)#, do_until=adel_(create_new.clickCursor, [], 1, True ))
    # next.clickCursor(40, -40)
    
    # await asyncio.sleep(1)

    # next = await ac.find(htmlE('/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div', "xpath", ac, label="next"), loop=2, click=0)
    # next.clickCursor(40, -40)
    
    write_a_caption = await ac.find(htmlE("""[aria-label="Write a caption..."]""", "querySelector", ac, label="write_a_caption"), loop=2, click=1)
    
    ab._workaround_write(track_title  + " " + title_hashs ); await asyncio.sleep(0.5)
    
    next = ab.find(ab.i.insta_share, loop=2)
    ac.ard_click.move_mouse_s(next.found[0:2])
                    
    shared = await ac.find(htmlE("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/span", "xpath", ac, label="shared"),timeout=600, loop=2)          
                              
    
    #share = await ac.find(htmlE("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div", "xpath", ac, label="share"), loop=2, click=1)
   

    await asyncio.sleep(3)
    pass

def close_firefox():
    tries = 5
    for x in range(tries):
        pk = sp.Popen(["tasklist", "/fi", "imagename eq firefox.exe"], stdout=sp.PIPE)
        out, err = pk.communicate()
        procs = str(out.decode("utf-8"))
        if "firefox.exe" not in procs:
            break
        os.system("taskkill /f /im firefox.exe")
        time.sleep(0.5)
        if x == tries - 1:
            print("Firefox had to be terminated with taskkill")
            os.system("taskkill /f /im firefox.exe")

def terminate_processes_by_exe(exe_path):
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if not proc.info['exe']: continue 
            proc_name = proc.info['exe'].lower()
            # if "msedge" in proc_name:
            #     print("--->", proc_name)
            if proc_name == exe_path.lower():
                proc.terminate()
                logging.info(f"Terminated process with PID {proc.pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def get_window_handle_from_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def get_window_handles_with_title(title):
    window_handles = []
    windows = pg.getWindowsWithTitle('')
    for window in windows:
        # if len(window.title) > 10:
        #     print(window.title)
        if re.search(title, window.title, re.IGNORECASE):
            window_handles.append(window._hWnd)
    return window_handles

async def start_browser(args):# url, profile):
    global edge_process
    await asyncio.sleep(0.5)
    binary = r"C:\Users\amade\AppData\Local\Microsoft\Edge SxS\Application\msedge.exe"
    terminate_processes_by_exe(binary)
    for x in range(2):
        await asyncio.sleep(1)
        logging.info("closed browser...")

    cmd = [binary]# url,  f'--profile-directory={profile}']
    cmd+=args
    edge_process = sp.Popen(cmd)

    title_to_search = "Edge Canary"
    for x in range(60):
        handles = get_window_handles_with_title(title_to_search)
        if len(handles):break
        await asyncio.sleep(1)
    else: logging.info("failed to get edge window handle after 60 seconds")
    logging.info(f"Window handles with title containing '{title_to_search}' : {handles}")
    
    for h in handles:
        win32gui.MoveWindow(h, 0, 0, 1920, 1040, True)
    await asyncio.sleep(2)
    print("Browser started successfully.")
    await ac.wait_for_websocket(100)


def start_browser_sync(url, profile):
    time.sleep(0.5)
    cmd = [r"C:\Users\amade\AppData\Local\Microsoft\Edge SxS\Application\msedge.exe", url, f'--profile-directory="${profile}"']
    p = sp.Popen(cmd)
    time.sleep(2)
    print("Browser started successfully.")
    
def notified_key_press(key):
    logging.info(f"----> pressing key {key}")        
    pg.press(key)

async def operate_file_popup( file_path, do_until_fun, do_until_fun_args=[]):
    ret = ab.find(ab.i.file_name_edge, loop=1, do_until=del_(do_until_fun, do_until_fun_args, 5 ) if do_until_fun else None)
    if ac.ard_click:
        [ac.ard_click.move_mouse_s((int(ret.found[0]+50),  int(ret.found[1] ))) or await asyncio.sleep(0.6) for x in range(2)]
    else:
        [pg.click(ret.found[0]+50,   ret.found[1] ) or await asyncio.sleep(0.6) for x in range(2)]

    ab.type(file_path)
    logging.info("waiting for file_name_edge to go...")
    ab.wait_to_go(ab.i.file_name_edge, do_while=lambda: notified_key_press("enter"), sleep=5)
    logging.info("file_name_edge is gone...")
    #network.send_string("YT_SUCCESS", conn)

async def youtube_task(title_hashs = ["#piano, #originalmusic"], channel_id:str=test_yt_id,  b_start_browser=True, edge_profile:str="Default", upload_file= test_file, track_title="Op. 42 - Cristian Kusch"):

    title_hashs = procHash(title_hashs, True)
          
    args = [f"https://studio.youtube.com/channel/"+channel_id+"/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D",f'--profile-directory={edge_profile}']
    
    if b_start_browser:   await start_browser(args)

    #await ac.wait_for_websocket(100)
    
    upload_arrow = await ac.find(htmlE('burst', "id", ac), loop=2,timeout=80, timeout_exception="yt page didn't open", do_until=adel_(start_browser, [args], 30 ), click=True)
        
    await operate_file_popup( upload_file, upload_arrow.clickCursor)
      
    next_btn = await ac.find(htmlE('[label="Next"]', "querySelector", ac), loop=2, do_until=adel_(pg.press, ["enter"], 3, True ))
     
    pg.hotkey("ctrl", "a")  
    
    ab._workaround_write(track_title  + " " + title_hashs ); await asyncio.sleep(0.5)
    
    await ac.find(htmlE("/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[1]/h1", "xpath", ac, label="visibility"), loop=2, do_until=adel_(next_btn.clickCursor, [], 1, True )) 
    
    await ac.find(htmlE("/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div", "xpath", ac, label="publish"), loop=2, click=True) 
    
    await ac.find(htmlE("/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[1]/div/h1", "xpath", ac, label="processing"), loop=0.2) 

    await ac.wait_to_go(htmlE("/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/ytcp-video-upload-progress/tp-yt-iron-icon[1]", "xpath", ac, label="arrow_up"))

    res = await ac.close_browser()



async def tiktok_task(title_hashs = ["#piano, #originalmusic"], channel_id= "", b_start_browser=True, edge_profile="Default", upload_file= test_file, track_title="Op. 42 - Cristian Kusch"):

    title_hashs = procHash(title_hashs, False)

    args = ["https://www.tiktok.com/upload?lang=en",f'--profile-directory={edge_profile}']
    
    if b_start_browser:  await start_browser(args)

    #await ac.wait_for_websocket(100)

    select_file = await ac.find([htmlE("""[aria-label="Select file"]""", "querySelector", ac), htmlE("""[aria-live="polite"]""", "querySelector", ac)], loop=2,timeout=80, timeout_exception="yt page didn't open", do_until=adel_(start_browser, [args], 30 ), click=1)
    
    await operate_file_popup( upload_file, select_file.clickCursor)

    caption = await ac.find(htmlE("""[aria-autocomplete="list"]""", "querySelector", ac), loop=2, do_until=adel_(pg.press, ["enter"], 2, True ), click=1)
    
    ab._workaround_write(track_title + " "  + title_hashs)

#    edit_video_btn = await ac.find(htmlE("/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div[3]/button", "xpath", ac, label="edit_video_btn"), loop=2,timeout=900, click=0)
    # uploaded_msg = await ac.find(htmlE("/html/body/div[1]/div/div/div/div[1]/div[1]/div[3]/div/span", "xpath", ac, label="uploaded_msg"), loop=2,timeout=900, click=0)

    for x in range(50):
        pg.scroll(-10)
        
    post_btn = await ac.find(htmlE("/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[7]/div[2]/button", "xpath", ac, label="post_btn"), loop=2, click=1)
    
    manage_posts = await ac.find(htmlE("/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[8]/div/div[2]/div[2]", "xpath", ac, label="manage_posts"), do_until=adel_(post_btn.clickCursor, [], 2, True ), loop=2, timeout=900)
        
    res = await ac.close_browser()


async def threads_task( title_hashs, channel_id, b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):


    args = ["https://www.threads.net/", f'--profile-directory={edge_profile}']
    
    if b_start_browser:   await start_browser(args)

    #await ac.wait_for_websocket(100)

    start_a_thread = await ac.find(htmlE("/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[1]", "xpath", ac, label="start_a_thread"), loop=2,timeout=80, timeout_exception="threads page didn't open", do_until=adel_(start_browser, [args], 30 ), click=1)
    
    attach_media = await ac.find(htmlE("""[aria-label="Attach media"]""", "querySelector", ac), loop=2, do_until=adel_(start_a_thread.clickCursor, [], 2, True ), click=0)
    
    await asyncio.sleep(0.2)
    ab._workaround_write("#")
    pg.write("piano")
    await asyncio.sleep(0.2)
    pg.press("enter")
    ab._workaround_write(track_title)
    
    #attach_media.clickCursor(15, -15)
    await operate_file_popup( upload_file, attach_media.clickCursor, [15, -15])
    
    for x in range(10):
        preview = await ac.find(htmlE("/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div", "xpath", ac, label="preview") )
        if preview.boundingBox["height"] > 40:
            break
        #pg.press("enter")
        logging.info(f"waiting for preview height > 40 ... {preview.boundingBox['height']}")
        await asyncio.sleep(1)
    
    post = await ac.find(htmlE("/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div", "xpath", ac, label="post"), loop=2)

    posting = await ac.find(htmlE("/html/body/div[4]/ul/li/div[1]/div/div[1]", "xpath", ac, label="posting"), loop=2, do_until=adel_(post.clickCursor, [], 2, True ))
    
    await ac.wait_to_go(posting, timeout=500)
    logging.info("THREADS_SUCCESS")


async def twitter_task(title_hashs = ["#piano, #originalmusic"], channel_id="", b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):

    title_hashs = procHash(title_hashs, False)
    
    args = ["https://twitter.com/compose/post", f'--profile-directory={edge_profile}']
    
    if b_start_browser:  await start_browser(args)

    #await ac.wait_for_websocket(100)

    attach_media = await ac.find(htmlE("""[aria-label="Add photos or video"]""", "querySelector", ac, label="attach_media"), loop=2,timeout=80, timeout_exception="twitter page didn't open", do_until=adel_(start_browser, [args], 30 ), click=0)
    
    what_is_happening = await ac.find(htmlE("""/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]""", "xpath", ac, label="what_is_happening"), loop=2,timeout=80, click=1)

    ab._workaround_write(track_title  + " " + title_hashs ); await asyncio.sleep(0.5)
    
    attach_media.clickCursor()
    
    await operate_file_popup(upload_file, attach_media.clickCursor)
    
    uploaded:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div[4]/div/div/div/div[1]/span", "xpath", ac, label="uploaded"), do_until=None, loop=2,timeout=300)
    
    for x in range(60):
        text = await uploaded.getField("innerHTML")
        if text and "Uploaded" in text:
            break
        logging.info("waiting for twitter upload")#piano #originalmusic Op. 42 - Cristian Kusch
        await asyncio.sleep(1)
    
    post = await ac.find(htmlE("/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/span/span", "xpath", ac, label="post"), loop=2, click=1)
    
    await ac.wait_to_go(post)
    logging.info("TWITTER_SUCCESS")
    #/div/div/div/div[1]/span "your post was sent"


async def facebook_task(title_hashs = ["#piano, #originalmusic"], channel_id="", b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):

    title_hashs = procHash(title_hashs, False)
    
    args = ["https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS", f'--profile-directory={edge_profile}']
    
    if b_start_browser:  await start_browser(args)

    #await ac.wait_for_websocket(100)

    add_video:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div", "xpath", ac, label="add_video"),  loop=2,timeout=80, timeout_exception="fb page didn't open", do_until=adel_(start_browser, [args], 30 ), click=1)
    
    await operate_file_popup(upload_file, add_video.clickCursor)

    await ac.wait_to_go(htmlE("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/form/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/span", "xpath", ac, label="your_video_preview"), do_while=None)

    next:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div", "xpath", ac, label="next"),  loop=2, click=1)

    next2:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div[2]/div[1]/div", "xpath", ac, label="next2"),  timeout=600, loop=2, click=1)
    
    describe:htmlE = await ac.find(htmlE("""[aria-label="Describe your reel..."]""", "querySelector", ac, label="describe"),  loop=2, click=1)
    
    ab._workaround_write(track_title  + " " + title_hashs )

    publish = None
    while 1:
        publish:htmlE = await ac.find(htmlE(next2.xpath, "xpath", ac, label="publish"),  loop=2, click=0 )
        rgb_string = publish.computed_style["backgroundColor"]
        red, green, blue = [int(x) for x in rgb_string[rgb_string.index("(")+1:rgb_string.index(")")].split(",")]
        if red < 200 and green < 200:
            logging.info(f"publish btn.. <200 <200 {(red, green, blue)}")
            await asyncio.sleep(5)
            break
        logging.info(f"waiting for publish btn.. {(red, green, blue)}")
        await asyncio.sleep(2)

    #/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div
    # /html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/span

    after_publish:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div[3]", "xpath", ac, label=f"after_publish"),  timeout=60, loop=2,do_until=adel_(publish.clickCursor, [], 5, True )) 
    
    last_elems = ["/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[1]/div[2]/a/object/a/div",
    "/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[1]/div[2]/a/span/div",   
    "/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[1]/div[2]/a/div"]
    
    last_elems += ["/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[3]/div[2]/div/div/div[2]", #last page
    "/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[4]",
    "/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[4]/div",
    "/html/body/div[1]/div/div[1]/div/div[7]",
    ]

    elems = [htmlE(e, "xpath", ac, label=f"last_elems{i}") for i, e in enumerate(last_elems)]

    notification:htmlE = await ac.find(elems,  timeout=600*2, loop=2) 
    
    logging.info("FB_SUCCESS")
    
    print()


async def tumblr_task(title_hashs = ["#piano, #originalmusic"], channel_id="", b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):
    
    #title_hashs =  title_hashs.replace("#", "").split(" ")
    title_hashs = procHash(title_hashs, False)
    
    args = ["https://www.tumblr.com/new/video", f'--profile-directory={edge_profile}']

    if b_start_browser:  await start_browser(args)
    
    put_anything:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div/div[4]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div[1]/p/span", "xpath", ac, label="put_anything"),  loop=2,timeout=80, timeout_exception="tumblr page didn't open", do_until=adel_(start_browser, [args], 30 ), click=1)
    asyncio.sleep(1.6)
    ab._workaround_write(track_title); await asyncio.sleep(0.6)
    
    tags_editor :htmlE = await ac.find(htmlE("""[aria-label="Tags editor"]""", "querySelector", ac),  loop=2, click=1)
    
    ab._workaround_write(title_hashs); await asyncio.sleep(0.4) #for hash in title_hashs: #pg.press("enter"); await asyncio.sleep(0.4)
       
    upload_video:htmlE = await ac.find(htmlE("""[aria-label="Upload a video"]""", "querySelector", ac),  loop=2, click=1)

    await operate_file_popup(upload_file, upload_video.clickCursor)
    
    loading:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div/div[4]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/div[2]", "xpath", ac, label="loading"),  loop=2,timeout=120,  do_until=None)#adel_(pg.press, ["enter"], 2, True )) 
    
    post_now:htmlE = await ac.find(htmlE("/html/body/div[1]/div/div/div[4]/div/div/div/div/div/div/div[2]/div/div[3]/div/div/div", "xpath", ac, label="post_now"),  loop=2)
    
    for x in range(50):
        pg.scroll(-10)

    publish = None
    while 1:
        publish:htmlE = await ac.find(htmlE(post_now.xpath, "xpath", ac, label="publish"),  loop=2, click=0 )
        rgb_string = publish.computed_style["backgroundColor"]
        if not "." in rgb_string:
            break
        print("waiting for publish btn..",rgb_string)
        await asyncio.sleep(2)
        
    await asyncio.sleep(1)

    publish:htmlE = await ac.find(htmlE(post_now.xpath, "xpath", ac, label="publish"),  loop=2, click=0 )
    publish.clickCursor(y_of=-40)


    #await ac.wait_to_go(loading, timeout=600, timeout_exception=True); await asyncio.sleep(1)
    
    logging.info("TUMBLR_SUCCESS")
    

async def soundcloud_task(title_hashs = ["#piano, #originalmusic"], b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch"):
    
    args = ["https://soundcloud.com/upload", f'--profile-directory={edge_profile}']
    
    if b_start_browser:  await start_browser(args)
    await ac.wait_for_websocket(100)
    raise Exception("test exception")
    await asyncio.sleep(2)
    # choose_file:htmlE = await ac.find(htmlE("/html/body/div[1]/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div/div[1]/div/button", "xpath", ac, label="choose_file"),  loop=2,timeout=80, timeout_exception="soundcloud page didn't open", do_until=adel_(start_browser, [args], 30 ), click=1)
    #ac.server_task.cancel("-END-")
    print()

async def monitor_task():
    import win32api

    def find_elements_not_in_first(first_array, second_array):
        first_xpaths = {element.xpath for element in first_array}
        return [element for element in second_array if element.xpath not in first_xpaths]
    cur = []
    prev = []

    await ac.wait_for_websocket(100)
    while 1:
        if win32api.GetAsyncKeyState(70)== -32767: #f
            prev = cur
            cur = await ac.querySelectorAll('div')
            print(len(cur))
            if len(prev) and len(cur):
                elems = find_elements_not_in_first(prev, cur)
                print("-->", len(elems))
                print("-------------------------\n")
                list_ = []
                for elem in elems:
                    list_.append(f" {elem.xpath}, {await elem.getBoundingBox()}")
                for elem in list_:
                    print(elem)

        await asyncio.sleep(0.2)
            #return True
#https://www.reddit.com/r/Songwriting/comments/1bo43ow/weekly_self_promotion_thread/f



class taskPayload():
    def __init__(self, title_hashs = ["#piano", "#originalmusic"], channel_id:str=test_yt_id, b_start_browser=True,  upload_file= test_file, edge_profile="Default", track_title="Op. 42 - Cristian Kusch", hashtag_map = None) -> None:
        self.title_hashs = title_hashs
        self.channel_id=channel_id
        self.b_start_browser=b_start_browser
        self.upload_file = upload_file
        self.edge_profile=edge_profile
        self.track_title=track_title
        #self.hashtag_map = hashtag_map
        
    def __str__(self) -> str:
        return " ".join([f'{key}: {value}' for key, value in vars(self).items() if not key.startswith('__')])
    def __repr__(self) -> str:
        return " ".join([f'{key}: {value}' for key, value in vars(self).items() if not key.startswith('__')])
    
async def terminate_all():    
    logging.info(f"----> terminating all..." )
    logging.info(f"----> perform_task: closing browser..." )
    await ac.close_browser()
    await asyncio.sleep(0.5)
    logging.info(f"----> perform_task: canceling ac.server_task ..." )
    ac.server_task.cancel("-END-")

def get_short_id():
    unique_id = str(uuid.uuid4())
    hashed_id = hashlib.md5(unique_id.encode()).hexdigest()
    short_id = hashed_id[:8]
    return short_id
    
async def perform_task(pl, task):
    
    try:
        if pl:
            await task(title_hashs=pl.title_hashs, channel_id=pl.channel_id, b_start_browser=pl.b_start_browser, upload_file=pl.upload_file, edge_profile=pl.edge_profile, track_title=pl.track_title)
        else:
            await task()
    except Exception as e:
        logging.info(f"----> perform_task: Function {task.__name__} exception: {e} , traceback:\n {traceback.format_exc()}")  
        await terminate_all()
        return { "id": get_short_id(),  "exception": e, "traceback": traceback.format_exc()}   
            
    logging.info(f"----> perform_task: Function {task.__name__} has returned" )

    await terminate_all()
    pass

async def check_timeout(timeout):
    global trigger_timeout
    trigger_timeout = True
    await asyncio.sleep(timeout)
    if trigger_timeout:
        logging.info(f"-----> timeout reached: {timeout}")
        await terminate_all()
        logging.info(f"-----> timeout NOT reached: {timeout}")

#all_tasks = [youtube_task, tiktok_task, instagram_task, threads_task, twitter_task, facebook_task,  tumblr_task]#, soundcloud_task]

all_tasks = {
  "youtube": youtube_task,
  "tiktok": tiktok_task,
  "instagram": instagram_task,
  "threads": threads_task,
  "twitter": twitter_task,
  "facebook": facebook_task,
  "tumblr": tumblr_task
}

def is_async_function(func):
    return inspect.iscoroutinefunction(func)

import utils.cloud_utils.mongo_schema as mongo_schema

def perform_upload_tasks(payload:taskPayload, tasks = all_tasks.values(), mongo_context=None, arduino=None):

    t1 = time.time()
    
    ac.ard_click = arduino
    
    logging.info(f"-------> task payload: {payload} " )

    mongo = mongo_context["client"] if mongo_context else None

    for task  in tasks:
        if type(task) == str: payload.title_hashs = hashtag_map[task]   
        task_fun =  all_tasks[task] if type(task) == str else task
        
        for attempt_n in range(3):

            upload_attempt_pl, new_entry_id = create_attempt_entry(mongo_context,  task)

            logging.info(f"----> starting task {task_fun.__name__} | attempt: {attempt_n} " )
            if is_async_function(task_fun):
                ret =  ac.start([lambda: perform_task(payload, task_fun)])#, lambda: check_timeout(1500)
                if ret: 
                    logging.info(f"""Post execution error log during async task  {task_fun.__name__}, id: {ret["id"]}, exception: "{ret["exception"]}", traceback:\n {ret["traceback"]}""")
                    if mongo_context:
                        update_with_error(mongo_context, upload_attempt_pl, str(new_entry_id.inserted_id), ret["traceback"])
                    time.sleep(1)
                else:
                    if mongo_context:
                        update_with_error(mongo_context, upload_attempt_pl, str(new_entry_id.inserted_id), "")
                    break
            else:
                try:
                    pl = payload
                    task_fun(title_hashs=pl.title_hashs, channel_id=pl.channel_id, b_start_browser=pl.b_start_browser, upload_file=pl.upload_file, edge_profile=pl.edge_profile, track_title=pl.track_title)
                    if mongo_context:
                        update_with_error(mongo_context, upload_attempt_pl, str(new_entry_id.inserted_id), "")
                    break
                except Exception as e:
                    logging.info(f"Error during sync task  {task_fun.__name__} ,  exception: {e},  traceback:\n {traceback.format_exc()}")
                    if mongo_context:
                        update_with_error(mongo_context, upload_attempt_pl, str(new_entry_id.inserted_id), str(traceback.format_exc()))
                    time.sleep(1)
            

def update_with_error(mongo_context, upload_attempt_pl, new_entry_id, error):
    mongo =  mongo_context["client"]
    upload_attempt_pl["error"] = error
    update_result = mongo.update_entry({"_id": ObjectId(new_entry_id)}, upload_attempt_pl, "upload_attempts", mongo.schemas["upload_attempts"])
    logging.info(f"Update operation for upload attempt with error { update_result.modified_count if update_result else 'Nothing updated'} {  'op id:' + str(uuid.uuid1())  }")

def create_attempt_entry(mongo_context, task):
    upload_attempt= None
    new_entry_id= None
    if mongo_context:
        mongo =  mongo_context["client"]
        upload_attempt =  mongo_schema.uploadAttempt.create(mongo_context["track_id"], str(mongo_context["session_id"]), task, datetime.datetime.now(datetime.timezone.utc).isoformat(), "task didn't reach end of function" )
        new_entry_id = mongo.create_entry(upload_attempt, "upload_attempts", mongo.schemas["upload_attempts"])
        logging.info(f"Created upload attempt entry with id: {new_entry_id.inserted_id} " )
    return upload_attempt,new_entry_id


if __name__ == "__main__":

    task_payload = taskPayload()
    #instagram_task()

    #ac.start([lambda: perform_task(task_payload, facebook_task)])
 
    # import subprocess
    # ld  = subprocess.Popen(os.getenv("LD_BIN"))
    #ac.start([lambda: monitor_task()])
    arduino = arduino_helper.arduinoHelper(True, "COM7")
    task_payload.channel_id = "UCdeGgQuczwgU8H-GaMrdLzw"
    arduino.ar.init()
    arduino.set_board_mode(arduino.boardModeEnum.mouseKeyboard.value)
    arduino.ar.change_delay_between(250) #250ms for click
    #ac.set_ard_click(arduino) 
    perform_upload_tasks(task_payload, [instagram_task2],  arduino=arduino)
    #perform_upload_tasks(task_payload,all_tasks.values())


    time.sleep(2)
    print("script exited")