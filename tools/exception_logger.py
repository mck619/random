import logging, sys, traceback, re, functools


class WrappedExceptionTracebackFormatter(logging.Formatter):
    def format(self, record):
        result = super(WrappedExceptionTracebackFormatter, self).format(record)
        result_list = result.split('|')
        tb = result_list[-1]
        tb = re.sub(r'(File.*?in wrapper\s*\n)', '',tb, flags = re.MULTILINE)
        tb = re.sub(r'(^.*?return func\(\*args, \*\*kwargs\)\s*\n)', '',tb, flags = re.MULTILINE)
        results = '|'.join(result_list[:-1]) + '| traceback: ' + tb
        return results
        
class MySQLHandler(logging.Handler):
    def __init__(self, db, table, col_mapping, *args, **kwargs):
        super(MySQLHandler, self).__init__(*args, **kwargs)
        self.conn = pymysql.connect(user=db['user'],
                                     password=db['password'],
                                     host=db['host'],
                                     database=db['database'])
        self.cur = self.conn.cursor()        
        self.col_mapping = col_mapping
        self.table = table
    def emit(self, record):
        msg = self.format(record)
        msgs = msg.split('|')
        log_data = {}
        for msg in msgs:
            message_type = msg[:msg.find(':')].strip()
            message_content = msg[msg.find(':')+1:].strip()
            if message_type in self.col_mapping.keys():
                log_data[self.col_mapping[message_type]] = message_content
                
        if 'time' in self.col_mapping.keys():
            tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
            log_data['time']=tm
            
        query = """ INSERT INTO {0} """.format(self.table) + construct_insert_values_string(log_data.keys())
        try:
            self.cur.execute(query, log_data)
            self.conn.commit()
        # If error - print it out on screen. Since DB is not working - there's
        # no point making a log about it to the database :)
        except pymysql.Error as e:
            print query
            print e
            print 'CRITICAL DB ERROR! Logging to database not possible!'
            
            
def create_logger(name, db, table, col_mapping):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = MySQLHandler(db, table, col_mapping)
 
    fmt ='time: %(asctime)s |logger: %(name)s |level: %(levelname)s |exception_type: %(message)s '
    formatter = WrappedExceptionTracebackFormatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
    
    
def log_exception(logger, verbose_exception_logging=False):
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
                if verbose_exception_logging:
                    print ei.__str__()
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
                raise type(e)(e.__str__() + '| ' + 'note: ' + note + '| function: '+err_func + '|'), tb
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
                raise type(e), type(e)('| exception_message: ' + e.__str__() + '| ' + 'note: ' + note_str  + '| function: '+err_func + '|'), tb
        return wrapper
    return decorator    

 
