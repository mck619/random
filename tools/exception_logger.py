import logging, sys, traceback, re, functools


class WrappedExceptionTracebackFormatter(logging.Formatter):
    def format(self, record):
        result = super(WrappedExceptionTracebackFormatter, self).format(record)
        result_list = result.split('|')
        tb = result_list[-1]
        tb = re.sub(r'(File.*?in wrapper\s*\n)', '',tb, flags = re.MULTILINE)
        tb = re.sub(r'(^.*?return func\(\*args, \*\*kwargs\)\s*\n)', '',tb, flags = re.MULTILINE)
        results = '|'.join(result_list[:-1]) + '|' + tb
        return results
        
def create_logger(name, path):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler(path)
 
    fmt = '%(asctime)s | %(name)s | %(levelname)s | %(message)s '
    formatter = WrappedExceptionTracebackFormatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
    
    
def log_exception(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
 
    @param logger: The logging object
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                et, ei, tb = sys.exc_info()
                stack = traceback.extract_stack()
                tb = traceback.extract_tb(tb)
                full_tb = stack[:-1] + tb
                tb_str = ''.join(traceback.format_list(full_tb))
                logger.error(e.__class__.__name__ + ei.__str__() + tb_str)
        return wrapper
    return decorator
    
def add_soup_url_to_exception():
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                et, ei, tb = sys.exc_info()
                err_func = func.__name__
                raise type(e), type(e)(e.__str__() + '| ' + 'url: ' + kwargs['soup']._url + '| function: '+err_func + '|'), tb

        return wrapper
    return decorator

def add_note_to_exception():
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                et, ei, tb = sys.exc_info()
                err_func = func.__name__
                raise type(e)(e.__str__() + '| ' + 'note: ' + note+ '| ' + '| function: '+err_func + '|'), tb
        return wrapper
    return decorator

def add_kwargs_note_to_exception(*key_words):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                et, ei, tb = sys.exc_info()
                err_func = func.__name__
                note_list = [str(kwargs[key_word]) for key_word in key_words]
                note_str = ','.join(note_list)
                raise type(e)(e.__str__() + '| ' + 'note: ' + note_str + '| ' + '| function: '+err_func + '|'), tb
        return wrapper
    return decorator    

 
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

