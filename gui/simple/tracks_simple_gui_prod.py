import logging, os
import time
import loggingHelper,win32gui,win32con
loggingHelper.Logger("track_monitor", level=logging.INFO,ignore_strings=["GET /health"])
import subprocess, socket,browserStarter, settingsManager, PyInterProcCom
import loge
from loge.check_task import checkTask

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 0))  # 0 means select a free port
        s.listen(1)
        port = s.getsockname()[1]
    return port


def start_or_focus(h =None):
    global manager
    if manager.hwnd:
        h = h._hWnd if h else manager.hwnd._hWnd
    win_valid = (h and win32gui.IsWindowVisible(h) and win32gui.IsWindowEnabled(h))
    if not win_valid:
        logging.info("Win not valid, starting new browser")
        start_browser()
    else:
        try:
            logging.info(f"Setting foreground win  {win_valid}")
            win32gui.SetForegroundWindow(h)
            win32gui.ShowWindow(h, win32con.SW_RESTORE)
        except Exception as e:
            logging.error(f"Error set fore {e}" )
            return {"success": False, "error": e, "timestamp": time.time()}
            

pipe_name =  r"\\.\pipe\browser_control_pipe"
lo = loge.loge.loge()

def main():
    url = None
    app_name = "Track monitor"
    pipe_server = PyInterProcCom.NamedPipeServer(pipe_name)

    def handle_json_data(data: dict) -> dict:
        logging.info(f"Received JSON: {data}")
        if data["operation"] == "get_browser_handle":
            # ret = start_or_focus(manager.hwnd)
            start_browser()
            return {"success": True,  "timestamp": time.time()}
        else:
            return {"success": False, "error": "no operation", "timestamp": time.time()}
    pipe_server.start(handle_json_data)

    
    parser = settingsManager.ArgParser(("br_sync", int, 1), ("cl_cl_disc", int, 0), ("new_win", int, 0))#,("debug", bool, False))

    os.chdir(r"F:\all\GitHub\aws-python\gui\simple")
    port =   get_free_port()
    br_sync_port = get_free_port()
    os.environ["PROD_PORT"] =str(port) 
    os.environ["BROWSER_SYNC_PORT"] =str(br_sync_port) 
    os.environ["PROD_DEBUG"] = "0"
    os.environ["USE_BROWSER_SYNC"] = str(parser.get("br_sync")) 
    os.environ["CLOSE_ON_CLIENT_DISCONNECT"] = str(parser.get("cl_cl_disc")) 
    
    cmd = ["py", "-3.10", "-m", "waitress",  f"--port={port}", "simple_gui:app", ]
    logging.info(" ".join(cmd))
    #cmd = ["py", "-3.10", "simple_gui.py", "--port", "8123", "&", "waitress-serve", "--call", "simple_gui:app"]
    p = subprocess.Popen(cmd)
    url = f'http://localhost:{br_sync_port if parser.get("br_sync") else port}'
    manager = browserStarter.AsyncPlaywrightWrapper(browser_type="chromium", headless=False, url_to_wait=url)

    def start_browser():
        logging.info("Starting browser");
        page = manager.get_tab_by_url(url, app_name)
        if page and not manager.is_page_closed(page):
            manager.focus_page(page)
        else:
            manager.open_url_sync(url , new_tab= not parser.get("new_win"), window_label=app_name, block=1)    
    
    lo.start_lisenting(checkTask(start_browser, lo.v["B"], [], False))
    start_browser()
    # manager.open_url_sync("google.com" , new_tab=True, window_label=app_name, block=False)    

    p.wait()
   

if __name__ == "__main__":

    ret = PyInterProcCom.send_json_to_pipe(pipe_name, {"operation":"get_browser_handle"})
    try:
        if ret == 2: #pipe not found
            main()
        else:
            if not "error" in ret:
                logging.info(f"""---------hwnd, {ret["hwnd"]}""")
            else:
                logging.error(f"""Error: {ret["error"]}""")
    except KeyboardInterrupt as e:
        print("Keyboard interrupt")
    finally:
        lo.stop_listening()

    # import sys

    # # Define your arguments
    # script_args = ["--port", "8123"]

    # python_dir = os.path.dirname(sys.executable)  # Gets Python install directory
    # scripts_dir = os.path.join(python_dir, "Scripts")

    # # Path to your .exe (e.g., pip.exe, black.exe, etc.)
    # exe_path = os.path.join(scripts_dir, "waitress-serve.exe")

    # waitress_cmd = [
    #     exe_path,
    #     #"py", "-3.10", "-m", "waitress",
    #     #"waitress-serve",
    #     "--call",
    #     "simple_gui:app"
    # ]

    # # Run the commands
    # try:
    #     # If your app.py needs to run first to process arguments
    #     subprocess.run([sys.executable, "simple_gui.py"] + script_args, check=True)
        
    #     # Then start waitress
    #     subprocess.run(waitress_cmd, check=True)
    # except subprocess.CalledProcessError as e:
    #     logging.info(f"Error running command: {e}")