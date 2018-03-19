import logging
 
def create_logger(name, path):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler(path)
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger