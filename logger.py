import inspect
import logging
import pathlib

#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def log(msg, lvl=logging.DEBUG):
    stack = inspect.stack()
    the_class = "NoClass"
    try:
        the_class = stack[1][0].f_locals["self"].__class__.__name__
    except KeyError :
        pass
    the_method = stack[1][0].f_code.co_name
#    path = pathlib.Path(__file__).parent.resolve()
    print("[{}.{}()]: {}".format(the_class, the_method, msg))