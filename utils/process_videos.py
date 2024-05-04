import cv2
import os, ffmpeg
from moviepy.editor import VideoFileClip
import os
import shutil

def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_all_video_durations(folder_path):
    video_durations = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                duration = get_video_duration(file_path)
                if duration is not None:
                    video_durations[file] = duration
                    print(file, video_durations[file])
    return video_durations
  
    
def get_video_info_ffmpeg(file_path):
    probe = ffmpeg.probe(file_path)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    duration = float(video_info['duration'])
    width = int(video_info['width'])
    height = int(video_info['height'])
    frame_rate = eval(video_info['avg_frame_rate'])
    return duration, width, height, frame_rate

def get_video_info_cv(file_path):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Error: Couldn't open the video file")
        return None

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.release()
    return duration, width, height, fps

def get_video_duration_ffmpeg(file_path, stream_type="video"):
    try:
        probe = ffmpeg.probe(os.path.normpath(file_path))
        l =[ stream for stream in probe['streams'] if stream['codec_type'] == stream_type]
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == stream_type)
        duration = float(video_info['duration'])
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_all_video_durations_ffmpeg(folder_path):
    video_durations = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                duration = get_video_duration_ffmpeg(file_path)
                if duration is not None:
                    video_durations[file] = duration
    return video_durations



# if os.path.exists(folder_path):
#     video_durations = get_all_video_durations_ffmpeg(folder_path)
#     for video, duration in video_durations.items():
#         print(f"Video: {video} - Duration: {duration} seconds")
# else:
#     print(f"The folder {folder_path} does not exist.")
    
    


def get_video_orientation(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream:
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            return 'vertical' if height > width else 'horizontal'
        else:
            return None
    except ffmpeg.Error:
        return None

def move_videos_by_orientation(source_folder, vertical_folder, horizontal_folder):
    if not os.path.isdir(vertical_folder): os.makedirs(vertical_folder)
    if not os.path.isdir(horizontal_folder): os.makedirs(horizontal_folder)
    for filename in os.listdir(source_folder):
        if filename.endswith(".mp4") or filename.endswith(".avi"):  # Adjust for other video formats if needed
            video_path = os.path.join(source_folder, filename)
            orientation = get_video_orientation(video_path)
            if orientation == 'vertical':
                shutil.move(video_path, os.path.join(vertical_folder, filename))
                print(f"Moved {filename} to {vertical_folder}")
            elif orientation == 'horizontal':
                shutil.move(video_path, os.path.join(horizontal_folder, filename))
                print(f"Moved {filename} to {horizontal_folder}")
            else:
                print(f"Skipping {filename}: Unable to determine orientation")

  
    
    
    
    
def check_empty_folders(directory):
    empty_folders = []
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            folder_path = os.path.join(root, d)
            if not os.listdir(folder_path):
                empty_folders.append(folder_path)
    return empty_folders

# empty_folders = check_empty_folders(folder_path)
# for folder in empty_folders:
#     print(folder)


def group_files_by_name(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Create a dictionary to store file names and corresponding lists of file paths
    file_groups = {}
    
    # Group files by name
    for file in files:
        file_name = os.path.splitext(file)[0]  # Extract file name without extension
        file_name2 = file_name.split("__")
        file_name3 = file_name2[1] if len(file_name2) > 1 else file_name2[0]
        file_name4 = file_name3.split("-")[0]
        file_name4 = file_name4.replace("_small", "")
        if file_name4 not in file_groups:
            file_groups[file_name4] = []
        file_groups[file_name4].append(os.path.join(folder_path, file))
    
    # Create folders and move files
    for file_name, file_paths in file_groups.items():
        if len(file_paths) > 1:  # Only move if there are multiple files with the same name
            # Create a folder for this group
            group_folder = os.path.join(folder_path, file_name)
            os.makedirs(group_folder, exist_ok=True)
            
            # Move files into the group folder
            for file_path in file_paths:
                shutil.move(file_path, group_folder)


# group_files_by_name(vertical_folder)
# group_files_by_name(horizontal_folder)


def find_files_with_suffix(directory, suffix, invert):
    small_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if root == directory:
                small_files.append(os.path.join(root, file))

        for dir in dirs:
            subdir = os.path.join(root, dir)
            for subroot, _, subfiles in os.walk(subdir):
                for subfile in subfiles:
                    i = int(suffix in subfile.lower())
                    if invert:   i = invert-(i)
                    if i:
                        small_files.append(os.path.join(subroot, subfile))

    return small_files

# small_files = find_files_with_suffix(vertical_folder, "small", 0)
# for file_path in small_files:
#     print(file_path)
    
if __name__ == "__main__":
    folder_path = r"C:\Users\amade\Videos\social_media_videos"

    source_folder = folder_path
    vertical_folder = os.path.join(folder_path, "vertical")
    horizontal_folder = os.path.join(folder_path, "horizontal") 

    #move_videos_by_orientation(source_folder, vertical_folder, horizontal_folder)

    files = find_files_with_suffix(horizontal_folder, "small", 1)

        
    horizontal_folder_processed = os.path.join(horizontal_folder, "processed")
    if not os.path.isdir(horizontal_folder_processed): os.makedirs(horizontal_folder_processed)

    for file_path in files:
        cmd = f"""ffmpeg -i {file_path} -vf "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" {os.path.join(horizontal_folder_processed, os.path.basename(file_path))} -y"""
        cmd = f"""ffmpeg -i {file_path} -filter:v "crop=ih*(9/16):ih" {os.path.join(horizontal_folder_processed, os.path.basename(file_path))} -y"""

        os.system(cmd)
        print(file_path)