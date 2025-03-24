import os
import gzip
import shutil
import datetime

# Get the current date to use in the compressed log file name.
current_date = datetime.date.today()

# Define the absolute path to the logs directory and the debug log file.
absolute_path_to_logs = os.path.abspath("src/logs")
file_path = os.path.abspath("src/logs/debug.log")

# Define the path for the compressed log file in the 'past_logs' directory.
new_file_path = os.path.join("src/past_logs", str(current_date) + ".gz")

def compress_old_logs():
    """
    Compresses the current debug log file and clears all log files in the logs directory.

    This function performs the following steps:
    1. Compresses the `debug.log` file into a `.gz` file.
    2. Clears the contents of all log files in the `src/logs` directory.
    3. Ensures that any missing log files in the `src/logs` directory are created.

    After execution, the compressed log file is stored in the `src/past_logs` directory
    with the current date as its name.

    Prints:
        - Confirmation messages for compression and file clearing.
    """
    # Compress the debug log file.
    with open(file_path, "rb") as f_in, gzip.open(new_file_path, "wb") as f_out:
        print("Compressing log file...")
        shutil.copyfileobj(f_in, f_out)

    # Clear all files in the `src/logs` directory after compression.
    for file in os.listdir(absolute_path_to_logs):
        logs_file_path = os.path.join(absolute_path_to_logs, file)
        if not os.path.exists(logs_file_path):
            # Create the file if it does not exist.
            open(file, 'w').close()
            print(f"File added: {logs_file_path}")
        # Truncate the file to clear its contents.
        open(logs_file_path, 'r+').truncate(0)

    print(f"Compressed and moved: {new_file_path}")

# Execute the log compression function.
compress_old_logs()
