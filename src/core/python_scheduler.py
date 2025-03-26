import schedule
import time
import logging
import datetime
import os
import gzip
import shutil
import pathlib
from logging.handlers import TimedRotatingFileHandler


current_date = datetime.date.today()

logging.basicConfig(filename='scheduler.log')
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)



# # find the different file paths
# MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
# absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")
# file_path = os.path.join(absolute_path_to_logs, "debug.log")
# new_file_path = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")

# def compress_old_logs():
#     """
#     Moves and compresses rotated log files into 'past_logs' directory."
#     """
#     # Compress log file
#     with open(file_path, "rb") as f_in, gzip.open(new_file_path, "wb") as f_out:
#         print("this works")
#         shutil.copyfileobj(f_in, f_out)

#     # Clear all the files in src/logs log file after compression
#     for file in os.listdir(absolute_path_to_logs):
#         logs_file_path = os.path.join(absolute_path_to_logs, file)
#         if not os.path.exists(logs_file_path):
#             open(file, 'w').close()
#             print(f"File added: {logs_file_path}")
#         open(logs_file_path, 'r+').truncate(0)

#     print(f"Compressed and moved: {new_file_path}")

# def job():
#     print("Executing the scheduled job")
#     # Add your task logic here
#     # return "Job completed"
#     compress_old_logs()

# schedule.every(1).minutes.do(job)
# # schedule.every().day.at("00:00").do(my_job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        log_file = self.baseFilename
        if os.path.exists(log_file):
            with open(log_file, 'rb') as f_in, gzip.open(log_file_name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

            # Clear all the files in src/logs log file after compression
            for file in os.listdir(absolute_path_to_logs):
                logs_file_path = os.path.join(absolute_path_to_logs, file)
                if not os.path.exists(logs_file_path):
                    open(file, 'w').close()
                    print(f"File added: {logs_file_path}")
                open(logs_file_path, 'r+').truncate(0)


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")
file_path = os.path.join(absolute_path_to_logs, "debug.log")
log_file_name = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")

# handler = GzipTimedRotatingFileHandler(log_file_name, when='S', interval=5, backupCount=5)
handler = GzipTimedRotatingFileHandler(log_file_name, when='M', interval=1)

# Set the log message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
