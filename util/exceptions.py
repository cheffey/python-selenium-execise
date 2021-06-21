import logging


def ignoreException(runnable):
    try:
        runnable()
    except BaseException:
        pass

def printException(runnable):
    try:
        runnable()
    except BaseException as e:
        logging.exception(e)