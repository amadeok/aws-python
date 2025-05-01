import subprocess, subprocessHelper, os, socket,browserStarter

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 0))  # 0 means select a free port
        s.listen(1)
        port = s.getsockname()[1]
    return port

if __name__ == "__main__":
    manager = browserStarter.BrowserManager()

    os.chdir(r"F:\all\GitHub\aws-python\gui\simple")
    port =   get_free_port()
    os.environ["WAITRESS_PORT"] =str(port) 
    os.environ["WAITRESS_DEBUG"] = "0"
    cmd = ["py", "-3.10", "-m", "waitress",  f"--port={port}", "simple_gui:app", ]
    print(" ".join(cmd))
    #cmd = ["py", "-3.10", "simple_gui.py", "--port", "8123", "&", "waitress-serve", "--call", "simple_gui:app"]
    p = subprocess.Popen(cmd)
    manager.start_chromium( f'http://localhost:{port}', False)    
    p.wait()
    
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
    #     print(f"Error running command: {e}")