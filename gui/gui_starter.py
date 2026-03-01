import subprocess
import os
import signal
import sys
import psutil

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    return process

def kill_child_processes(parent_pid):
    parent = psutil.Process(parent_pid)
    children = parent.children(recursive=True)
    
    for child in children:
        try:
            child.terminate()
        except psutil.NoSuchProcess:
            pass
    
    # Wait for all child processes to finish
    gone, alive = psutil.wait_procs(children, timeout=3)

def main():
    # Command to run
    os.chdir("F:\\all\\GitHub\\aws-python\\gui\\eel\\")
    print(os.getcwd())
    command = "npm-run-all -p start:*"
    # command = 'cd F:\\all\\GitHub\\aws-python\\gui\\eel\\ && npm-run-all -p start:*'
    parent_process = run_command(command)
    
    try:
        # Wait for the process to finish or for a keyboard interrupt
        parent_process.wait()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    finally:
        # Ensure all child processes are terminated when the script ends
        kill_child_processes(os.getpid())
        sys.exit(0)

if __name__ == "__main__":
    main()