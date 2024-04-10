import subprocess as  sp
import os
os.chdir(r"F:\all\GitHub\aws-python\gui\eel\\")
print(os.listdir("."))
p1 = sp.Popen([r"F:\all\GitHub\aws-python\gui\eel\dist\react-eel-app.exe"])

os.system("serve -s build")
p1.wait()
#p1 = sp.Popen(["serve", "-s", "build"])
#p1.wait()