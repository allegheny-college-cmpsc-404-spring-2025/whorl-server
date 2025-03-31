import schedule
import time
import logging
import datetime
import os
import gzip
import shutil
import pathlib

# Get the current date
current_date = datetime.date.today()

# Configure logging for the scheduler
logging.basicConfig(filename='scheduler.log')
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)

# Define paths for logs and compressed files
MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")
file_path = os.path.join(absolute_path_to_logs, "debug.log")
new_file_path = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")

def compress_old_logs():
    """
    Compresses and moves the rotated log file to the 'past_logs' directory.

    This function performs the following steps:
    1. Compresses the `debug.log` file from the `logs` directory into a `.gz` file.
    2. Moves the compressed file to the `past_logs` directory.
    3. Clears the contents of all files in the `logs` directory after compression.

    Raises:
        FileNotFoundError: If the `debug.log` file does not exist.
        IOError: If there is an issue reading or writing files.
    """
    # Compress the log file
    with open(file_path, "rb") as f_in, gzip.open(new_file_path, "wb") as f_out:
        print("Compressing log file...")
        shutil.copyfileobj(f_in, f_out)

    # Clear all files in the logs directory after compression
    for file in os.listdir(absolute_path_to_logs):
        logs_file_path = os.path.join(absolute_path_to_logs, file)
        if not os.path.exists(logs_file_path):
            # Create the file if it doesn't exist
            open(file, 'w').close()
            print(f"File created: {logs_file_path}")
        # Truncate the file to clear its contents
        open(logs_file_path, 'r+').truncate(0)

    print(f"Compressed and moved: {new_file_path}")

# Schedule the `compress_old_logs` function to run daily at midnight
schedule.every().day.at("00:00").do(compress_old_logs)

# Run the scheduler in an infinite loop
while True:
    """
    Continuously checks and runs any scheduled tasks.

    This loop ensures that the scheduled tasks are executed at their specified times.
    It sleeps for 1 second between checks to avoid excessive CPU usage.
    """
    schedule.run_pending()
    time.sleep(1)
