import inspect
from io import StringIO
import logging
import sys

from io import StringIO # Python3 use: from io import StringIO
import sys
import io

#old_stdout = sys.stdout
#sys.stdout = mystdout = StringIO()
from contextlib import redirect_stdout

class capture2(redirect_stdout):

    def __init__(self):
        self.f = io.StringIO()
        self._new_target = self.f
        self._old_targets = []  # verbatim from parent class

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))  # verbatim from parent class
        setattr(sys, self._stream, self._new_target)  # verbatim from parent class
        return self  # instead of self._new_target in the parent class

    def __repr__(self):
        return self.f.getvalue()  

class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()


class Logger:

    def __init__(self):
        self.stdout = sys.stdout
        self.lastMessage = ""

    def start(self): 
        print("logger start")
        sys.stdout = self

    def stop(self): 
        sys.stdout = self.stdout

    def write(self, text): 
        self.stop()
        print("LOGGER DETECTING MESSAGE " + text)
        self.lastMessage = text
        self.start()

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def log(msg:str, lvl=logging.DEBUG):
    stack = inspect.stack()
    the_class = "NoClass"
    try:
        the_class = stack[1][0].f_locals["self"].__class__.__name__
    except KeyError :
        pass
    the_method = stack[1][0].f_code.co_name
#    path = pathlib.Path(__file__).parent.resolve()
    print("[{}.{}()]: {}".format(the_class, the_method, msg))