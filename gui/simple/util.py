import os, logging#, flask
def get_it_path(op_number, iteration, abort_func=lambda s: print(s)):

    folder = os.getenv("PLAY_WAV_FOLDER")
    op_dir = f"{op_number:05d}" 
    highest_it= None
    if iteration == -1:
        highest_it = 1
        for x in range(1, 10):
            folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{x}")
            if os.path.isdir(folder_path) and os.listdir(folder_path).__len__()  > 0:
                highest_it = x
        logging.info(f"Highest iteration for for op. {op_number}: {highest_it}")
        folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{highest_it}")
        
    elif iteration:            
        if op_number is None or iteration is None:   abort_func("Missing required parameters: 'op' and 'it'")
        folder_path = os.path.join(folder, op_dir, 'Mixdown', f"it{iteration}")
    else:
        if op_number is None:  abort_func("Missing required parameters: 'op'")
        folder_path = os.path.join(folder, op_dir)
        
    return folder_path, highest_it or iteration