#!/usr/bin/env xpython
# adapted from scene_builder
import logging

LOGGER_INITIALIZED = False
LOGGER_LEVEL = logging.DEBUG

packageName = 'shaderRenamer'

def getLogger():
    """
    Returns logger object for use in this package
    """
    global LOGGER_INITIALIZED
    logger = logging.getLogger(packageName)
    if not LOGGER_INITIALIZED:
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.propagate = False
        logger.setLevel(LOGGER_LEVEL)
        console_handler = logging.StreamHandler()
        #file_handler = logging.FileHandler(getLogFile())
        formatter_console = logging.Formatter('[shaderRenamer]: %(levelname)s: %(message)s')
        formatter_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')        
        console_handler.setFormatter(formatter_console)
        #file_handler.setFormatter(formatter_file)
        logger.addHandler(console_handler)

    LOGGER_INITIALIZED = True
    return logger

# def enableDebugging():
#     """
#     Enables debugging on the logger
#     """
#     global LOGGER_INITIALIZED
#     global LOGGER_LEVEL
#     LOGGER_INITIALIZED = False
#     LOGGER_LEVEL = logging.DEBUG
#     return

# def disableDebugging():
#     """
#     Disables debugging on the logger
#     """
#     global LOGGER_INITIALIZED
#     global LOGGER_LEVEL
#     LOGGER_INITIALIZED = False
#     LOGGER_LEVEL = logging.INFO
#     return

# def getLogFile():
#     """
#     Returns the user log file
#     """
#     import os
#     PREFS_DIR=os.path.join(os.environ.get('HOME'), '.mrx', __package__)
#     if not os.path.exists(PREFS_DIR):
#         os.makedirs(PREFS_DIR)
#     return os.path.join(PREFS_DIR, '%s.log' % __package__.lower())
#     