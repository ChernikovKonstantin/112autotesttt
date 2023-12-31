import os
import logging

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs/api"))


logger = logging.getLogger('root')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
fh = logging.FileHandler('%s/autotests.log' % ROOT_DIR, encoding='utf-8')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)
logger.debug('START NEW SESSION')


def log_error(message, raise_exception=False):
    logger.error(message)

    if raise_exception:
        raise ValueError(message)
