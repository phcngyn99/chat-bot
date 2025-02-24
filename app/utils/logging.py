import logging
import datetime
import os

class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.timezone = self.get_timezone()

    def get_timezone(self):
        log_tz = os.getenv('LOG_TZ', '+7')  # Default to +7 if not set
        tz_offset = int(log_tz)  # Convert to integer
        return datetime.timezone(datetime.timedelta(hours=tz_offset))

    def converter(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp, self.timezone)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            return dt.strftime(datefmt) + f' UTC{int(os.getenv("LOG_TZ", "+7")):+d}'
        return dt.isoformat()

# Config logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Apply custom formatter to all handlers
for handler in logging.getLogger().handlers:
    handler.setFormatter(TimezoneFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                                            datefmt='%Y-%m-%d %H:%M:%S'))

# Create logger
logger = logging.getLogger(__name__)

def example():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

# Output:
# 2021-10-03 15:41:48 UTC+7 - __main__ - DEBUG - This is a debug message
# 2021-10-03 15:41:48 UTC+7 - __main__ - INFO - This is an info message
# 2021-10-03 15:41:48 UTC+7 - __main__ - WARNING - This is a warning message
# 2021-10-03 15:41:48 UTC+7 - __main__ - ERROR - This is an error message
# 2021-10-03 15:41:48 UTC+7 - __main__ - CRITICAL - This is a critical message
