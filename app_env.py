from dotenv import dotenv_values
config = dotenv_values(".env")
ld_shared_folder =  config["LD_SHARED_FOLDER"]
audio_folder = config["AUDIO_FOLDER"]
output_folder = config["OUTPUT_FOLDER"]