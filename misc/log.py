__author__ = 'Vijay Ganesan'

import inspect

class Log:
    '''
    Log class. Call at start of function you want to check, then just use ShowDebug method to print out information anywhere
    '''
    def __init__(self):
        self.func = inspect.stack()[1] #[0] would just return Log, we want whatever called log
        self.func_prev = inspect.stack()[2]
        self.module = inspect.getmodule(self.func[0]) # Record the calling function
        self.module_prev = inspect.getmodule(self.func_prev[0])
        return
    def __del__(self):
        del self.module
        del self.module_prev
        del self.func_prev
        del self.func
        return
    def ShowDebug(self,message): #E.g. ShowDebug("function_name: message")
        print '[%s -> %s] %s' % (self.module_prev.__name__,self.module.__name__,message)
        return
