from __future__ import absolute_import

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
    """

    exception = None

    def run( self ):
        try:
            super( ExceptionalThread, self ).run( )
        except BaseException as e:
            self.exception = e
            raise

    def join( self, timeout=None ):
        super( ExceptionalThread, self ).join( timeout )
        if not self.is_alive and self.exception:
            self.exception = None
            raise self.exception
