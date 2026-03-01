import eel_utils, sys, os
from pydub import AudioSegment

def get_audio_length(file_path):
    if not file_path: return None
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0  # Convert milliseconds to seconds

def seconds_to_minutes_seconds(seconds):
    if not seconds: return ""
    minutes = int(seconds // 60)  # Get the whole number of minutes
    remaining_seconds = int(seconds % 60)  # Get the remaining seconds
    return f"{minutes}m {remaining_seconds}s"


if __name__ == "__main__":
    path = os.path.expandvars( r"C:\Users\%username%\Documents\Studio One\Songs\newstart")
    paths = os.listdir(path)
    autio_lengths = []
    for p in paths:
        full_p = os.path.join(path, p, "Mixdown")
        file = eel_utils.get_most_recent_audio_file_with_string(full_p)
        length = get_audio_length(file)
        if file and length:
            autio_lengths.append([file, length])

    obj = { "<1m": [], "<1m30s": [], "<2m": [], ">2m": []}
    
    for elem in autio_lengths:
        file, length = elem
        asters = ''
        if length:
            if length < 60*1.0:
                asters = "* * *"
                obj["<1m"] += [os.path.basename(file)]
            elif length < 60*1.5:
                asters = "* *"
                obj["<1m30s"] += [os.path.basename(file)]
            elif length < 60*2:
                asters = "* "
                obj["<2m"] += [os.path.basename(file)]
            else:
                obj[">2m"] += [os.path.basename(file)]

        print((f"{os.path.basename(file):20}" if file else "")  + f" {seconds_to_minutes_seconds(length):7} {asters}")

tot = 0
for k, v in obj.items():
    print(k, len(v))
    tot+=len(v)
assert tot == len(autio_lengths)

l1 = obj["<2m"]
l2 = obj["<1m30s"]
for elem in l1:
    assert not elem in l2
for elem in l2:
    assert not elem in l1
print()