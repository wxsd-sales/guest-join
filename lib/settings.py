import logging 
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(object):
    port = int(os.environ["MY_APP_PORT"].replace('"',''))
    host = os.environ["MY_APP_HOST"].replace('"','')
    redis_host = os.environ["MY_REDIS_HOST"].replace('"','')
    redis_port = int(os.environ["MY_REDIS_PORT"].replace('"',''))

    iss = os.environ["GUEST_APP_ISS"].replace('"','')
    secret = os.environ["GUEST_APP_SECRET"].replace('"','')
    
    embed_url = os.environ["EMBED_URL"].replace('"','')

    expire_days = 180


class LogRecord(logging.LogRecord):
    def getMessage(self):
        msg = self.msg
        if self.args:
            if isinstance(self.args, dict):
                msg = msg.format(**self.args)
            else:
                msg = msg.format(*self.args)
        return msg

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    blue = "\x1b[31;34m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
