import logging

def init_logger(name, log_level):
    ''' init logger
    '''
    # init:
    logger = logging.getLogger(name)
    # set logging level:
    logger.setLevel(log_level)
    # set format:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # set handler:
    logger.addHandler(handler)

    # start:
    logger.debug("Starting with log level: %s" % log_level)

    return logger