from __future__ import absolute_import

import threading


class BoundedEmptySemaphore( threading._BoundedSemaphore ):
    """
    A bounded semaphore that is initially empty.
    """

    def __init__(self, value=1, verbose=None):
        super( BoundedEmptySemaphore, self ).__init__( value, verbose )
        for i in xrange( value ):
            assert self.acquire( blocking=False )