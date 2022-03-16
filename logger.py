import inspect
import logging


def log(msg: str, lvl=logging.DEBUG):
    stack = inspect.stack()
    the_class = "NoClass"
    try:
        the_class = stack[1][0].f_locals["self"].__class__.__name__
    except KeyError:
        pass
    the_method = stack[1][0].f_code.co_name
    print("[{}.{}()]: {}".format(the_class, the_method, msg))
