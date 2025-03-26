import os
import gzip
import shutil
import datetime
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler

current_date = datetime.date.today()


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        # log_file = self.baseFilename

        # log_file = self.baseFilename
        # if os.path.exists(log_file):
        #     with open(log_file, 'rb') as f_in:
        #         with gzip.open(log_file + '.gz', 'wb') as f_out:
        #             f_out.writelines(f_in)
        #     os.remove(log_file)
        file_path = self.baseFilename

        directory = file_path.replace("/debug.log","")
        
        MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
        log_file_name = os.path.join(MODULE_PATH, "past_logs", str(current_date) + ".gz")

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f_in, gzip.open(log_file_name, "wb") as f_out:
                print(f_in)
                print('arrived')
                shutil.copyfileobj(f_in, f_out)

            # Clear all the files in src/logs log file after compression
            for file in os.listdir(directory):
                logs_file_path = os.path.join(directory, file)
                if not os.path.exists(logs_file_path):
                    open(file, 'w').close()
                    print(f"File added: {logs_file_path}")
                open(logs_file_path, 'r+').truncate(0)


def test_logging():

    MODULE_PATH = pathlib.Path(__file__).parent.parent.resolve()
    absolute_path_to_logs = os.path.join(MODULE_PATH, "logs")

    # log_dir = "logs"
    # os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(absolute_path_to_logs, "debug.log")

    logger = logging.getLogger("TestLogger")
    logger.setLevel(logging.DEBUG)

    handler = GzipTimedRotatingFileHandler(log_file, when="s", interval=5, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Generate logs for 15 seconds to trigger rollover
    import time
    for i in range(15):
        logger.info(f"Log entry {i}")
        time.sleep(1)

test_logging()