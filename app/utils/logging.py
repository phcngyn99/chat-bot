import logging

# Config logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Create logger
logger = logging.getLogger(__name__)


def example():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

# Output:
# 2021-10-03 15:41:48 - __main__ - DEBUG - This is a debug message
# 2021-10-03 15:41:48 - __main__ - INFO - This is an info message
# 2021-10-03 15:41:48 - __main__ - WARNING - This is a warning message
# 2021-10-03 15:41:48 - __main__ - ERROR - This is an error message
# 2021-10-03 15:41:48 - __main__ - CRITICAL - This is a critical message
