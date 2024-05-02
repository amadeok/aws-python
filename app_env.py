from dotenv import dotenv_values, load_dotenv
import os
load_dotenv()
ld_shared_folder =   os.getenv("LD_SHARED_FOLDER")
audio_folder =  os.getenv("AUDIO_FOLDER")
output_folder =  os.getenv("OUTPUT_FOLDER")
