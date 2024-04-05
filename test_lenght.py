import app_env

l = [f"{app_env.ld_shared_folder}\\output\\ohio0_00024v2_s",
f"{app_env.ld_shared_folder}\\output\\tok0_00024v2_s",
f"{app_env.ld_shared_folder}\\output\\SA0_00024v2_s",
f"{app_env.ld_shared_folder}\\output\\osa1_00024v2_s",
f"{app_env.ld_shared_folder}\\output\\lond1_00024v2_s"]

import math
import textwrap
import ass, datetime

lyr_file = r"C:\Users\amade\Documents\dawd\Exported\00034\Mixdown\s_00034(5).ass"

start = datetime.timedelta(minutes=0, seconds=15, milliseconds=810)

with open(lyr_file, encoding='utf_8_sig') as f:
    doc = ass.parse(f)
    for e in doc.events:
        r_start = e.start - start
        print(r_start)
        print(r_start.total_seconds())
    print(doc)


lyrics_text = [["it's true i did with forgot us all with another ti and then another line", 0], ["it's true i did see you fall", 100]]


max_chars_per_line = 31# it's true i forgot about us all


wrapper = textwrap.TextWrapper(width=max_chars_per_line)

for line in lyrics_text:
    line_ = line[0]
    size = len(line_)
    lines_n = size / max_chars_per_line

    line[0] =  wrapper.wrap(text=line[0])
    l2 = "\n".join(line[0])
    print(line[0]) 
    for ll in line[0]:
        print(len(ll))


exit()


print(new_string)    # Output: "hello-world"
for p in l:
    with open (p +  "\\lenght.txt", "r")as fff:
        data = fff.read()
        print(data)