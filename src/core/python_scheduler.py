import schedule
import time
import logging
import datetime
import os
import gzip
import shutil
import pathlib

current_date = datetime.date.today()

logging.basicConfig(filename='scheduler.log')
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)

# # find the different file paths
MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")
file_path = os.path.join(absolute_path_to_logs, "debug.log")
new_file_path = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")

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

# schedule.every(1).minutes.do(compress_old_logs)
schedule.every().day.at("00:0").do(compress_old_logs)

while True:
    schedule.run_pending()
    time.sleep(1)
