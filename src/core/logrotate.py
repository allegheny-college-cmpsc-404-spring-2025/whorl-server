import os
import gzip
import logging

class GzipTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):

    doRollover(self):
        super().doRolleover()
        if os.path.exists(self.baseFilename):
            with open(self.baseFilename, 'rb') as fh:
                with gzip.open(f"{self.baseFilename}.gz", 'wb') as archive:
                    archive.writelines(fh)
            os.remove(self.baseFilename)
