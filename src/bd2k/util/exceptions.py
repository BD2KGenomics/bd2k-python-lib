from contextlib import contextmanager
import sys


@contextmanager
def panic( log=None ):
    """
    The Python idiom for reraising a primary exception fails when the except block raises a
    secondary exception, e.g. while trying to cleanup. In that case the original exception is
    lost and the secondary exception is reraised. The solution seems to be to safe the primary
    exception info as returned from sys.exc_info() and then reraise that.

    This is a contextmanager that should be used like this

    try:
         # do something that can fail
    except:
        with panic( log ):
            # do cleanup that can also fail

    If a logging logger is passed to panic(), any secondary Exception raised within the with
    block will be logged. Otherwise those exceptions are swallowed. At the end of the with block
    the primary exception will be reraised.

    """
    exc_type, exc_value, traceback = sys.exc_info( )
    try:
        yield
    except Exception as e:
        if log is not None:
            log.warn( "Exception during panic", exc_info=True )
    finally:
        raise exc_type, exc_value, traceback
