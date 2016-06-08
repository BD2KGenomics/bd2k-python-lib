from contextlib import contextmanager
import sys


class panic( object ):
    """
    The Python idiom for reraising a primary exception fails when the except block raises a
    secondary exception, e.g. while trying to cleanup. In that case the original exception is
    lost and the secondary exception is reraised. The solution seems to be to save the primary
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

    def __init__( self, log=None ):
        super( panic, self ).__init__( )
        self.log = log
        self.exc_info = None

    def __enter__( self ):
        self.exc_info = sys.exc_info( )

    def __exit__( self, *exc_info ):
        if self.log is not None:
            self.log.warn( "Exception during panic", exc_info=exc_info )
        exc_type, exc_value, traceback = self.exc_info
        raise exc_type, exc_value, traceback
