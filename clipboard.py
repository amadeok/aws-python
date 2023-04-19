import subprocess, time

def getClipboardData():
    p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data.decode("utf-8")

if __name__ == "__main__":
    time.sleep(2)
    data =getClipboardData() 
    print(data)