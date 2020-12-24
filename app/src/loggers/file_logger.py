import logging
from logging import Logger
import os
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from functools import wraps


# import json
class DataakLogger(Logger):
    def __init__(self, name: str):
        super().__init__(name)
        self.prefix_msg = ""

    def error(self, msg: str) -> None:
        msg = str(msg)[:7000]
        super(DataakLogger, self).error(f"{self.prefix_msg} {msg}")

    def critical(self, msg: str) -> None:
        msg = str(msg)[:7000]
        super(DataakLogger, self).critical(f"{self.prefix_msg} {msg}")

    def set_extra_config(self,configs: dict) -> None:
        self.prefix_msg = ""
        for k, v in configs.items():
            self.prefix_msg += f"<(^)> {k} @:|:@ {v} <(^)>"



logger = DataakLogger(__name__)
custom_fields = None
log_level = logging.INFO


def set_logging_config(log_configs, logger_name=__name__):
    # Log level
    level = str(log_configs.get('log_level', logging.INFO)).upper()
    global log_level
    log_level = level

    # Output format
    format = log_configs.get('format',
                             '%(asctime)s-Name %(name)s-File %(pathname)s-Line %(lineno)d-Method %(funcName)s-LogLevel %(levelname)s-Message %(message)s')

    # Output filename
    filename = log_configs.get('log_output')
    final_filename = str(__current_working_dir()) + '/ignoredfile/outputlogs/' + filename
    print('Output logs are written in ' + final_filename)

    # Rotating type
    rotating_type = log_configs.get('rotating_type', 'size')
    if rotating_type is 'size':
        __create_rotating_file_handler(final_filename, level=level, format=format)
    elif rotating_type is 'time':
        __create_time_rotating_file_handler(final_filename, level=level, format=format)

    # Log handler
    enable_console_handler = False
    log_handler_type = log_configs.get('log_handler')
    if isinstance(log_handler_type, str):
        log_handler_type = [log_handler_type]
    if 'console' in log_handler_type:
        enable_console_handler = True
    if enable_console_handler:
        __create_console_handler(level=level, format=format)

    # Responding person
    global custom_fields
    custom_fields = log_configs.get('custom_fields', None)

    global logger
    logger.name = logger_name
    logger.set_extra_config(log_configs.get('custom_fields',{}))
    # logger.error = __error


def __current_working_dir():
    """
    :return: Return parent path
    """
    path = Path(os.getcwd())
    return path


def __create_rotating_file_handler(filename, level=logging.INFO,
                                   format='%(asctime)s-Name %(name)s-File %(pathname)s-Line %(lineno)d-Method %(funcName)s-LogLevel %(levelname)s-Message %(message)s'):
    rotating_file_handler = RotatingFileHandler(filename=filename, maxBytes=262144,
                                                backupCount=40)
    rotating_file_handler.setFormatter(logging.Formatter(format))
    rotating_file_handler.setLevel(level)
    logger.addHandler(rotating_file_handler)
    logger.setLevel(level)


def __create_time_rotating_file_handler(filename, level=logging.INFO,
                                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    time_rotating_file_handler = TimedRotatingFileHandler(filename=filename, when='d', interval=1,
                                                          backupCount=8)
    time_rotating_file_handler.setFormatter(logging.Formatter(format))
    time_rotating_file_handler.setLevel(level)
    logger.addHandler(time_rotating_file_handler)


def __create_console_handler(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    # format = '{ "content": %(message)s, "asctime": "%(asctime)s", "name": "%(name)s", "pathname": "%(pathname)s", "lineno": %(lineno)d, "funcName": "%(funcName)s", "levelname": "%(levelname)s" }' # TODO: Use this
    # create console handler
    ch = logging.StreamHandler()
    # Set level to debug
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter(format)
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


spend_time_table = {}


def span_time(func):
    @wraps(func)
    def log_time(*args, **kwargs):
        start_time = time.time() * 1000
        result = func(*args, **kwargs)
        spend_time = (time.time() * 1000) - start_time
        logger.info(f"Function '{func.__qualname__}' takes: {spend_time}")
        total_spend_time = spend_time_table.get(func.__qualname__, 0)
        total_spend_time += spend_time
        spend_time_table[func.__qualname__] = total_spend_time
        logger.info(f"Total for function '{func.__qualname__}' is {total_spend_time}")
        return result

    return log_time


# This function is written by Mohammad Taheri. It may change in near future or if Kafka and logstash do not use!
# 'final_message[0:700000]': According to the Mr. Taheri's mention, this limitation is because of Kafka max size for a message.
# def __create_log_message_V2(message, custom_fields=None):
#     if custom_fields is None:
#         custom_fields = {}
#     custom_fields_sec = ' #*|*# '.join(f'{key} @:|:@ {value}' for key, value in custom_fields.items())
#     final_message = f'<(^)> {custom_fields_sec} <(^)> {message}'
#     final_message = final_message[0:700000]
#     return final_message


def __create_log_message(message, custom_fields=None):
    if custom_fields is None:
        custom_fields = {}
    final_message = {"message": message, **custom_fields}
    return final_message


# def __create_log_message_V3(message, custom_fields=None):
#     if custom_fields is None:
#         custom_fields = {}
#     final_message = {"message": message, **custom_fields}
#     return final_message

def __error(msg, *args, **kwargs):
    msg = msg[:7000]
    if log_level:
        if custom_fields is not None:
            logger._log(logging.ERROR, __create_log_message(msg, custom_fields), args, **kwargs)
        else:
            logger._log(logging.ERROR, msg, args, **kwargs)

