import os
import gzip
import shutil
import datetime
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler

# current_date = datetime.date.today()

# # set the file paths
# # TODO: make the path always route to this file no matter where it is called from
# # absolute_path_to_logs = os.path.abspath("src/logs")
# # file_path = os.path.abspath("src/logs/debug.log")
# # new_file_path = os.path.join("src/past_logs", str(current_date) + ".gz")
# # print(absolute_path_to_logs)
# # print(file_path)

# MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
# print(MODULE_PATH)

# absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")
# file_path = os.path.join(absolute_path_to_logs, "debug.log")
# new_file_path = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")
# # print("absolute_path_to_logs: ", absolute_path_to_logs)


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

# compress_old_logs()



# Get the current date to use in the compressed log file name.
current_date = datetime.date.today()

# logging.basicConfig(filename='scheduler.log')
# schedule_logger = logging.getLogger('schedule')
# schedule_logger.setLevel(level=logging.DEBUG)


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        # log_file = self.baseFilename

        log_file = self.baseFilename
        if os.path.exists(log_file):
            with open(log_file, 'rb') as f_in:
                with gzip.open(log_file + '.gz', 'wb') as f_out:
                    f_out.writelines(f_in)
            os.remove(log_file)


        # if os.path.exists(file_path):
        #     with open(file_path, 'rb') as f_in, gzip.open(log_file_name, "wb") as f_out:
        #         print(f_in)
        #         print('arrived')
        #         shutil.copyfileobj(f_in, f_out)

        #     # Clear all the files in src/logs log file after compression
        #     for file in os.listdir(absolute_path_to_logs):
        #         logs_file_path = os.path.join(absolute_path_to_logs, file)
        #         if not os.path.exists(logs_file_path):
        #             open(file, 'w').close()
        #             print(f"File added: {logs_file_path}")
        #         open(logs_file_path, 'r+').truncate(0)


logging.basicConfig(filename='scheduler.log')
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)

# get path to local file
MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")
file_path = os.path.join(absolute_path_to_logs, "debug.log")
log_file_name = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")


# handler = GzipTimedRotatingFileHandler(log_file_name, when='S', interval=5, backupCount=5)
handler = GzipTimedRotatingFileHandler(file_path, when='m', interval=1)
# handler = GzipTimedRotatingFileHandler(log_file_name, when='midnight')

# while True:
#   logging.error('other error message')
