import os
import gzip
import shutil
# import logging
# from logging.handlers import TimedRotatingFileHandler
import datetime

current_date = datetime.date.today()

# set the file paths
# TODO: make the path always route to this file no matter where it is called from
absolute_path_to_logs = os.path.abspath("src/logs")
file_path = os.path.abspath("src/logs/debug.log")
new_file_path = os.path.join("src/past_logs", str(current_date) + ".gz")
# print(absolute_path_to_logs)
# print(file_path)

def compress_old_logs():
    """
    Moves and compresses rotated log files into 'past_logs' directory."
    """
    # Compress log file
    with open(file_path, "rb") as f_in, gzip.open(new_file_path, "wb") as f_out:
        print("this works")
        shutil.copyfileobj(f_in, f_out)

    # Clear all the files in src/logs log file after compression
    for file in os.listdir(absolute_path_to_logs):
        logs_file_path = os.path.join(absolute_path_to_logs, file)
        if not os.path.exists(logs_file_path):
            open(file, 'w').close()
            print(f"File added: {logs_file_path}")
        open(logs_file_path, 'r+').truncate(0)

    print(f"Compressed and moved: {new_file_path}")

compress_old_logs()