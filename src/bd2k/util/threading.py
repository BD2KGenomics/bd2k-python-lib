from __future__ import absolute_import
import logging
import sys
import threading

class BoundedEmptySemaphore( threading._BoundedSemaphore ):
    """
    A bounded semaphore that is initially empty.
    """

    def __init__( self, value=1, verbose=None ):
        super( BoundedEmptySemaphore, self ).__init__( value, verbose )
        for i in xrange( value ):
            assert self.acquire( blocking=False )


class ExceptionalThread( threading.Thread ):
    """
    A thread whose join() method re-raises exceptions raised during run(). While join() is
    idempotent, the exception is only during the first invocation of join() that succesfully
    joined the thread. If join() times out, no exception will be re reraised even though an
    exception might already have occured in run().

    >>> def f():
    ...     assert False
    >>> t = ExceptionalThread(target=f)
    >>> t.start()
    >>> t.join()
    Traceback (most recent call last):
    ...
    AssertionError
    """

    exc_info = None

    def run( self ):
        try:
            super( ExceptionalThread, self ).run( )
        except:
            self.exc_info = sys.exc_info( )
            raise

    def join( self, *args, **kwargs ):
        super( ExceptionalThread, self ).join( *args, **kwargs )
        if not self.is_alive( ) and self.exc_info is not None:
            type, value, traceback = self.exc_info
            self.exc_info = None
            raise type, value, traceback
