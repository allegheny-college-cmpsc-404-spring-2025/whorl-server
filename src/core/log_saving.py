import os
import logging
import gzip
import shutil
from logging.handlers import TimedRotatingFileHandler

# # Create 'past_logs' folder if it doesn't exist
# LOG_DIR = "logs"
# PAST_LOGS_DIR = os.path.join(LOG_DIR, "past_logs")
# os.makedirs(PAST_LOGS_DIR, exist_ok=True)

# Log file path
# LOG_FILE = os.path.join(LOG_DIR, "../logs")

# Configure logger
# logger = logging.getLogger("MyLogger")
# logger.setLevel(logging.INFO)

# print(os.listdir('src/logs'))

# # Create a TimedRotatingFileHandler that rotates logs every midnight
# handler = TimedRotatingFileHandler(
#     "src/logs/debug.log", when="midnight", interval=1, backupCount=7, encoding="utf-8"
# )
# handler.suffix = "%Y-%m-%d"  # Adds a date suffix to rotated logs
# print(handler.suffix)

# # Define log format
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)

# Add handler to logger
# logger.addHandler(handler)

def compress_old_logs():
    """
    Moves and compresses rotated log files into 'past_logs' directory.
    """
    for filename in os.listdir('src/logs'):
        # if filename.endswith(".log") and not filename.endswith(".gz"):
        old_log_path = os.path.join('src/logs/', filename)
        print("old log path: ", old_log_path)
        # compressed_log_path = os.path.join(PAST_LOGS_DIR, filename + ".gz")
        compressed_log_path = os.path.join("src/past_logs/", filename + ".gz")
        print("compressed log branch: ", compressed_log_path)

        # Compress log file
        with open(old_log_path, "rb") as f_in, gzip.open(compressed_log_path, "wb") as f_out:
            print("this works")
            shutil.copyfileobj(f_in, f_out)

    # Remove uncompressed log file after compression
    os.remove(old_log_path)
    print(f"Compressed and moved: {filename}")

compress_old_logs()
# compress_old_logs('success.log')
# compress_old_logs('error.log')

# Schedule compression to run every midnight
# if __name__ == "__main__":
#     # logger.info("Application started. Logging initialized.")

#     import threading
#     import time

#     def schedule_compression():
#         while True:
#             # now = time.localtime()
#             # midnight = time.mktime((now.tm_year, now.tm_mon, now.tm_mday))
#             # midnight = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 23, 59, 59, 0, 0, -1))
#             # sleep_time = midnight - time.time() + 1  # Ensure it runs just after midnight
#             # time.sleep(max(0, sleep_time))
#             compress_old_logs('debug.log')
#             compress_old_logs('success.log')
#             compress_old_logs('error.log')

#     # Start compression in a background thread
#     compression_thread = threading.Thread(target=schedule_compression, daemon=True)
#     compression_thread.start()

    # Simulating log generation
    # while True:
    #     # logger.info("Logging some activity...")
    #     time.sleep(10)  # Adjust as needed
