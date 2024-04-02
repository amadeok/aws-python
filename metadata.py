import random
import subprocess
import os
from random_word import RandomWords

r = RandomWords()

target_f = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\osa1_00024v2_s\00024v2_s_joined.mp4"
cmd = f"""exiftool\exiftool.exe -Encoder="ave3e"  Graphics Mode {target_f}  -overwrite_original"""

#fields = ["ExifToolVersionNumber","MIME Type","GraphicsMode","MediaLanguageCode","MajorBrand","HandlerDescription","OtherFormat","HandlerType","HandlerVendorID","Encoder"]
fields = ["MIME Type", "Encoder"]

def format(f):
    ran = r.get_random_word()
    return f'-"{f}"={ran}'

def randomize_metadata(file):
    cmd_l = ["exiftool\exiftool.exe"]
    for f in fields:
        cmd_l.append(format(f))
    
    if random.randint(0, 1):
        cmd_l.append(format("Artist"))
    cmd_l.append(file)
    cmd_l.append("-overwrite_original")
    #    l = ["exiftool", format(f),  file ]#"-overwrite_original"]
    str_ = " ".join(cmd_l)
    print(f"\n {f} {str_}")
    os.system(str_)
    

#randomize_metadata(target_f)
    
if __name__ == "__main__":
    randomize_metadata(r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\rom0!_00033v2_s\00033v2_s_dav.mp4")
    print("main")